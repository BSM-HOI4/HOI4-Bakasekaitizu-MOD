"""Small span-preserving reader for Clausewitz GUI/GFX, without import side effects."""
from dataclasses import dataclass, field
from pathlib import Path
import re

TOKEN = re.compile(r'#[^\n]*|"(?:\\.|[^"\\])*"|[{}=]|[^\s{}="#]+')
SCALAR = r'"(?:\\.|[^"\\])*"|[^\s{}=#]+'


@dataclass
class Node:
    key: str
    start: int
    body: int
    end: int = 0
    parent: object = None
    children: list = field(default_factory=list)


def nodes(text, tolerate_outer=False):
    result, stack, previous = [], [], []
    for match in TOKEN.finditer(text):
        token = match[0]
        if token.startswith('#'):
            continue
        if token == '{':
            assigned = len(previous) > 1 and previous[-1][0] == '='
            key, start = previous[-2] if assigned else ('', match.start())
            node = Node(key, start, match.end(), parent=stack[-1] if stack else None)
            if stack:
                stack[-1].children.append(node)
            result.append(node)
            stack.append(node)
        elif token == '}':
            if not stack:
                raise ValueError('Unexpected closing brace')
            stack.pop().end = match.end()
        previous.append((token, match.start()))
        previous = previous[-2:]
    if tolerate_outer and len(stack) == 1 and stack[0].key.lower() in ('spritetypes', 'bitmapfonts'):
        # Some shipped GFX files omit only their outer wrapper's final brace.
        # Completed individual definitions remain usable; never tolerate GUI damage.
        stack.pop().end = len(text) + 1
    if stack:
        raise ValueError('Unclosed block')
    return result


def shallow(text, node):
    """Mask child blocks/comments, retaining absolute offsets and quoted # characters."""
    chars = list(text[node.body:node.end - 1])
    for child in node.children:
        a, b = child.start - node.body, child.end - node.body
        chars[a:b] = ' ' * (b - a)
    result = ''.join(chars)
    return re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*',
                  lambda m: m[0] if m[0].startswith('"') else ' ' * len(m[0]), result)


def prop(text, node, key):
    match = re.search(r'(?<![\w])' + re.escape(key) + r'\s*=\s*(' + SCALAR + ')',
                      shallow(text, node), re.I)
    if not match:
        return None
    raw = match[1]
    quoted = raw.startswith('"')
    value = raw[1:-1] if quoted else raw
    return value, node.body + match.start(1) + int(quoted), node.body + match.end(1) - int(quoted)


def value(text, node, key, default=None):
    found = prop(text, node, key)
    return found[0] if found else default


def child(text, node, key):
    return next((n for n in node.children if n.key.lower() == key.lower()), None)


def replacements(text, edits):
    edits = sorted(set(edits), reverse=True)
    last = len(text)
    for start, end, new in edits:
        if end > last:
            raise ValueError('Overlapping replacements')
        text = text[:start] + new + text[end:]
        last = start
    return text


def numeric(raw, extent=0):
    if raw is None:
        return None
    try:
        return float(raw[:-2]) * extent / 100 if raw.endswith('%%') else float(raw)
    except ValueError:
        return None


def pair(text, node, key, x='x', y='y', extent=(0, 0)):
    block = child(text, node, key)
    if not block:
        return None
    return (numeric(value(text, block, x), extent[0]), numeric(value(text, block, y), extent[1]))


def game_directory():
    candidates = [
        Path.home() / 'Library/Application Support/Steam/steamapps/common/Hearts of Iron IV',
        Path.home() / '.local/share/Steam/steamapps/common/Hearts of Iron IV',
    ]
    return next((p for p in candidates if (p / 'interface/core.gfx').exists()), candidates[0])
