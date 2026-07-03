# Repository Guidelines (HOI4-Bakasekaitizu-MOD)

## 目的 / Purpose
- 本ファイルはエージェント向けの作業指針です。
- HOI4 1.13.* 向けの総変換MOD開発を前提とします。
- 既存の `CLAUDE.md` と `.github/copilot-instructions.md` を統合・整理しています。

## Required First Steps
- 変更前に本ファイルを読むこと。
- `git status --short --branch` で現在のブランチと作業ツリー状態を確認すること。
- ユーザーの変更を上書き・取り消ししないこと（明示的な指示がある場合を除く）。
- 編集前に適切な作業ブランチを作成・切り替えすること。
- `main` へ直接プッシュしないこと。

## リポジトリ構成
- `bakasekai/`: 主要コンテンツ（HOI4標準構造）
  - `common/`, `events/`, `history/`, `localisation/japanese/`, `gfx/`, `interface/`, `map/`
- `documents/00_coding_contexts/`: 効果・トリガー・スクリプト概念の参照資料
- `flags/00-03/`: 国旗アセットの分割保管
- `tests/`: 検証用シナリオ/デバッグ用コンテンツ

## 重要ドキュメント
- `CLAUDE.md`: AI向け全体ガイド
- `.github/copilot-instructions.md`: コーディング規約と構造
- `.github/CONTRIBUTING.md`: 開発/検証フロー
- `documents/onboarding_guide.md`: 新規参加者向け案内
- `documents/00_coding_contexts/*`: 効果/トリガー/変数の辞書

## ビルド/実行（実質の開発フロー）
- HOI4ランチャーでMODを有効化しプレイテストします。
- 依存MOD: Japanese Language mod
- バージョン: HOI4 1.13.*

## テスト/検証（単体テスト相当）
- 自動テスト/CI/リンタは基本的に存在しません。
- 単一テストは以下の手順で実施します。
  - `tests/` に検証シナリオを置く
  - コンソールで `event <event_id> <TAG>` を実行
  - 必要に応じて `reload interface` / `reload localisation`
- テスト用コンテンツは `_bsm_*_test.*` など明確に分離する
- 変更後は対象の国家/イベント/GUIに限定した最小検証を行う

## デバッグ/検証コマンド
- `tdebug`: デバッグ情報表示
- `event <event_id> <TAG>`: イベント実行
- `reload interface`: GUI反映
- `reload localisation`: ローカライズ反映（慎重に）
- `imgui show profiler`: Scriptタブで `hourly` の負荷を確認

## ファイル配置の原則
- 既存フォルダ構成を崩さない
- 新規ファイルは同系統の既存ファイルと並べる
- 既存のファイル名・IDプレフィックスに合わせる
- 目的別に小さく分割し、巨大ファイルを避ける

## コーディング規約（共通）
- インデントはスペース2個、タブ禁止
- 1行1命令（Paradox scriptの可読性維持）
- コメントは必要最低限、内容は日本語可
- 既存の並び順や構造を崩さない

## 命名規則
- 国別ファイル: 3文字タグ（例 `JPN.txt`, `USA.txt`）
- システム系: `_bsm_` 接頭辞（例 `_bsm_mine_system.txt`）
- 汎用: `generic.txt` 等のわかる名前
- GUI/Scripted: `_bsm_` + 機能名で統一
- 国旗: `flags/00-03/` で命名規則に合わせる

## イデオロギーキー（重要）
- 既存の置換キーを必ず使う
  - `communism_ideology`
  - `democratic_ideology`
  - `fascism_ideology`
  - `neutrality_ideology`

## ローカライズ規約
- 配置: `bakasekai/localisation/japanese/*.yml`
- `l_japanese:` ヘッダー必須
- エンコードは UTF-8 with BOM
- 変数表示は `[?variable_name]` を使用
- 追加キーは既存キーとの整合性を最優先
- Scripted localisation は既存の書式に合わせる
- キー名は機能・国・システム名で一意にする

## 変数フォーマット指定子（ローカライズ内 `[?var|format]`）
- **順序**: 小数桁数 → フラグ（`%`, `+`, `R`, `G`, `Y`, `H`, `W`）の順で記述する
- **有効な例**: `|0`, `|0%`, `|0+`, `|0%+`, `|0R`, `|1`, `|1%+`
- **無効・非標準（使用禁止）**: `|a0+`（`a`は無効）, `|R0`（順序逆）, `|+0`（順序逆）, `|+=%`（順序逆）
- **ツールチップ内の変数が表示されない場合**: フォーマット指定子の文字・順序を最初に疑うこと
- **スコープ**: 国変数は `[?ROOT.variable]` で参照。`ROOT` 省略はスコープ依存のため、ツールチップ等では原則 `ROOT.` を付けること
- **重複定義に注意**: 同じローカライズキーを複数 yml に定義しないこと（後読みファイルが上書きする）

## スクリプトの書式/構造
- 条件ブロックは軽い条件から先に記述
- `limit` や `trigger` のネストは最小限に保つ
- `any_state` など重いスコープは高頻度処理で避ける
- 同一効果の繰り返しはスクリプト化を検討

