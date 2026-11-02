# 01 プロジェクト概要

バカ世界地図MOD（BSM）は、Chakuwikiの共同創作「バカ世界地図」をHearts of Iron IV上で再現するトータルコンバージョンMODである（[README.md:10](../../README.md#L10)）。ゲームに読み込まれる本体は `bakasekai/` で、リポジトリの残りは開発資料とツールが占める（[AGENTS.md:3](../../AGENTS.md#L3)）。

## 基本情報

| 項目 | 値 | 出典 |
|---|---|---|
| MOD名 | バカ世界地図テスト版 | [descriptor.mod:65](../../bakasekai/descriptor.mod#L65) |
| バージョン表記 | Alpha 0.1 | [descriptor.mod:1](../../bakasekai/descriptor.mod#L1) |
| 対応ゲーム版 | `1.19.*` | [descriptor.mod:69](../../bakasekai/descriptor.mod#L69) |
| 依存MOD | Japanese Language mod | [descriptor.mod:66](../../bakasekai/descriptor.mod#L66) |
| Workshop ID（公開設定） | `2585391890` | [descriptor.mod:70](../../bakasekai/descriptor.mod#L70) |
| 既定ブックマーク | 1936年1月1日、既定国 `BTL` | [the_gathering_storm.txt:5](../../bakasekai/common/bookmarks/the_gathering_storm.txt#L5) |
| 統合先ブランチ | `develop`。`main` へ直接pushしない | [AGENTS.md:7](../../AGENTS.md#L7) |
| GitHub | `BSM-HOI4/HOI4-Bakasekaitizu-MOD`（公開） | `git remote -v` |

一部の開発文書は対応版を `1.13.*` と記載しており、descriptorと食い違う。一覧は [90-known-discrepancies](90-known-discrepancies.md) を参照。

## リポジトリ構成

| パス | 役割 |
|---|---|
| `bakasekai/` | MOD本体。この下がゲームに読み込まれる |
| `documents/` | 開発資料。システム仕様、シナリオ設計、辞書（`01_effects/`, `02_scopes/`, `04_triggers/`）、Win95 UI作業記録 |
| `tools/` | 静的検証（`validate_mod.py`, `verify_*.py`）とWin95 GUI生成器。[14-gui-tooling-ci](14-gui-tooling-ci.md) |
| `scripts/` | 分析・一括修正用のPythonスクリプト |
| `flags/` | 国旗画像のシャード置き場 |
| `.github/` | CI（`validate-mod.yml`, `cwtools.yml`）、Issue・PRテンプレート、CONTRIBUTING |
| `.claude/skills/`, `codex/skills/` | エージェント向けのHOI4作業スキル |
| `.agent-context/legacy/` | 2026-09-05以前のエージェント指示。履歴として保全（[AGENTS.md:39](../../AGENTS.md#L39)） |

## `bakasekai/` の規模

作業ツリーの実ファイルを `find` と `du` で集計した値である。

| パス | ファイル数 | 容量 |
|---|---:|---:|
| `gfx/` | 12,650 | 1.5G |
| `music/` | 95 | 398M |
| `map/` | 310 | 180M |
| `sound/` | 31 | 20M |
| `interface/` | 280 | 8.5M |
| `history/states/` | 1,112 | 4.3M |
| `localisation/japanese/` | 193 | 2.4M |
| `history/countries/` | 353 | 1.5M |
| `history/units/` | 229 | 1.3M |
| `events/` | 142 | 1.2M |
| `localisation/english/` | 82 | 660K |

`common/` の主なファイル数は `units` 267、`ideas` 259、`characters` 224、`decisions` 144、`scripted_effects` 122、`autonomous_states` 82、`national_focus` 73 である。国タグの定義は `common/country_tags/` の5ファイル合計466件で、うち動的タグの扱いは [12-countries-and-scenarios](12-countries-and-scenarios.md) で説明する。

## 開発の経緯

`HEAD` までのコミットは1,769件、最古は2021-09-18である。現在のremoteとリリースページは `BSM-HOI4` にある（[README.md:56](../../README.md#L56)）。

## このWikiの読み方

- 全体の構造と読み込みの仕組み: [02-architecture](02-architecture.md)
- 変更するときのルールと検証: [03-development-guide](03-development-guide.md)
- システム別の詳細: [10-civilization-and-resources](10-civilization-and-resources.md), [11-gameplay-systems](11-gameplay-systems.md)
- 国家とシナリオ: [12-countries-and-scenarios](12-countries-and-scenarios.md)
- マップ、アセット、翻訳: [13-map-assets-localisation](13-map-assets-localisation.md)
- GUI、ツール、CI: [14-gui-tooling-ci](14-gui-tooling-ci.md)

## 関連ページ

- [README](README.md)
- [02-architecture](02-architecture.md)
