# HOI4-Bakasekaitizu-MOD — エージェント指示

本体は `bakasekai/`。既存の世界観、架空データ、国タグ、ID、命名を保持する。ゲーム対応版は現在のdescriptorと実環境を確認する。

## 作業・公開境界

- 編集前に `git status --short --branch` を確認し、他者の変更を保護する。適切な作業branchがあればそのまま使う。統合先は `develop`、`main`へ直接pushしない。
- 新規branchは `type/scope_name`（type: `feature` / `fix` / `archive`）。無関係な作業はbranchを分ける。commit／merge／pushは明示された依頼範囲だけ行う。
- `.wav` / `.ogg` は変更しない。map／CSV／binary／実セーブの削除・破壊的な置換は事前に対象と復元方法を明確にし、承認を得る。
- Workshop ID `2585391890` は公開フローのみで使う。外部公開・production操作・課金・secrets／権限変更は明示された対象と範囲の承認が必要。
- 依頼範囲のローカル編集、fixture・静的検証、変更起因の失敗修正と再検証は自律的に続行する。

## 保護するproject制約

- Paradox scriptは2 spaces、1行1命令。同系統の配置・IDを踏襲し、systemは `_bsm_`、国別は既存3文字tagを使う。
- ideology keyは `communism_ideology` / `democratic_ideology` / `fascism_ideology` / `neutrality_ideology`。vanilla keyへ無断で戻さない。
- 日本語localisationは `bakasekai/localisation/japanese/*.yml`、UTF-8 with BOM、`l_japanese:`。可視要素と同時に更新し、既存名・説明・キーを失わない。
- 変数formatは小数桁数→flagの順（例 `|0%+`）。`|a0+`、`|R0`、`|+0`、`|+=%` を使わない。tooltipで国変数を参照する場合はscopeを確認し、原則 `[?ROOT.variable]` とする。同じlocalisation keyを別ymlへ重複定義しない。
- 頻繁に動くtriggerで広い `any_state` scanを増やさず、既存scripted effect／triggerを再利用する。scopeのROOT/FROMを取り違えない。
- OE／EA／AS型tab panelとentry templateは `.gui` の `guiTypes` 直下に置く。main window内にネストしない。tabの独立scripted GUIで `parent_window_name` を指定する。
- GUIでは `hidden = yes` / `listboxType` を使わず、scripted GUIの `visible` / `gridboxType` を使う。gridには `add_horizontal = no` と `format = "UPPER_LEFT"`、scrollbarには `"right_vertical_slider"`、titleには `hoi_24header`。
- `clamp_variable` / `clamp_temp_variable` の `var =`、期限付き `set_country_flag` の `flag =` を省略しない。trigger内へeffectを置かない。変数比較や追加syntaxの可否は該当辞書と現行実装を照合する。

## 必要なときだけ読む

| 作業領域 | 参照先 |
|---|---|
| effect／trigger | [effects辞書](documents/01_effects/effects.json)、[triggers辞書](documents/04_triggers/triggers.json) |
| scope | [scope辞書](documents/02_scopes/hoi4_scopes.json) |
| 高頻度処理・性能 | [最適化資料](documents/00_coding_contexts/00_mod_optimization.md) |
| OE型GUI構造・scripted GUIの注意 | [旧ガイド](.agent-context/legacy/AGENTS-before-2026-09-05.md) の「GUI作業」「GUI固有の構文注意」と既存OE／EA／AS実装 |
| contribution・運用 | [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) |

## 検証と報告

対象国家／イベント／GUIに限定して、構文・ID参照・localisationを検証する。実ゲームでは必要に応じて `event <id> <TAG>`、`reload interface`、`reload localisation` を使う。性能変更は `imgui show profiler` のScript/hourlyを確認する。
静的検証と実ゲーム確認を区別し、実行した検証、変更起因の問題、未確認を報告する。UI変更の画像・save互換性・性能値は関連する場合だけ添える。test/debug contentは `_bsm_*_test` などで識別し、復元可能にする。

旧ガイドは履歴として原文を保全している。固定ゲーム版・CI不存在という過去snapshot・モデル別役割・全資料先読みは現行指示ではない。通常作業で旧ガイド全文を読む必要はない。
