# 90 既知の差異と未解決の問い

Wiki作成時の調査で見つかった、文書と実装の差異、実装内の不整合の候補、未解決の問いをまとめる。いずれも静的な読解の結果で、ゲーム内の症状は確認していない。修正はしていない。

## 最優先で確認する問い

### on_daily / on_weekly / on_monthly は国ごとに発火するか

この問いの答えによって、性能と数値の評価が大きく変わる。

- 設計文書は「全体で1回」と断定している（[bsm_economic_alliance_v2_documentation.md:206](../00_coding_contexts/bsm_economic_alliance_v2_documentation.md#L206)）。
- `_bsm_system.txt` の週次処理は `every_country` を内包しており（[_bsm_system.txt:452](../../bakasekai/common/on_actions/_bsm_system.txt#L452)）、全体で1回の前提で書かれている。
- 一方、同じ on_monthly から呼ぶ `ucs_on_monthly` は国スコープを前提に書かれている（[_bsm_Unified_Currency.txt:372](../../bakasekai/common/scripted_effects/_bsm_Unified_Currency.txt#L372)）。
- バニラのDLC用 on_action も国スコープの条件を直接書いている（詳細は [11-gameplay-systems](11-gameplay-systems.md) の1章）。

国ごとに発火する場合、`every_country` を内包する処理は国数の2乗で動き、文明度や統合力の加算も国数倍になる。全体で1回の場合は、国スコープ前提の処理のスコープが問題になる。実機で `log` を入れて発火回数とROOTを確かめるのが確実である。

## 文書と実装の差異

| 項目 | 文書の記述 | 実装 | 詳細 |
|---|---|---|---|
| 対応ゲーム版 | `1.13.*`（[CONTRIBUTING.md:8](../../.github/CONTRIBUTING.md#L8), [copilot-instructions.md:29](../../.github/copilot-instructions.md#L29)） | `1.19.*`（[descriptor.mod:69](../../bakasekai/descriptor.mod#L69)） | [14](14-gui-tooling-ci.md) |
| Workshop ID | `2926389173`（[README.md:44](../../README.md#L44)） | `2585391890`（[descriptor.mod:70](../../bakasekai/descriptor.mod#L70), [AGENTS.md:10](../../AGENTS.md#L10)）。別ページの可能性があり、どちらが正かは未確認 | - |
| `CLAUDE.md` | 開発ガイドとして参照（[CONTRIBUTING.md:95](../../.github/CONTRIBUTING.md#L95)） | 追跡済みのシンボリックリンクが自分自身を指しており読めない | [14](14-gui-tooling-ci.md) |
| 文明度の尺度 | 0〜100%（[civilization_degree_system.md](../civilization_degree_system.md)） | 0〜1の小数を `\|0%` で表示（[bsm_system_l_japanese.yml:8](../../bakasekai/localisation/japanese/bakasekai/bsm_system_l_japanese.yml#L8)） | [10](10-civilization-and-resources.md) |
| 統一通貨の更新頻度 | 日次（[README_systems.md:80](../README_systems.md#L80)） | 獲得は月次。日次は補正計算 | [10](10-civilization-and-resources.md) |
| 経済同盟の仕様 | 旧v1の記述（[economic_alliance_spec.md](../economic_alliance_spec.md)） | 現行はv2 | [10](10-civilization-and-resources.md) |
| シナリオ文書の冒頭 | ESP、FRA、NTS は「未作成」の記述 | いずれも実装あり | [12](12-countries-and-scenarios.md) |
| `tests/` | 検証シナリオ置き場（[onboarding_guide.md:11](../onboarding_guide.md#L11)） | 実体は `bakasekai/tests/` で、ゲームが実行する自動テスト | [14](14-gui-tooling-ci.md) |
| Win95スプライト数 | 文書の最新値は258 | 作業ツリーは351。対応する文書がない | [14](14-gui-tooling-ci.md) |

## 実装内の不整合の候補

| 内容 | 根拠 | 想定される影響 |
|---|---|---|
| `Cultural_Degree` の尺度が混在する。主要な式は0〜1前提、特性スロットは30以上を要求 | [_bsm_Unified_Currency.txt:34](../../bakasekai/common/scripted_effects/_bsm_Unified_Currency.txt#L34), [_bsm_stellaris_effects.txt:64](../../bakasekai/common/scripted_effects/_bsm_stellaris_effects.txt#L64) | 特性スロットが通常のプレイで解放されない |
| スーパーイベントが立てるフラグと表示側の判定が異なる。`NO_Economy` と `MAC_NO_Economy` | [BAKA_SuperEvents.txt:224](../../bakasekai/events/BAKA_SuperEvents.txt#L224), [Super_Event_Scripted_Loc.txt:49](../../bakasekai/common/scripted_localisation/Super_Event_Scripted_Loc.txt#L49) | タイトルや本文が表示されない可能性 |
| `economic_alliance_count` に代入する処理がない | `common/`, `events/`, `interface/` をgrepして読み取りのみ（[_bsm_Unified_Currency.txt:112](../../bakasekai/common/scripted_effects/_bsm_Unified_Currency.txt#L112)） | 同盟数ボーナスが常に効かない |
| `mercenary_system_init` の呼び出し元がない | [_bsm_mercenary.txt:43](../../bakasekai/common/scripted_effects/_bsm_mercenary.txt#L43) | 未使用コードの可能性 |
| `215-Namibia.txt` の名前が `STRATEGICREGION_228` で、`STRATEGICREGION_215` が参照されない | [215-Namibia.txt:4](../../bakasekai/map/strategicregions/215-Namibia.txt#L4) | リージョン名の表示誤り |
| `tools/atrmrw/` は `__pycache__` だけが残る | 追跡ファイル0件。ソースは `feature/_system_ATRMRW_naval_design` のみ | 現ブランチでは使えない |

## 検証の現状

2026-11-02に作業ツリーで実行した結果である。

| コマンド | 結果 |
|---|---|
| `python3 tools/validate_mod.py bakasekai` | PASSED。0 errors、139 warnings |
| `python3 tools/loc_coverage.py bakasekai` | 英語カバレッジ33.6%（5,985 / 17,839キー） |

## ページごとの未確認事項

- [10-civilization-and-resources](10-civilization-and-resources.md) の「未確認」
- [11-gameplay-systems](11-gameplay-systems.md) の15章
- [12-countries-and-scenarios](12-countries-and-scenarios.md) の5章
- [13-map-assets-localisation](13-map-assets-localisation.md) の5章
- [14-gui-tooling-ci](14-gui-tooling-ci.md) の7章

## 関連ページ

- [README](README.md)
- [03-development-guide](03-development-guide.md)
