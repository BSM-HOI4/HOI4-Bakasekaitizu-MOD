#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テスト用: 単一ファイルでスクリプトをテスト
"""

import os
import re
from pathlib import Path


def parse_resources(content):
    """
    ファイルコンテンツからresourcesブロックを解析し、steel、oil、coalの値を抽出
    
    Returns:
        tuple: (steel_value, oil_value, coal_value, resources_start, resources_end)
    """
    # resourcesブロックを探す
    resources_pattern = r'resources\s*=\s*\{([^}]*)\}'
    match = re.search(resources_pattern, content, re.DOTALL)
    
    if not match:
        return None, None, None, None, None
    
    resources_block = match.group(1)
    resources_start = match.start()
    resources_end = match.end()
    
    # steel値を抽出
    steel_match = re.search(r'steel\s*=\s*(\d+(?:\.\d+)?)', resources_block)
    steel_value = float(steel_match.group(1)) if steel_match else 0
    
    # oil値を抽出
    oil_match = re.search(r'oil\s*=\s*(\d+(?:\.\d+)?)', resources_block)
    oil_value = float(oil_match.group(1)) if oil_match else 0
    
    # coal値を抽出（既存の値があるか確認）
    coal_match = re.search(r'coal\s*=\s*(\d+(?:\.\d+)?)', resources_block)
    coal_value = float(coal_match.group(1)) if coal_match else None
    
    return steel_value, oil_value, coal_value, resources_start, resources_end


def calculate_coal(steel, oil):
    """
    Coal値を計算: steel * 1.5 + oil / 2
    
    Returns:
        int: 計算されたcoal値（整数に丸める）
    """
    coal = steel * 1.5 + oil / 2
    return int(round(coal))


def update_coal_in_resources(content, coal_value):
    """
    resourcesブロック内のcoal値を更新または追加
    
    Returns:
        str: 更新されたコンテンツ（ファイル全体）
    """
    # resourcesブロックを探す
    resources_pattern = r'(resources\s*=\s*\{)([^}]*?)(\})'
    match = re.search(resources_pattern, content, re.DOTALL)
    
    if not match:
        return content
    
    resources_start = match.group(1)
    resources_content = match.group(2)
    resources_end = match.group(3)
    
    # 既存のcoal行を探す
    coal_pattern = r'\s*coal\s*=\s*\d+(?:\.\d+)?[^\n]*\n?'
    
    if re.search(coal_pattern, resources_content):
        # 既存のcoal行を更新
        new_resources_content = re.sub(
            coal_pattern,
            f'\t\tcoal={coal_value}\n',
            resources_content
        )
    else:
        # coal行を追加（最後の行の前に挿入）
        # インデントを保持するため、既存の行からインデントを取得
        lines = resources_content.split('\n')
        # 空行でない最後の行を見つける
        last_line_with_content = None
        for line in reversed(lines):
            if line.strip():
                last_line_with_content = line
                break
        
        # インデントを取得（タブまたはスペース）
        indent = '\t\t'  # デフォルト
        if last_line_with_content:
            indent_match = re.match(r'^(\s+)', last_line_with_content)
            if indent_match:
                indent = indent_match.group(1)
        
        # coal行を追加
        # 最後の非空行の後に追加
        if resources_content.rstrip():
            new_resources_content = resources_content.rstrip() + f'\n{indent}coal={coal_value}\n'
        else:
            new_resources_content = f'{indent}coal={coal_value}\n'
    
    # 新しいresourcesブロックを構築
    new_resources_block = resources_start + new_resources_content + resources_end
    
    # ファイル全体のコンテンツ内でresourcesブロックを置き換える
    new_content = content[:match.start()] + new_resources_block + content[match.end():]
    
    return new_content


# テスト用のファイルパス
test_file = Path(__file__).parent / 'bakasekai' / 'history' / 'states' / '67-Oberschlesien.txt'

print(f"Testing with: {test_file.name}")
print("-" * 60)

# ファイルを読み込む
with open(test_file, 'r', encoding='utf-8') as f:
    original_content = f.read()

print("Original file length:", len(original_content), "bytes")
print("Original file lines:", len(original_content.split('\n')))

# resourcesを解析
steel, oil, existing_coal, _, _ = parse_resources(original_content)
print(f"Steel: {steel}, Oil: {oil}")

# coal値を計算
calculated_coal = calculate_coal(steel, oil)
print(f"Calculated coal: {calculated_coal}")

# coal値を更新
new_content = update_coal_in_resources(original_content, calculated_coal)

print("\nNew file length:", len(new_content), "bytes")
print("New file lines:", len(new_content.split('\n')))

print("\n" + "=" * 60)
print("UPDATED CONTENT:")
print("=" * 60)
print(new_content)
