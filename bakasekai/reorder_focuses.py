#!/usr/bin/env python3
"""
HOI4国家フォーカスファイルを依存関係順に並び替えるスクリプト
"""
import re
import sys

def parse_focus_file(filepath):
    """フォーカスファイルをパースして、フォーカスブロックを抽出"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ヘッダー部分(focus_tree開始まで)を抽出
    header_match = re.search(r'^(.*?focus_tree\s*=\s*\{[^\}]*?country\s*=\s*\{.*?\})', content, re.DOTALL)
    if not header_match:
        print("Error: Could not find focus_tree header")
        return None, None, None
    
    header = header_match.group(1)
    remaining = content[len(header):]
    
    # フッター部分(最後の})を抽出
    # focus_treeの終了括弧を見つける
    bracket_count = 1
    pos = 0
    for i, char in enumerate(remaining):
        if char == '{':
            bracket_count += 1
        elif char == '}':
            bracket_count -= 1
            if bracket_count == 0:
                pos = i
                break
    
    body = remaining[:pos]
    footer = remaining[pos:]
    
    # フォーカスブロックを抽出
    focus_pattern = r'([ \t]*focus\s*=\s*\{(?:[^{}]|\{[^{}]*\})*\})'
    focuses = []
    
    for match in re.finditer(focus_pattern, body, re.DOTALL):
        focus_text = match.group(1)
        
        # IDを抽出
        id_match = re.search(r'id\s*=\s*(\w+)', focus_text)
        if not id_match:
            continue
        focus_id = id_match.group(1)
        
        # relative_position_idを抽出
        relative_match = re.search(r'relative_position_id\s*=\s*(\w+)', focus_text)
        relative_id = relative_match.group(1) if relative_match else None
        
        # prerequisiteを抽出
        prereqs = []
        for prereq_match in re.finditer(r'prerequisite\s*=\s*\{\s*focus\s*=\s*(\w+)', focus_text):
            prereqs.append(prereq_match.group(1))
        
        focuses.append({
            'id': focus_id,
            'text': focus_text,
            'relative_id': relative_id,
            'prereqs': prereqs,
            'processed': False
        })
    
    return header, focuses, footer

def topological_sort(focuses):
    """位相ソートを使用してフォーカスを並び替え"""
    # IDでインデックス化
    focus_map = {f['id']: f for f in focuses}
    sorted_focuses = []
    
    def visit(focus_id):
        if focus_id not in focus_map:
            return  # 存在しないフォーカスは無視
        
        focus = focus_map[focus_id]
        if focus['processed']:
            return
        
        # 依存関係を先に処理
        if focus['relative_id']:
            visit(focus['relative_id'])
        for prereq in focus['prereqs']:
            visit(prereq)
        
        # このフォーカスを追加
        if not focus['processed']:
            sorted_focuses.append(focus)
            focus['processed'] = True
    
    # すべてのフォーカスを処理
    for focus in focuses:
        visit(focus['id'])
    
    return sorted_focuses

def write_sorted_file(filepath, header, sorted_focuses, footer):
    """並び替えられたフォーカスをファイルに書き込み"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write('\n')
        for focus in sorted_focuses:
            f.write(focus['text'])
            f.write('\n')
        f.write(footer)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python reorder_focuses.py <focus_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    print(f"Processing {filepath}...")
    
    header, focuses, footer = parse_focus_file(filepath)
    if header is None:
        sys.exit(1)
    
    print(f"Found {len(focuses)} focuses")
    
    sorted_focuses = topological_sort(focuses)
    print(f"Sorted {len(sorted_focuses)} focuses")
    
    # バックアップを作成
    import shutil
    backup_path = filepath + '.backup'
    shutil.copy(filepath, backup_path)
    print(f"Backup created: {backup_path}")
    
    # 並び替えたファイルを書き込み
    write_sorted_file(filepath, header, sorted_focuses, footer)
    print(f"File reordered: {filepath}")
