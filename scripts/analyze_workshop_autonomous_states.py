#!/usr/bin/env python3
"""
Steam Workshop MODのautonomous_states（傀儡国）一覧を作成するスクリプト
"""
import os
import re
from pathlib import Path
from collections import defaultdict

def parse_mod_descriptor(mod_path):
    """descriptor.modファイルからMOD名を取得"""
    descriptor_files = list(Path(mod_path).glob("*.mod")) + list(Path(mod_path).glob("descriptor.mod"))
    if not descriptor_files:
        return None
    
    for desc_file in descriptor_files:
        try:
            with open(desc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'name\s*=\s*"([^"]+)"', content)
                if match:
                    return match.group(1)
        except Exception as e:
            pass
    return None

def parse_autonomous_state_file(file_path):
    """autonomous_statesファイルを解析"""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return None
    except Exception as e:
        return None
    
    # IDを抽出
    id_match = re.search(r'id\s*=\s*(autonomy_\w+)', content)
    if not id_match:
        return None
    autonomy_id = id_match.group(1)
    
    # プロパティを抽出
    state_info = {
        'name': autonomy_id,
        'file': file_path.name,
        'level': None,
        'is_puppet': False,
        'min_freedom_level': None,
        'use_overlord_color': False,
        'subjects': [],
        'can_be_subjects': []
    }
    
    # levelを抽出
    level_match = re.search(r'level\s*=\s*(\d+)', content)
    if level_match:
        state_info['level'] = int(level_match.group(1))
    
    # is_puppetを抽出
    state_info['is_puppet'] = "is_puppet = yes" in content
    
    # min_freedom_levelを抽出
    min_freedom_match = re.search(r'min_freedom_level\s*=\s*([\d.]+)', content)
    if min_freedom_match:
        state_info['min_freedom_level'] = float(min_freedom_match.group(1))
    
    # use_overlord_colorを抽出
    state_info['use_overlord_color'] = "use_overlord_color = yes" in content
    
    # subjectを抽出
    subjects_match = re.findall(r'subject\s*=\s*([^\s\n]+)', content)
    state_info['subjects'] = subjects_match
    
    # can_be_subjectを抽出
    can_be_subjects_match = re.findall(r'can_be_subject\s*=\s*([^\s\n]+)', content)
    state_info['can_be_subjects'] = can_be_subjects_match
    
    return state_info

def analyze_workshop_mods(workshop_path):
    """Workshop内のMODを解析"""
    workshop_dir = Path(workshop_path)
    results = []
    
    print(f"Workshopディレクトリ: {workshop_dir}")
    print(f"解析対象MOD数: {len([d for d in workshop_dir.iterdir() if d.is_dir()])}")
    
    for mod_dir in sorted(workshop_dir.iterdir()):
        if not mod_dir.is_dir():
            continue
        
        workshop_id = mod_dir.name
        mod_name = parse_mod_descriptor(mod_dir)
        if not mod_name:
            mod_name = f"Unknown ({workshop_id})"
        
        # autonomous_statesフォルダを検索
        autonomous_states_dir = mod_dir / "common" / "autonomous_states"
        if not autonomous_states_dir.exists():
            continue
        
        # autonomous_statesファイルを解析
        all_states = []
        for state_file in sorted(autonomous_states_dir.glob("*.txt")):
            state = parse_autonomous_state_file(state_file)
            if state:
                all_states.append(state)
        
        if all_states:
            result = {
                'workshop_id': workshop_id,
                'mod_name': mod_name,
                'states': all_states
            }
            results.append(result)
    
    return results

def generate_report(results, output_json, output_csv):
    """レポートを生成"""
    import json
    import csv
    
    # JSON形式で出力
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # CSV形式で出力
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Workshop ID', 'MOD名', 'ファイル名', '傀儡国名', 
            'レベル', 'Subject', 'Can Be Subject'
        ])
        
        for result in results:
            for state in result['states']:
                writer.writerow([
                    result['workshop_id'],
                    result['mod_name'],
                    state['file'],
                    state['name'],
                    state['level'] if state['level'] is not None else '',
                    '; '.join(state['subjects']),
                    '; '.join(state['can_be_subjects'])
                ])

def print_summary(results):
    """サマリーを表示"""
    print(f"\n{'='*80}")
    print(f"Workshop MODの傀儡国一覧")
    print(f"{'='*80}")
    
    total_states = 0
    for result in results:
        print(f"\n[{result['workshop_id']}] {result['mod_name']}")
        print(f"  傀儡国種類数: {len(result['states'])}")
        
        for state in sorted(result['states'], key=lambda x: (x['level'] or 99, x['name'])):
            subjects_str = ', '.join(state['subjects']) if state['subjects'] else 'なし'
            print(f"    - {state['name']} (level={state['level']}, subject=[{subjects_str}])")
        
        total_states += len(result['states'])
    
    print(f"\n{'='*80}")
    print(f"合計MOD数: {len(results)}")
    print(f"合計傀儡国種類数: {total_states}")
    print(f"{'='*80}")

if __name__ == "__main__":
    workshop_path = "/Users/eightman/Library/Application Support/Steam/steamapps/workshop/content/394360"
    output_json = "workshop_autonomous_states.json"
    output_csv = "workshop_autonomous_states.csv"
    
    results = analyze_workshop_mods(workshop_path)
    generate_report(results, output_json, output_csv)
    print_summary(results)
    
    print(f"\n出力ファイル:")
    print(f"  JSON: {output_json}")
    print(f"  CSV:  {output_csv}")
