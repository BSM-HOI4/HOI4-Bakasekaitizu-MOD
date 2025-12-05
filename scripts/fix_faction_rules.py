#!/usr/bin/env python3
"""
Faction rulesファイル内のイデオロギー名を修正するスクリプト
バニラのイデオロギー名をカスタムイデオロギー名に置換する
"""

import os
import re

# 置換マッピング
IDEOLOGY_REPLACEMENTS = {
    r'\bdemocratic\b': 'democratic_ideology',
    r'\bfascism\b': 'fascism_ideology',
    r'\bcommunism\b': 'communism_ideology',
    r'\bneutrality\b': 'neutrality_ideology',
}

def fix_ideology_names(file_path):
    """ファイル内のイデオロギー名を修正"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    original_content = content
    
    # 各イデオロギー名を置換
    for pattern, replacement in IDEOLOGY_REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content)
    
    # 変更があった場合のみファイルを書き込む
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        print(f"  ✓ Updated: {file_path}")
        return True
    else:
        print(f"  - No changes: {file_path}")
        return False

def main():
    """メイン処理"""
    base_dir = "/Users/eightman/Desktop/HOI4_modding/bsm_test/bakasekai/common/factions/rules"
    
    if not os.path.exists(base_dir):
        print(f"Error: Directory not found: {base_dir}")
        return
    
    files_processed = 0
    files_updated = 0
    
    # ディレクトリ内のすべての.txtファイルを処理
    for filename in os.listdir(base_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(base_dir, filename)
            files_processed += 1
            if fix_ideology_names(file_path):
                files_updated += 1
    
    print(f"\n完了: {files_processed}ファイル処理、{files_updated}ファイル更新")

if __name__ == "__main__":
    main()
