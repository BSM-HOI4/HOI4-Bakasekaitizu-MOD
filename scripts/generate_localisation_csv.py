#!/usr/bin/env python3
"""
ローカライズファイルを走査して、言語ごとにファイル名・パス・キー数をCSVで出力するスクリプト
出力:
  - localisation_report_{lang}.csv (各言語フォルダ単位)
  - localisation_report_all.csv (全言語まとめ)

使い方:
  python3 scripts/generate_localisation_csv.py --root bakasekai/localisation --out reports

"""

import argparse
#!/usr/bin/env python3
"""
ローカライズファイルを走査して、言語ごとにファイル名・パス・キー数をCSVで出力するスクリプト
出力:
  - localisation_report_{lang}.csv (各言語フォルダ単位)
  - localisation_report_all.csv (全言語まとめ)

使い方:
  python3 scripts/generate_localisation_csv.py --root bakasekai/localisation --out reports

"""

import argparse
import csv
import os
import re
from collections import defaultdict

# Paradox localization files often use key: "value" or key: "value" #comments
# We will count keys by matching lines that look like: ^\s*<key>\s*:\s"<value>"\s*(#.*)?$
# Use a raw string with single quotes so double quotes don't need escaping.
KEY_RE = re.compile(r'^\s*([^#\n"][^\"]*?)\s*:\s".*"\s*(#.*)?$')


def count_keys_in_file(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            count = 0
            for line in f:
                if KEY_RE.match(line):
                    count += 1
            return count
    except Exception:
        # fallback: try latin1
        try:
            with open(path, "r", encoding="latin-1") as f:
                count = 0
                for line in f:
                    if KEY_RE.match(line):
                        count += 1
                return count
        except Exception:
            return 0


def is_localisation_file(fname):
    # consider .yml and .txt files in localisation folders
    return fname.lower().endswith(('.yml', '.txt'))


def gather_localisation(root):
    # Expect structure: root/<language>/*.yml
    results = defaultdict(list)  # lang -> list of (filename, relpath, keycount)
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        # dirpath like /.../localisation/japanese or /.../localisation/japanese/some
        rel_dir = os.path.relpath(dirpath, root)
        parts = rel_dir.split(os.sep)
        if parts == ['.']:
            language = None
        else:
            language = parts[0]
        for fname in filenames:
            if not is_localisation_file(fname):
                continue
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, root)
            keycount = count_keys_in_file(full)
            lang_key = language if language and language != '.' else 'unknown'
            results[lang_key].append((fname, rel, keycount))
    return results


def write_csv_per_language(results, outdir):
    os.makedirs(outdir, exist_ok=True)
    all_rows = []
    for lang, files in sorted(results.items()):
        csv_path = os.path.join(outdir, f"localisation_report_{lang}.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["language", "filename", "relative_path", "key_count"])
            for fname, rel, count in sorted(files, key=lambda x: x[1]):
                writer.writerow([lang, fname, rel, count])
                all_rows.append((lang, fname, rel, count))
    # write combined
    combined_path = os.path.join(outdir, "localisation_report_all.csv")
    with open(combined_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["language", "filename", "relative_path", "key_count"])
        for row in sorted(all_rows, key=lambda x: (x[0], x[2])):
            writer.writerow(row)
    return outdir, combined_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='bakasekai/localisation', help='localisation root dir')
    parser.add_argument('--out', default='reports', help='output directory for CSVs')
    args = parser.parse_args()

    results = gather_localisation(args.root)
    outdir, combined = write_csv_per_language(results, args.out)
    print(f"Wrote reports to {outdir}")
    print(f"Combined CSV: {combined}")


if __name__ == '__main__':
    main()