## 参照・再利用（imports相当）
- 既存の `scripted_effect` / `scripted_trigger` を優先再利用
- 共有処理は `_bsm_` 接頭辞で命名し再利用性を高める
- ローカライズは `scripted_localisation` を活用し重複を避ける
- 既存のキーやIDを上書きしない

## 変数・型（HOI4スクリプト）
- 変数は `set_variable`, `add_to_variable` 等の標準式で統一
- 比較は `check_variable` を使う
- 変数名は用途が明確な英語スネークケースで揃える
- スコープは明示し、`root/from` の取り違えを避ける

## エラー/検証の基本姿勢
- 仕様が曖昧な場合は既存実装に合わせる
- 変更後は必ず最小検証（イベント/国/GUI限定）
- ローカライズ欠落が起きるため追加キーは必ず確認
- 不具合があれば `tests/` の検証シナリオで再現性を確保
- テスト用変更は必ずクリーンアップ可能にする

## パフォーマンス指針
- 早期returnで軽い条件を先に書く
- 頻繁なスコープで `any_state` を避ける
- 高頻度処理はフラグ/変数でキャッシュ
- ミッション決定は重いので代替も検討

## イベント/国家方針/決定の作法
- IDは既存のプレフィックスに揃える
- トリガー・効果・説明は最小限で明確に
- オプションの結果はローカライズとセットで確認
- 検証用の決定やイベントは `_bsm_*_test` に分離

## GUI作業（OE方式タブパターン）

### 基本原則
- GUI作業は段階的に実装し、都度 `reload interface`
- 追加するGUIは `_bsm_` 系の命名を徹底
- Scripted GUIやlocalisation連携は既存実装に合わせる
- 画像差し替え時は最適化と命名統一を維持
- タイトルフォントは `hoi_24header` を使用

### タブ付きウィンドウの構造（OE方式）
このMODのタブ付きウィンドウ（OE/EA/AS）は全て以下の構造に従う：

#### 1. `.gui` ファイル構造
```
guiTypes = {
    # メインウィンドウ（top-level）
    containerWindowType {
        name = "<main_window>"
        position = { x = -420 y = -310 }
        orientation = center
        size = { width = 840 height = 620 }
        moveable = yes
        click_to_front = yes
        background { ... }
        buttonType { name = "close_button" ... }
        instantTextboxType { name = "title" font = "hoi_24header" ... }
        # タブボタン群（メインウィンドウ内）
        buttonType { name = "<tab>_button" ... }
        # その他のUI要素
    }

    # タブパネル（top-level、メインウィンドウの外に配置）
    containerWindowType {
        name = "<tab_panel_1>"
        position = { x = 15 y = 110 }   # メインウィンドウからの相対位置
        size = { width = 810 height = 498 }
        clipping = yes
        # パネル内容
    }
    containerWindowType {
        name = "<tab_panel_2>" ...
    }

    # Entry テンプレート（top-level）
    containerWindowType {
        name = "<entry_template>" ...
    }
}
```

**重要**: タブパネルは `guiTypes = { }` の直下（top-level）に配置する。
メインウィンドウの子としてネストしない。ネストすると scripted GUI が
`window_name` で該当要素を見つけられず "Undefined GUI_TYPE" エラーになる。

#### 2. Scripted GUI 構造（OE方式）
```txt
scripted_gui = {
    # メインウィンドウ制御
    <main_window>_sgui = {
        window_name = "<main_window>"
        context_type = player_context
        visible = { check_variable = { <window_open> = 1 } }
        effects = {
            # 閉じる、タブ切替、メインウィンドウ内のボタン操作
            <tab>_button_click = { set_variable = { <active_tab> = N } }
        }
        triggers = {
            # メインウィンドウ内要素の表示/有効化
        }
        dynamic_lists = {
            # メインウィンドウ内のリスト
        }
    }

    # タブパネル別の独立 scripted_gui
    <tab_panel_1>_window = {
        window_name = "<tab_panel_1>"
        context_type = player_context
        parent_window_name = <main_window>    # ★必須: 親ウィンドウを指定
        visible = {
            check_variable = { <window_open> = 1 }
            check_variable = { <active_tab> = 1 }
        }
        effects = { }      # パネル固有のボタン操作
        triggers = { }     # パネル固有の表示制御
        dynamic_lists = { } # パネル固有のリスト
    }
}
```

#### 3. `parent_window_name` の役割
- top-level に配置されたタブパネルを、メインウィンドウの子として
  画面上に配置するために使用
- これにより scripted GUI システムが該当要素を発見できる
- 指定しないと "Window not found" エラーになる

#### 4. 既存実装の参照先
- OE（Opening Event）: `interface/_bsm_opening_event.gui` + `common/scripted_guis/_bsm_opening_event.txt`
- EA（Economic Alliance）: `interface/bsm_economic_alliance.gui` + `common/scripted_guis/bsm_economic_alliance_sgui.txt`
- AS（Anomaly System）: `interface/bsm_AS.gui` + `common/scripted_guis/bsm_AS_window.txt`

