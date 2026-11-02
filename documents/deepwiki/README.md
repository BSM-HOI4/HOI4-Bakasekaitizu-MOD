# バカ世界地図MOD DeepWiki

バカ世界地図MOD（BSM）の構造と実装を、ソースへの行番号付きリンクで説明する開発者向けWikiである。ルールの正本は [AGENTS.md](../../AGENTS.md) で、このWikiはコードを読むための案内として使う。

## 基準とする状態

- 基準コミット: `c187c6bbb`（ブランチ `feature/london_three_sovereignties`）に、2026-11-02時点の未コミット変更を加えた作業ツリー。`origin/develop` より18コミット遅れ、2コミット進んでいる。
- ロンドン、フランス、スペイン、北センチネルのシナリオとWin95テーマの一部は未コミットの内容を含み、`develop` には存在しない場合がある。
- 行番号はこの時点のものである。ファイルの編集でずれるので、古くなっていたら識別子で検索する。
- 記述はコードの静的な読解、集計、検証ツールの実行に基づく。今回ゲームは起動していない。確認できなかったものは各ページに「未確認」と記載している。

## ページ

| ページ | 内容 |
|---|---|
| [01-overview](01-overview.md) | 基本情報、リポジトリ構成、規模 |
| [02-architecture](02-architecture.md) | バニラとの関係、実行モデル、on_action、命名規則 |
| [03-development-guide](03-development-guide.md) | ブランチ、変更の制約、スクリプト規約、検証手順 |
| [10-civilization-and-resources](10-civilization-and-resources.md) | 文明度、統合力、統一通貨、国家通貨、ステラリス要素、堕ちた帝国、経済同盟、自治度 |
| [11-gameplay-systems](11-gameplay-systems.md) | on_actionの全体像、元首ガチャ、スーパーイベント、鉱山、傭兵、請求権捏造、核、ATRMRW |
| [12-countries-and-scenarios](12-countries-and-scenarios.md) | 国タグ、国家データ、国家方針、シナリオの実装状況、イベント |
| [13-map-assets-localisation](13-map-assets-localisation.md) | マップの実数、アセット、翻訳カバレッジ、`replace_path` |
| [14-gui-tooling-ci](14-gui-tooling-ci.md) | GUI構造、Win95生成パイプライン、検証ツール、CI、スクリプト |
| [90-known-discrepancies](90-known-discrepancies.md) | 文書と実装の差異、不整合の候補、未解決の問い |

## 目的別の入口

| やりたいこと | 読むページ |
|---|---|
| 全体像をつかむ | [01-overview](01-overview.md) → [02-architecture](02-architecture.md) |
| 新しいシステムを追加する | [02-architecture](02-architecture.md) → [11-gameplay-systems](11-gameplay-systems.md) の on_action 全体像 |
| 国やシナリオを追加する | [12-countries-and-scenarios](12-countries-and-scenarios.md) |
| GUIを変更する | [14-gui-tooling-ci](14-gui-tooling-ci.md)。Win95生成物は生成元を編集する |
| 既存文書が正しいか確かめる | [90-known-discrepancies](90-known-discrepancies.md) |

## 更新方法

ページはMarkdownで、DeepWikiのサービスには依存しない。コードを変更して記述が古くなったら該当ページを直接編集する。引用はファイル名と行番号を表示名にし、リンク先に相対パスと `#L行` を指定する。
