---
name: hoi4-ai-modding
description: Comprehensive Hearts of Iron IV AI modding for the BSM mod. Use when (1) Controlling AI behavior - diplomacy, war targets, focus order, research, production, division/equipment design, naval missions, (2) Working with any common/ai_* file - ai_strategy, ai_strategy_plans, ai_templates, ai_equipment, ai_attitudes, ai_areas, ai_faction_theaters, ai_navy, ai_peace, (3) Tuning ai_will_do / ai_chance / ai_likelihood weights, (4) Using add_ai_strategy effect or ai_strategy_X@TAG variables, (5) Debugging AI with human_ai/aiview, or (6) User says "AIに〜させたい", "AIの挙動", "AI戦略", "AIが動かない", "make the AI do X", "AI strategy", "AI modding", etc.
---

# HOI4 AI Modding (BSM)

HOI4のAI挙動を制御するための統合スキル。「AIに何をさせたいか」から該当システムを特定し、BSM mod の規約に沿って実装する。

## 最初にやること

1. `git status --short --branch` でブランチ確認(`feature/` or `fix/` ブランチで作業)
2. 「何をAIにさせたいか」を下の対応表で該当システムに変換
3. 対応する references/ ファイルと、mod内の既存実例を読む
4. 既存ファイルに追記できるか、新規ファイルが必要かを判断(既存構成を崩さない)

## 目的 → システム対応表

| AIにさせたいこと | 使うシステム | 配置場所 | リファレンス |
|---|---|---|---|
| 特定国と同盟・敵対・宣戦・義勇軍派遣 | `ai_strategy` | `common/ai_strategy/` | [ai_strategy_reference.md](references/ai_strategy_reference.md) |
| イベント・NFから動的にAI方針を変更 | `add_ai_strategy` effect | events / focuses / decisions | [ai_strategy_reference.md](references/ai_strategy_reference.md) |
| NFの取得順序・研究配分・大臣選択を国別に指定 | `ai_strategy_plans` | `common/ai_strategy_plans/` | [ai_strategy_plans_reference.md](references/ai_strategy_plans_reference.md) |
| 個別NF・decision・イベント選択肢の選択確率 | `ai_will_do` / `ai_chance` | 各コンテンツファイル内 | [ai_content_weights_reference.md](references/ai_content_weights_reference.md) |
| 師団テンプレートの設計・アップグレード | `ai_templates` | `common/ai_templates/` | [ai_templates_reference.md](references/ai_templates_reference.md) |
| 戦車・艦船・航空機の装備設計 | `ai_equipment` | `common/ai_equipment/` | [ai_equipment_reference.md](references/ai_equipment_reference.md) |
| 海軍の任務優先度・艦隊編成 | `ai_navy` (goals/fleet/taskforce) | `common/ai_navy/` | [ai_navy_reference.md](references/ai_navy_reference.md) |
| 戦域・地域単位の兵力配分 | `ai_areas` / `ai_faction_theaters` | `common/ai_areas/` 等 | [ai_areas_theaters_reference.md](references/ai_areas_theaters_reference.md) |
| 外交感情・態度(敵視/友好)の枠組み | `ai_attitudes` / opinion | `common/ai_attitudes.txt` | [ai_diplomacy_reference.md](references/ai_diplomacy_reference.md) |
| 講和会議でのAIの要求 | `peace_ai_desires` | `common/peace_conference/ai_peace/` | [ai_diplomacy_reference.md](references/ai_diplomacy_reference.md) |
| AIが動かない・想定外の挙動を調査 | コンソール・デバッグ | - | [ai_debugging_reference.md](references/ai_debugging_reference.md) |

## mod内の実例(必ず先に確認)

新規作成の前に、同種の既存ファイルを必ず読むこと:

