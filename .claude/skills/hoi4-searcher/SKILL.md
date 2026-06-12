---
name: hoi4-searcher
description: Token-efficient search for ALL Hearts of Iron IV mod definitions - events, focuses, decisions, ideas, scripted effects/triggers, dynamic modifiers, on_actions, opinion modifiers, ai_strategy, technologies, characters, GFX sprites, and localisation keys. ALWAYS use this instead of reading whole mod files when locating or inspecting existing definitions. Use when (1) Finding where something is defined ("どこで定義", "find event/focus/decision/effect X", "what events exist"), (2) Searching definitions by content ("which decisions grant PP"), (3) Extracting a single definition block to read, (4) Looking up GFX sprite -> texture path, (5) Quick syntax check of edited files, or (6) Browsing available vanilla modifiers.
---

# HOI4 Searcher (統合検索)

mod内の既存定義を**ファイル全読みせずに**特定・抽出するスキル。
旧 searcher 系6スキル(event/focus/decision/modifier/scripted-effect/gfx)の統合版。

## トークン節約の原則

1. **Readでmodファイルを開く前に、必ずこのスクリプトで位置を特定する**(一覧出力は1件1行)
2. 定義の中身が必要なときは `--def` で**該当ブロックだけ**抽出する(ファイル全体をReadしない)
3. 編集後は `--check` で軽量構文チェック(MCP cwtoolsより速く、出力も小さい)

## 基本コマンド

作業ディレクトリがリポジトリルートなら `--base` 省略可(自動で `bakasekai/` に降りる)。

```bash
S=.claude/skills/hoi4-searcher/scripts/search_defs.py

# 1) 定義の一覧・検索(name は正規表現・大文字小文字無視)
python3 $S --type scripted_effect --name '^bsm_ea'
python3 $S --type event --name '^nc\.'
python3 $S --type decision --grep 'add_political_power'   # 内容で絞る(遅い)

# 2) 1定義だけブロック抽出(←ファイルをReadする代わりにこれ)
python3 $S --def bsm_ea_ai_monthly
python3 $S --def nc.4 --type event        # --type指定で高速化

# 3) 編集後の軽量構文チェック(brace/quote/BOM/loc形式)
python3 $S --check bakasekai/common/scripted_effects/foo.txt bakasekai/localisation/japanese/bar_l_japanese.yml
```

## --type 一覧

| type | 対象 | 名前の取り方 |
|---|---|---|
| `event` | events/ | `id =`(定義のみ。effect発火元は除外) |
| `focus` | common/national_focus/ | focus/shared_focusの`id =` |
| `decision` / `decision_category` | common/decisions/ | decision名 / カテゴリ名 |
| `idea` | common/ideas/ | idea名(国民精神・大臣) |
| `scripted_effect` / `scripted_trigger` | common/scripted_*/ | トップレベル名 |
| `dynamic_modifier` | common/dynamic_modifiers/ | トップレベル名 |
| `on_action` | common/on_actions/ | on_xxx(全上書き箇所が出る) |
| `opinion_modifier` | common/opinion_modifiers/ | modifier名 |
| `ai_strategy` / `ai_strategy_plan` | common/ai_strategy*/ | ブロック名 |
| `tech` | common/technologies/ | 技術名 |
| `character` | common/characters/ | キャラクター名 |
| `gfx` | interface/, gfx/ | GFX_スプライト名 |
| `loc` | localisation/ | locキー |

## 専用スクリプト(必要時のみ)

- **GFXの逆引き・texture実在確認**: `scripts/search_gfx.py --base <mod> --id GFX_x` / `--path image.png`(spriteとtextureの対応・ファイル実在チェック)
- **vanillaモディファイア探索**: `scripts/search_modifiers.py --search stability` / `--category production`(アイデア・NF作成時に使えるmodifier候補)。より正確な仕様は MCP `mcp__hoi4-modding__get_vanilla_modifiers` か `documents/00_coding_contexts/modifiers_documentation.md`

## 検索のヒント

- イベントIDはファイル名と一致しない。namespace(`add_namespace`)を先に確認: `--type event --name '^<namespace>\.'`
- BSM命名: システムファイルは `_bsm_`、効果・変数は `bsm_` プレフィックスが多い
- `--grep` は全ブロック抽出を伴うので、`--type` との併用必須・ヒット過多なら `--name` で先に絞る
- 0件のときは検索語が実際の命名と違う可能性を疑う(例: 通貨イベントのnamespaceは `nc`)

## 検証との分担

- このスキルの `--check`: 編集直後の軽量チェック(構文骨格のみ)
- MCP `mcp__hoi4__hoi4_cwtools_check`: 本格検証(スコープ・引数の妥当性まで)
- MCP `mcp__hoi4__hoi4_find_missing_keys` / `hoi4_check_missing_gfx`: loc/GFX参照の欠落検出
