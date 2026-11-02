# 03 開発ガイド

現行のルールの正本は [AGENTS.md](../../AGENTS.md) である。このページは変更作業の流れに沿って要点を示す。詳しい手順は [.github/CONTRIBUTING.md](../../.github/CONTRIBUTING.md) にあるが、対応ゲーム版など古い記述が残っている（[90-known-discrepancies](90-known-discrepancies.md)）。

## ローカル環境

1. リポジトリをcloneし、`bakasekai/` をHOI4のmodディレクトリへコピーまたはシンボリックリンクする（[CONTRIBUTING.md:14](../../.github/CONTRIBUTING.md#L14)）。
2. ランチャーでBSMと依存MOD「Japanese Language mod」を有効にする（[descriptor.mod:66](../../bakasekai/descriptor.mod#L66)）。

## ブランチとコミット

- 編集前に `git status --short --branch` で他者の変更を確認する（[AGENTS.md:7](../../AGENTS.md#L7)）。
- 新規ブランチは `feature` / `fix` / `archive` を使った `type/scope_name` 形式にする（[AGENTS.md:8](../../AGENTS.md#L8)）。
- 統合先は `develop`。`main` へ直接pushしない（[AGENTS.md:7](../../AGENTS.md#L7)）。
- コミットメッセージには `focus:`, `events:`, `localisation:`, `perf:` などのスコープを付ける（[CONTRIBUTING.md:75](../../.github/CONTRIBUTING.md#L75)）。
- PRには影響パス、UI変更の画像、localisationキーの増減、セーブ互換性、性能値を記載する（[CONTRIBUTING.md:78](../../.github/CONTRIBUTING.md#L78)）。

## 変更してはいけないもの

- `.wav` / `.ogg` は変更しない（[AGENTS.md:9](../../AGENTS.md#L9)）。
- map、CSV、バイナリ、実セーブの削除や破壊的な置換は、対象と復元方法を明確にして承認を得る（[AGENTS.md:9](../../AGENTS.md#L9)）。
- 既存の世界観、架空データ、国タグ、ID、命名を保持する（[AGENTS.md:3](../../AGENTS.md#L3)）。
- Workshop ID `2585391890` は公開フローだけで使う（[AGENTS.md:10](../../AGENTS.md#L10)）。

## スクリプトの規約

| 項目 | 規則 | 出典 |
|---|---|---|
| 書式 | 2スペース、1行1命令 | [AGENTS.md:15](../../AGENTS.md#L15) |
| localisation | `localisation/japanese/*.yml`、UTF-8 BOM付き、`l_japanese:`。同じキーを別ファイルに重複定義しない | [AGENTS.md:17](../../AGENTS.md#L17) |
| 変数format | 小数桁数の次にflagを書く（`\|0%+`）。`\|a0+`, `\|R0`, `\|+0`, `\|+=%` は使わない | [AGENTS.md:18](../../AGENTS.md#L18) |
| tooltipの国変数 | スコープを確認し、原則 `[?ROOT.variable]` | [AGENTS.md:18](../../AGENTS.md#L18) |
| 性能 | 高頻度のtriggerに広い `any_state` を増やさない。既存のeffect/triggerを再利用する | [AGENTS.md:19](../../AGENTS.md#L19) |
| GUI配置 | OE/EA/AS型のtab panelとentry templateは `guiTypes` 直下。tabの独立scripted GUIで `parent_window_name` を指定する | [AGENTS.md:20](../../AGENTS.md#L20) |
| GUI部品 | `hidden = yes` と `listboxType` を使わず、`visible` と `gridboxType` を使う | [AGENTS.md:21](../../AGENTS.md#L21) |
| effect構文 | `clamp_variable` の `var =`、期限付き `set_country_flag` の `flag =` を省略しない。trigger内にeffectを置かない | [AGENTS.md:22](../../AGENTS.md#L22) |

## 参照資料

| 調べたいもの | 資料 |
|---|---|
| effect | [documents/01_effects/effects.json](../01_effects/effects.json) |
| trigger | [documents/04_triggers/triggers.json](../04_triggers/triggers.json) |
| scope | [documents/02_scopes/hoi4_scopes.json](../02_scopes/hoi4_scopes.json) |
| 高頻度処理と最適化 | [documents/00_coding_contexts/00_mod_optimization.md](../00_coding_contexts/00_mod_optimization.md) |

## 検証

静的検証と実ゲーム確認は別のものとして報告する（[AGENTS.md:37](../../AGENTS.md#L37)）。

```bash
python3 tools/validate_mod.py bakasekai
```

```bash
python3 tools/loc_coverage.py bakasekai
```

実ゲームでは次のコンソールコマンドを使う（[AGENTS.md:36](../../AGENTS.md#L36)）。

| コマンド | 用途 |
|---|---|
| `event <id> <TAG>` | イベントを発火する |
| `reload interface` | GUIを再読込する |
| `reload localisation` | テキストを再読込する |
| `imgui show profiler` | Script/hourlyの負荷を確認する |

テストやデバッグ用の内容は `_bsm_*_test` などで識別できる名前にし、復元可能にする（[AGENTS.md:37](../../AGENTS.md#L37)）。CIの内容と現在の検証結果は [14-gui-tooling-ci](14-gui-tooling-ci.md) を参照。

## 関連ページ

- [01-overview](01-overview.md)
- [02-architecture](02-architecture.md)
- [14-gui-tooling-ci](14-gui-tooling-ci.md)
