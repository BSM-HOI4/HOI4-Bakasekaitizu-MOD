# CLAUDE.md

This file provides Claude Code guidance for working in the HOI4-Bakasekaitizu-MOD repository.

Always read `AGENTS.md` first. That file contains the shared rules for all AI agents, including GitFlow, branch naming, safety, style, and validation.

Do not modify any `.wav` or `.ogg` files.

## Project Overview

This is **HOI4-Bakasekaitizu-MOD** (バカ世界地図MOD), a comprehensive Hearts of Iron IV modification based on the "Foolish World Map Project" from Chakuwiki. It's a total conversion mod that reimagines the world with alternative history, geography, and countries.

## シンボルインデックス（Grep総当たり禁止）

定義の場所を探すときは、mod全体をGrepする前に必ずインデックスを引く:

- `bakasekai/hoi4_index.tsv` — event / focus / idea / decision / scripted_effect / scripted_trigger / equipment / oob_variant の `type \t name \t path \t line`
- `bakasekai/hoi4_loc_keys.tsv` — localisation キー一覧（キー存在確認はここで済ませ、yml本文は翻訳作業時のみ読む）

例: `grep -P '^event\tjapan' bakasekai/hoi4_index.tsv` → 該当ファイルの該当行だけ読む。

再生成（common/events/localisation を編集したら実行）:
```
python3 ~/Desktop/HOI4_modding/tools/hoi4_index.py bakasekai
```
`gfx/ map/ music/ sound/ portraits/ interface/` は探索対象外（アセットのみ）。定義ブロックの抽出には hoi4-searcher スキルを併用する。

## Key Development Information

### Performance Optimization Commands
Use the in-game profiler to identify performance bottlenecks:
```
imgui show profiler
```
Enable collection and use the Script tab to analyze processing times. Focus on optimizing `hourly` processes which impact performance most.

### Project Structure

**Core Directories:**
- `bakasekai/` - Main mod content (HOI4 standard structure)
- `documents/00_coding_contexts/` - Development documentation and optimization guides
- `flags/` - Country flag assets organized by number prefixes (00/, 01/, 02/, 03/)

**Critical HOI4 Mod Structure:**
- `bakasekai/common/` - Game rules, countries, focuses, decisions, ideas, etc.
- `bakasekai/events/` - Event definitions for countries and mechanics
- `bakasekai/history/` - Initial game state (countries, states, units)
- `bakasekai/localisation/` - Text translations (primarily Japanese)
- `bakasekai/gfx/` - Graphics and interface files
- `bakasekai/map/` - Map data, provinces, terrain
- `bakasekai/interface/` - UI definitions and scripted GUIs

### Mod Configuration
- **Version:** Alpha 0.1
- **Supported HOI4 Version:** 1.13.*
- **Dependencies:** Japanese Language mod
- **Steam Workshop ID:** 2585391890

### Custom Systems

**BSM (Bakasekai) Systems:**
- Harvest System (`_bsm_Harvest_System.*`)
- Mine Development System (`_bsm_mine_system.*`) 
- Mercenary System (`_bsm_mercenary_system.*`)
- Custom diplomatic actions and scripted GUIs

**Modified Vanilla Systems:**
- **Ideologies:** Vanilla ideology names have been changed to avoid conflicts:
  - `communism` → `communism_ideology`
  - `democratic` → `democratic_ideology`
  - `fascism` → `fascism_ideology`
  - `neutrality` → `neutrality_ideology`

**Performance Considerations:**
- Use early returns in triggers (check lightweight conditions first)
- Avoid `any_state` in frequently-executed code
- Leverage caching with country flags for state-dependent decisions
- Mission-type decisions are heavy - consider alternatives where possible

