#!/usr/bin/env python3
"""
ソース言語を基に他言語の不足しているローカライズキーを埋めるスクリプト

使い方例(dry-run, 出力のみ):
  python3 scripts/fill_missing_translations.py --root bakasekai/localisation --source english --out reports --dry-run

実際にファイルを更新する場合は `--apply` を付ける（推奨: 事前にgitでコミットしてから）。

注意: デフォルトはソース言語を `english` とするが、リポジトリに合わせて `japanese` など指定可能。
"""

import argparse
import os
import re
import csv
from collections import defaultdict, OrderedDict

KEY_RE = re.compile(r'^\s*([^#\n\"][^\"]*?)\s*:\s*"(.*)"\s*(#.*)?$')


def parse_localisation_file(path):
    """Return OrderedDict of key->value for given localisation file."""
    d = OrderedDict()
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                m = KEY_RE.match(line)
                if m:
                    key = m.group(1).strip()
                    val = m.group(2)
                    d[key] = val
    except Exception:
        try:
            with open(path, 'r', encoding='latin-1') as f:
                for line in f:
                    m = KEY_RE.match(line)
                    if m:
                        key = m.group(1).strip()
                        val = m.group(2)
                        d[key] = val
        except Exception:
            return d
    return d


def find_language_dirs(root):
    # immediate child dirs of root
    langs = []
    with os.scandir(root) as it:
        for entry in it:
            if entry.is_dir():
                langs.append(entry.name)
    return sorted(langs)


def collect_source_files(root, source_lang):
    source_root = os.path.join(root, source_lang)
    files = []
    for dirpath, dirnames, filenames in os.walk(source_root):
        for fname in filenames:
            if not fname.lower().endswith(('.yml', '.txt')):
                continue
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, source_root)
            files.append(rel)
    return sorted(files)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def fill_missing(root, source_lang, outdir, dry_run=True, apply=False, marker=' # TODO: translate'):
    """Scan localisation files and fill missing keys from source_lang.

    Returns list of rows for CSV report: (target_lang, relative_path, key, source_value)
    """
    root = os.path.abspath(root)
    report_rows = []
    languages = find_language_dirs(root)
    if source_lang not in languages:
        raise ValueError(f"Source language '{source_lang}' not found in {root}. Available: {languages}")

    source_files = collect_source_files(root, source_lang)

    source_root = os.path.join(root, source_lang)

    for lang in languages:
        if lang == source_lang:
            continue
        target_root = os.path.join(root, lang)
        for rel in source_files:
            src_path = os.path.join(source_root, rel)
            tgt_path = os.path.join(target_root, rel)

            src_keys = parse_localisation_file(src_path)
            tgt_keys = parse_localisation_file(tgt_path) if os.path.exists(tgt_path) else OrderedDict()

            missing = [k for k in src_keys.keys() if k not in tgt_keys]
            if not missing:
                continue

            # prepare lines to append
            lines_to_add = []
            for k in missing:
                v = src_keys[k]
                # escape double quotes in value
                v_escaped = v.replace('"', '\\"')
                line = f'{k}: "{v_escaped}"{marker} (from {source_lang})\n'
                lines_to_add.append(line)
                report_rows.append((lang, rel, k, v))

            if dry_run or not apply:
                # don't modify files
                continue

            # ensure directory exists for target file
            tgt_dir = os.path.dirname(tgt_path)
            ensure_dir(tgt_dir)
            # If target file doesn't exist, create a simple header
            if not os.path.exists(tgt_path):
                with open(tgt_path, 'w', encoding='utf-8') as f:
                    f.write('l_%s:\n' % lang)
                    f.write('\n')

            # append missing keys at end
            with open(tgt_path, 'a', encoding='utf-8') as f:
                f.write('\n')
                for line in lines_to_add:
                    f.write(line)

    # write combined CSV
    ensure_dir(outdir)
    out_csv = os.path.join(outdir, f'fill_missing_from_{source_lang}.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['target_language', 'relative_path', 'key', 'source_value'])
        for row in sorted(report_rows, key=lambda x: (x[0], x[1], x[2])):
            writer.writerow(row)

    return out_csv, report_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='bakasekai/localisation', help='localisation root dir')
    parser.add_argument('--source', default='english', help='source language folder name (e.g. english, japanese)')
    parser.add_argument('--out', default='reports', help='output directory for CSV report')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true', help='only report missing keys, do not modify files')
    parser.add_argument('--apply', dest='apply', action='store_true', help='apply changes to target files (dangerous)')
    parser.add_argument('--marker', default=' # TODO: translate', help='marker/comment to append to inserted lines')
    args = parser.parse_args()

    # default mode: dry-run unless --apply given
    dry = True if args.dry_run or not args.apply else False
    if args.apply:
        dry = False

    try:
        out_csv, rows = fill_missing(args.root, args.source, args.out, dry_run=dry, apply=args.apply, marker=args.marker)
        if rows:
            print(f'Found {len(rows)} missing keys; report written to: {out_csv}')
        else:
            print('No missing keys found.')
    except Exception as e:
        print('Error:', e)


if __name__ == '__main__':
    main()
