#!/usr/bin/env python3
"""
HOI4 Autonomous States 完全調査スクリプト
指定された親フォルダ内にある複数のMODを横断して分析します。
"""

import os
import re
import json
import csv
from pathlib import Path
from collections import defaultdict
import argparse

class AutonomousStatesAnalyzer:
    def __init__(self, mod_paths):
        """
        Args:
            mod_paths (list[Path]): 分析対象のMODフォルダパスのリスト
        """
        self.mod_paths = mod_paths
        self.autonomous_states = {}
        self.localizations = defaultdict(lambda: defaultdict(dict))
        
    def _parse_state_file(self, filepath, mod_name):
        """autonomous_states/*.txtをパース"""
        try:
            content = filepath.read_text(encoding="utf-8-sig") # BOM付きUTF-8に対応
        except Exception:
            content = filepath.read_text(encoding="utf-8")

        # IDを抽出
        id_match = re.search(r'id\s*=\s*(autonomy_\w+)', content)
        if not id_match:
            return
        autonomy_id = id_match.group(1)
        
        # プロパティを抽出
        is_puppet = "is_puppet = yes" in content
        min_freedom = re.search(r'min_freedom_level\s*=\s*([\d.]+)', content)
        min_freedom_val = float(min_freedom.group(1)) if min_freedom else None
        use_overlord_color = "use_overlord_color = yes" in content
        
        # HOI4のMOD読み込み順と同様に、後から読み込んだもので上書きする
        self.autonomous_states[autonomy_id] = {
            "id": autonomy_id,
            "filepath": f"{mod_name}/{filepath.name}",
            "is_puppet": is_puppet,
            "min_freedom_level": min_freedom_val,
            "use_overlord_color": use_overlord_color
        }
    
    def load_autonomous_states(self):
        """autonomous_states定義ファイルを読み込み"""
        total_files = 0
        for mod_path in self.mod_paths:
            state_dir = mod_path / "common/autonomous_states"
            if not state_dir.exists():
                continue
            
            state_files = sorted(state_dir.glob("*.txt"))
            if state_files:
                print(f"  MOD '{mod_path.name}': {len(state_files)}個の州ファイルを読み込み")
                for filepath in state_files:
                    self._parse_state_file(filepath, mod_path.name)
                    total_files += 1
        
        print(f"\n合計 {total_files}個の州ファイルを処理しました。")
        print(f"ユニークな自治州ID: {len(self.autonomous_states)}個")
    
    def _parse_localization_file(self, yml_file, lang):
        """ロケールファイルをパース"""
        try:
            content = yml_file.read_text(encoding="utf-8-sig") # BOM付きUTF-8に対応
            
            lines = content.split('\n')
            for line in lines:
                match = re.match(r'^\s*([A-Z0-9_]+):\d+\s*"([^"]*)"', line)
                if match:
                    key, value = match.groups()
                    value = value.strip()
                    # 後から読み込んだもので上書き
                    self.localizations[lang][key] = value
        except Exception as e:
            print(f"警告: {yml_file} の読み込みに失敗: {e}")
    
    def load_all_localizations(self):
        """全言語ロケールを読み込み"""
        for mod_path in self.mod_paths:
            loc_dir = mod_path / "localisation"
            if not loc_dir.exists():
                continue
            
            print(f"  MOD '{mod_path.name}' のロケールを走査:")
            for lang_dir in loc_dir.glob("*/"):
                lang = lang_dir.name.replace("_l", "") # english_l_english -> english
                if lang in ["replace"]:
                    continue
                
                yml_files = list(lang_dir.glob("*.yml"))
                if yml_files:
                    print(f"    - {lang}: {len(yml_files)}ファイル")
                    for yml_file in yml_files:
                        self._parse_localization_file(yml_file, lang)

    def extract_autonomy_localization_keys(self):
        """全ロケールからautonomy関連キーを抽出"""
        autonomy_keys = defaultdict(lambda: defaultdict(set))
        
        for lang, locs in self.localizations.items():
            for key, value in locs.items():
                if "autonomy" in key.lower():
                    # 国別キー: COUNTRY_autonomy_LEVEL
                    match = re.match(r'^([A-Z]{3})_([a-z]+)?_?(autonomy_\w+)', key)
                    if match:
                        parts = match.groups()
                        if parts[0] and parts[2]:
                            country = parts[0]
                            autonomy_id = parts[2]
                            autonomy_keys[lang][autonomy_id].add((country, key, value))
        
        return autonomy_keys
    
    def check_japanese_translations(self, autonomy_keys):
        """日本語訳の有無を確認"""
        results = []
        
        for autonomy_id in sorted(self.autonomous_states.keys()):
            state_data = self.autonomous_states[autonomy_id]
            
            # 英語ロケールで確認
            english_names = []
            for country, key, value in autonomy_keys.get("english", {}).get(autonomy_id, []):
                english_names.append({
                    "country": country,
                    "key": key,
                    "value": value
                })
            
            # 日本語ロケールで確認
            japanese_names = []
            has_japanese = False
            for country, key, value in autonomy_keys.get("japanese", {}).get(autonomy_id, []):
                has_japanese = True
                japanese_names.append({
                    "country": country,
                    "key": key,
                    "value": value
                })
            
            # 基本英語名を決定
            base_english_name = self._get_base_english_name(autonomy_id, english_names)
            
            # 和訳候補生成
            jp_candidate = self._generate_japanese_candidate(autonomy_id)
            
            results.append({
                "id": autonomy_id,
                "filepath": state_data["filepath"],
                "english_name": base_english_name,
                "has_japanese": has_japanese,
                "japanese_count": len(japanese_names),
                "min_freedom": state_data["min_freedom_level"],
                "is_puppet": state_data["is_puppet"],
                "uses_overlord_color": state_data["use_overlord_color"],
                "english_examples": english_names[:3],
                "japanese_examples": japanese_names[:3],
                "japanese_candidate": jp_candidate
            })
        
        return results
    
    def _get_base_english_name(self, autonomy_id, english_names):
        known_names = {
            "autonomy_puppet": "Puppet", "autonomy_colony": "Colony", "autonomy_dominion": "Dominion",
            "autonomy_integrated_puppet": "Integrated Puppet", "autonomy_reichskommissariat": "Reichskommissariat",
            "autonomy_reichsprotectorate": "Reichsprotectorate", "autonomy_satellite": "Satellite",
            "autonomy_supervised_state": "Supervised State", "autonomy_collaboration_government": "Collaboration Government",
            "autonomy_personal_union": "Personal Union", "autonomy_wtt_imperial_associate": "Imperial Associate",
            "autonomy_wtt_imperial_protectorate": "Imperial Protectorate", "autonomy_wtt_imperial_subject": "Imperial Subject",
            "autonomy_sea_warlord_subject": "Warlord", "autonomy_sea_integrated_warlord_subject": "Integrated Warlord",
            "autonomy_aat_defense_council_member": "Defense Council Member", "autonomy_austro_hungarian_subject": "Austro-Hungarian Subject",
            "autonomy_eu_member": "EU Member", "autonomy_volkskommissariat": "Volkskommissariat"
        }
        if autonomy_id in known_names: return known_names[autonomy_id]
        if english_names:
            value = english_names[0]["value"]
            if "$OVERLORDADJ$" in value: return autonomy_id.replace("autonomy_", "").replace("_", " ").title()
            return value
        return autonomy_id.replace("autonomy_", "").replace("_", " ").title()

    def _generate_japanese_candidate(self, autonomy_id):
        translations = {
            "autonomy_puppet": "傀儡国家", "autonomy_colony": "植民地", "autonomy_dominion": "自治領",
            "autonomy_integrated_puppet": "統合傀儡国家", "autonomy_reichskommissariat": "帝国委任統治領",
            "autonomy_reichsprotectorate": "帝国保護領", "autonomy_satellite": "衛星国",
            "autonomy_supervised_state": "監督国家", "autonomy_collaboration_government": "協力政府",
            "autonomy_personal_union": "同君連合", "autonomy_wtt_imperial_associate": "帝国連合国",
            "autonomy_wtt_imperial_protectorate": "帝国保護領", "autonomy_wtt_imperial_subject": "帝国従属国",
            "autonomy_sea_warlord_subject": "軍閥", "autonomy_sea_integrated_warlord_subject": "統合軍閥",
            "autonomy_aat_defense_council_member": "防衛評議会メンバー", "autonomy_austro_hungarian_subject": "オーストリア・ハンガリー従属国",
            "autonomy_eu_member": "EU加盟国", "autonomy_volkskommissariat": "人民委員区"
        }
        return translations.get(autonomy_id, autonomy_id.replace("autonomy_", "").replace("_", " ").title())

    def print_summary(self, results):
        print("\n" + "="*80)
        print("Autonomous States 分析結果")
        print("="*80)
        print(f"\n総計: {len(results)}個の自治州")
        with_jp = sum(1 for r in results if r["has_japanese"])
        print(f"  日本語訳あり: {with_jp}個")
        print(f"  日本語訳なし: {len(results) - with_jp}個")
        print("\nFreedom Level 順（低→高）:")
        sorted_by_freedom = sorted(results, key=lambda x: (x["min_freedom"] or 1.0))
        for i, r in enumerate(sorted_by_freedom, 1):
            jp_status = "✓" if r["has_japanese"] else "✗"
            print(f"{i:2d}. {r['id']:45s} Freedom: {str(r['min_freedom']):5s} JP: {jp_status}")
        print("\n" + "-"*80)
        print("日本語訳が必要な自治州:")
        print("-"*80)
        for r in sorted(results, key=lambda x: x["id"]):
            if not r["has_japanese"]:
                print(f"\nID: {r['id']}")
                print(f"  ファイル: {r['filepath']}")
                print(f"  英語名: {r['english_name']}")
                print(f"  和訳候補: {r['japanese_candidate']}")
                print(f"  Freedom: {r['min_freedom']}, Puppet: {r['is_puppet']}, Overlord Color: {r['uses_overlord_color']}")
                if r["english_examples"]:
                    print(f"  使用例（英語）:")
                    for ex in r["english_examples"][:2]:
                        print(f"    {ex['country']}: {ex['value']}")

    def export_csv(self, results, filename="autonomous_states_analysis.csv"):
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            fieldnames = ["id", "filepath", "english_name", "has_japanese", "japanese_count", "min_freedom", "is_puppet", "uses_overlord_color", "japanese_candidate", "english_examples", "japanese_examples"]
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(results)
        print(f"\nCSV出力: {filename}")
    
    def export_json(self, results, filename="autonomous_states_analysis.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"JSON出力: {filename}")

def main():
    parser = argparse.ArgumentParser(description="HOI4の複数のMODフォルダを横断して、自治州定義とローカライズを分析します。")
    parser.add_argument(
        "parent_dir",
        nargs="?",
        default=str(Path.cwd()),
        help="分析対象のMOD群が格納されている親フォルダ。指定しない場合はカレントディレクトリを親フォルダと見なします。"
    )
    args = parser.parse_args()
    
    parent_dir = Path(args.parent_dir).resolve()
    
    print("HOI4 Autonomous States 分析ツール")
    print(f"対象の親フォルダ: {parent_dir}")
    
    # 親フォルダ直下のディレクトリをMOD候補としてリストアップ
    # .git や documents などの明らかにMODではないフォルダを除外
    excluded_dirs = {".git", "documents", "tests", ".vscode"}
    mod_paths = [p for p in parent_dir.glob('*') if p.is_dir() and p.name not in excluded_dirs]
    
    if not mod_paths:
        print(f"エラー: {parent_dir} に分析対象となるMODフォルダが見つかりません。")
        print("正しい親フォルダを指定するか、スクリプトの実行場所を確認してください。")
        return

    print(f"発見されたMOD候補: {[p.name for p in mod_paths]}")
    print("-" * 40)
    
    analyzer = AutonomousStatesAnalyzer(mod_paths)
    
    print("\n1. 自治州定義 (autonomous_states) の読み込み:")
    analyzer.load_autonomous_states()
    
    print("\n2. ローカライズファイルの読み込み:")
    analyzer.load_all_localizations()
    
    print("\n3. autonomy関連キーの抽出と分析:")
    autonomy_keys = analyzer.extract_autonomy_localization_keys()
    results = analyzer.check_japanese_translations(autonomy_keys)
    
    analyzer.print_summary(results)
    
    print("\n4. 結果をファイルに出力:")
    analyzer.export_csv(results)
    analyzer.export_json(results)
    
    print("\n分析完了！")

if __name__ == "__main__":
    main()