### Country Tags and Scope
The mod includes hundreds of custom countries with unique 3-letter tags:
- Major powers: USA, GBR, DEU, SOV, JPN, etc.
- Custom nations: BKK (Bangkok), MAC (McDonald's), WES (Western Sahara), etc.
- Formable nations and dynamic countries supported

### Development Workflow

**File Organization:**
- Country-specific files use 3-letter country codes (e.g., `JPN.txt`, `USA.txt`)
- System files prefixed with `_bsm_`
- Generic/shared content in files like `generic.txt`

**Localization:**
- Primary language: Japanese (`localisation/japanese/`)
- Organized by feature area (countries, events, focuses)
- Uses `.yml` format with proper encoding

**Testing:**
- Custom test scenarios in `tests/` directory
- Debug events and decisions available
- Performance profiler integration for optimization

## Claude Workflow

Before edits:

- Run `git status --short --branch`.
- Confirm the work is on a properly named branch, such as `feature/JPN_project` or `fix/crash_TAG_event`.
- If the task covers unrelated areas, split the work by branch.
- Inspect nearby files before creating new patterns.

During edits:

- Keep changes scoped to the request.
- Preserve user changes and unrelated work.
- Prefer existing bsm_test conventions over patterns from other repositories.
- Use concise comments only where the script is not self-explanatory.

After edits:

- Review changed files.
- Run the most relevant lightweight validation available (see table below).
- Report changed files and any validation that could not be run.

## Skill Routing & Token Economy

**調査(トークン節約・必須)**: 既存定義の場所特定・抽出は `hoi4-searcher` スキルの
`python3 .claude/skills/hoi4-searcher/scripts/search_defs.py` を使う。modファイルをReadで全読みしない。
一覧(`--type X --name Y`、1件1行)→ 中身が必要な定義だけ `--def NAME` でブロック抽出、の順。

**実装**: タスクに対応するスキルを必ず起点にする(一覧はスキルのdescription参照)。主な対応:
イベント実装=`hoi4-event-helper` / シナリオ設計=`hoi4-event` / NF=`hoi4-nf-creator` / decision=`hoi4-decisions-helper` /
国民精神=`hoi4-idea-creator` / modifier=`hoi4-modifier-maker` / scripted effect・trigger・loc=`hoi4-scripted-*` /
変数=`hoi4-variable-helper` / on_actions=`hoi4-on-actions-helper` / GUI=`hoi4-gui` / AI挙動=`hoi4-ai-modding` /
画像=`hoi4-image-asset-creator` / 艦船OOB=`hoi4-naval-oob-editor` / 技術=`hoi4-techtree-creator` / 装備=`hoi4-unit-design-creator` /
国家追加・初期状態=`hoi4-country-setup` / 陸空OOB=`hoi4-land-air-oob` / マップ編集=`hoi4-map-editing`(**map/配下を触ったら必ず**キャッシュ削除+2回起動検証)

**検証(変更種別→ツール)**: まず `search_defs.py --check <changed files>`(brace/BOM/loc形式の即時チェック)。その後:

| 変更したもの | 追加で実行 |
|---|---|
| common/, events/ の script | `mcp__hoi4__hoi4_cwtools_check`(変更ファイルのみ) |
| localisation .yml | `mcp__hoi4__hoi4_find_missing_keys` |
| .gfx / GFX_ 参照追加 | `mcp__hoi4__hoi4_check_missing_gfx` |
| 画像アセット | `mcp__hoi4__hoi4_convert_images`(TGA/DDS変換) |

vanillaの効果・トリガー・modifier仕様の確認は `documents/00_coding_contexts/` の辞書か
`mcp__hoi4-modding__get_vanilla_modifiers` / `get_clausewitz_ref` を使い、推測で書かない。

### Variable System
The mod uses HOI4's variable system extensively for dynamic content. Key commands:
- `set_variable = { var = name value = X }`
- `add_to_variable`, `subtract_from_variable`, `multiply_variable`, `divide_variable`
- `check_variable` for triggers
- Visualization in localization: `[?variable_name]`

### Character and Leader System
Extensive character definitions in `common/characters/` organized by country, including:
- Country leaders with custom traits
- Military advisors and field marshals  
- Custom portrait assignments in `portraits/`

## Development Best Practices

1. **Performance First:** Always consider the performance impact of triggers and effects, especially those that run hourly
2. **Consistent Naming:** Follow the established country code conventions and BSM prefixing
3. **Localization:** Ensure all new content has proper Japanese localization
4. **Testing:** Use debug tools and test scenarios to verify functionality
5. **Documentation:** Complex systems should include documentation files in appropriate directories
6. **Effects and Triggers:** When implementing logic, consult the coding context references:
   - Effects: `documents/00_coding_contexts/01_effects/effects.json`
   - Triggers: `documents/00_coding_contexts/04_triggers/triggers.json`
7. **システムタグ `_` の記述ルール:** TAGとして使用する場合は必ずアポストロフィで囲む。スコープ: `XXX = { ... }`、トリガー: `tag = XXX`、`NOT = { tag = XXX }`。囲まないと変数名として解釈される。

## Branch Policy

Claude must follow the branch policy in `AGENTS.md`:

- No direct push to `main`.
- Finished branches merge into `develop`.
- Start work on a branch.
- Switch branches between unrelated items.
- Use `type/scope_name` branch names.

## External References

Use `SSW_mod` and `Tsareich2` as reference repositories only for general HOI4 and AI-agent workflow patterns. Do not copy their mod-specific systems, tags, IDs, worldbuilding, or naval rules into this mod unless the user explicitly asks.

## Asset References
- For a complete list of goal interface graphics, see [goals_file_list.md](goals_file_list.md).