### GUI固有の構文注意
- `hidden = yes` はHOI4 `.gui` では無効。表示制御は scripted GUI の `visible` で行う
- `listboxType` は存在しない。リスト表示には `gridboxType` を使用
- `gridboxType` には `add_horizontal = no` と `format = "UPPER_LEFT"` を付ける
- Entry テンプレートは `gridboxType` の外（top-level）に定義
- `verticalScrollbar` には `"right_vertical_slider"` を指定（`"right"` は不可）
- `clamp_variable` / `clamp_temp_variable` には `var =` キーが必須:
  `clamp_variable = { var = <name> min = X max = Y }`
- `set_country_flag` で期限付きフラグを設定する際は `flag =` キーが必須:
  `set_country_flag = { flag = <name> days = N }`
- `scripted_triggers` 内では effect（`set_temp_variable`等）は使用不可。
  `check_variable` は数値リテラルとの比較のみ対応（変数同士の比較は不可）

## アセット規約
- `.wav` / `.ogg` は絶対に変更しない
- 画像は最適化を意識、命名は既存に合わせる
- 国旗は `flags/00-03/` の規則に従う

## 変更時のチェックリスト
- 影響範囲が `bakasekai/` 内に収まっているか
- ローカライズの追加/更新があるか
- 既存の命名規則を逸脱していないか
- パフォーマンスに悪影響がないか

## コミット/PRの方針
- コミットは命令形 + スコープ（例 `focus: Add ...`）
- PRには次を含める
  - 変更内容の要約
  - 影響パス
  - UI変更はスクショ
  - 追加/変更ローカライズキー
  - セーブ互換性
  - パフォーマンス観測

## GitFlow

`develop` を統合ブランチとして使用する。完了した作業ブランチは `develop` にマージする（`main` には直接マージしない）。

ブランチ名は以下の形式に従う:

```text
type/scope_name
```

許可される `type` 値:
- `feature`: 新コンテンツ、システム、国家、マップ作業、テクノロジー、UI、ドキュメント
- `fix`: バグ修正、クラッシュ修正、構文修正、ローカライズ修正
- `archive`: 保存用の履史的バージョンや保全ブランチ

scope の例:
- `TAG`: 国タグ作業（`GER`, `JAP`, `USA` 等）
- `_map`: マップ、州、プロビンス、戦略地域
- `_system`: 共有システム、scripted effects、scripted triggers、GUIシステム

```text
feature/JPN_project
feature/_map_africa
feature/_system_harvest
fix/crash_JAP_event
archive/1.0
```

複数の無関係な項目を作業する場合は、項目ごとにブランチを切り替えること。

## 外部ツール/ルール
- Cursor ルール: 未検出（`.cursor/rules/`, `.cursorrules` なし）
- Copilot ルール: `.github/copilot-instructions.md` を参照

## AI-Specific Notes
- Claude は `CLAUDE.md` も読むこと。
- Gemini は `GEMINI.md` を参照（存在する場合）。
- GitHub Copilot は `.github/copilot-instructions.md` に従うこと。
- Opencode は `.opencode/AGENTS.md` に従うこと。
- Codex は本ファイルを主要なリポジトリ指示ファイルとして扱うこと。

## 参照パス（頻出）
- `documents/00_coding_contexts/01_effects/effects.json`
- `documents/00_coding_contexts/04_triggers/triggers.json`
- `documents/00_coding_contexts/00_mod_optimization.md`
- `documents/00_coding_contexts/console_commands_documentation.md`

## 注意事項
- Workshop ID `2585391890` は公開フローのみで使用
- 既存の世界観/設定を尊重し、独自解釈は最小限
- 不明点は既存ファイルを優先して調査


---

# External Agent Policy

This repository uses multiple coding agents.

## Agy / Antigravity CLI

Default role:
- read-only audit
- requirements checking
- documentation consistency
- long-context scan
- log and diff compression

Default prompt:

```text
Read the mission, CLAUDE.md, AGENTS.md, README, and relevant docs.
Do not edit files.
Return:
1. conclusion
2. hidden assumptions
3. contradictions
4. affected files
5. risks
6. recommended next action
```

Rules:
- Agy is NOT a primary implementation worker.
- If Agy must implement something, isolate it in a separate branch/worktree first.

## OpenCode(GLM)

Default role:
- secondary implementation lane
- independent patch attempt
- scoped feature work
- tests and refactors

Rules:
- Prefer separate git worktree
- Keep changes minimal
- Do not redesign unrelated systems
- Do not use `/share` (never share private repository content publicly)
- Return changed files, tests run, risks, and unresolved questions

Suggested worktree flow:

```bash
git worktree add ../PROJECT-glm -b glm/TASK_NAME
cd ../PROJECT-glm
opencode
```

## Codex

Default role:
- peer senior engineer
- rescue
- adversarial review
- independent second opinion

Use cases:
- hard bug
- design challenge
- security-sensitive review
- Claude loop recovery
- final review before risky merge

Rules:
- Do not enable an always-on review gate by default.
- Use Codex on high-risk decisions only when the extra cost is justified.

## Required final report (all external agents)

1. conclusion / approach summary
2. changed files (if any)
3. tests run and their actual output
4. risks
5. unresolved questions