- `bakasekai/common/ai_strategy/bsm_iberian_ai_strategy.txt` — BSM独自の国別戦略の最小例
- `bakasekai/common/ai_strategy/sew_strategies.txt`, `CHN_civil_war.txt` — シナリオ駆動の戦略
- `bakasekai/common/ai_strategy_plans/WES.txt` — country_flagで分岐するランダムAIプラン
- `bakasekai/common/ai_templates/generic.txt` — 師団設計AIの標準形
- `bakasekai/common/ai_equipment/generic_naval.txt`, `*_tank.txt` — 装備設計AI
- `bakasekai/common/ai_navy/_documentation.md` — 目標ベース海軍AIの公式解説(日本語)
- `bakasekai/common/ai_faction_theaters/_documentation.md` — 陣営戦域の解説
- `bakasekai/common/ai_areas/default.txt` — strategic_regionのグルーピング

## BSM規約

- 新規ファイル名: BSM独自システムは `bsm_` プレフィックス(例: `bsm_iberian_ai_strategy.txt`)。国別は `TAG.txt` または `TAG_用途.txt`
- インデントはスペース2個、タブ禁止(AGENTS.md準拠。古いファイルにタブが残っていても新規コードはスペース)
- 1行1命令。コメントは日本語可、必要最低限
- システムタグ `_` をTAGとして使う場合はアポストロフィで囲む(`tag = XXX` 形式の話。詳細はCLAUDE.md)
- AI方針の動的制御はBSMでは country_flag 駆動が定番(例: EAシステムの `AI方針フラグ`、WESの `WES_AI_RANDOM_SAND`)。flagを `enable` に置き、scripted_effect / イベントからflagを立てて切り替える
- ローカライズ: `ai_strategy_plans` の `name`/`desc` は直接文字列でよいが、プレイヤーに見えるAI関連テキストは `localisation/japanese/` に追加

## パフォーマンス原則

- `ai_strategy` の `enable`/`abort` は毎日評価される。軽いトリガー(tag, has_country_flag, has_war)を先頭に、`any_state`/`any_country` 系は避けるか最後に置く
- `ai_will_do` の `modifier` も選択時に都度評価される。重いトリガーはcountry_flagにキャッシュする
- 恒久的な方針は `ai_strategy`(静的定義)、一時的・条件付きは `add_ai_strategy`(effect)を使い分ける。effectで積んだものは元のevent/focusの管理下から外れるので乱用しない
- `imgui show profiler` の Script タブで hourly/daily の負荷を確認

## 検証手順

1. 構文チェック: `mcp__hoi4__hoi4_cwtools_check` または `hoi4_lint` を変更ファイルに実行
2. 起動確認後、コンソールで:
   - `human_ai` — 自国もAI操作にして観察
   - `aiview` — 国を選択してAIの戦略値・態度を表示(`tdebug` 併用)
   - `event <id> <TAG>` — flag切替イベントの動作確認
3. `documents/00_coding_contexts/console_commands_documentation.md` にコマンド一覧
4. AI戦略値の確認は変数でも可: `ai_strategy_befriend@GER` 等(localisationに `[?ROOT.ai_strategy_befriend@GER]` を仮置きして目視)

## 関連スキル・資料の分担

- 個別コンテンツ(NF/イベント/decision/idea)の**作成自体**は `hoi4-nf-creator` / `hoi4-event-helper` / `hoi4-decisions-helper` / `hoi4-idea-creator` を使う。その中のAI重みフィールドの設計はこのスキルの [ai_content_weights_reference.md](references/ai_content_weights_reference.md) を参照
- プレイヤー用の装備variantは `hoi4-unit-design-creator`(Tsareich2用) / `hoi4-naval-oob-editor`。**AIに設計させる**場合のみこのスキルの `ai_equipment`
- 効果・トリガーの正確な仕様: `documents/00_coding_contexts/effects_documentation.md` / `triggers_documentation.md`
- AI戦略値を読む変数の全リスト: `documents/00_coding_contexts/dynamic_variables_documentation.md` の `ai_strategy_*` 項
