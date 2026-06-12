# アノマリーシステム（ステラリス要素）仕様書

- **対象 mod**: HOI4-Bakasekaitizu-MOD（バカ世界地図MOD）
- **prefix**: `bsm_AS_`
- **レイアウト元**: `BSM_AS.drawio`（イベント画面 / サイドUI / サイドUI_A / 探検隊）
- **作成日**: 2026-06-06
- **ステータス**: 実装済み（cwtools 構文検証・GFX欠落・loc欠落 すべてパス）。dynamic_list エントリボタンの value 読み取りのみ要 in-game 確認。

---

## 1. 概要

探検隊が世界を探索して未知の「アノマリー」を発見し、統合力（UC = `National_Unity_Power`）を投じて解析することで報酬（マーカーアイデア）を得る、ステラリス風の研究サブシステム。

- アノマリーは静的 DB（全 **327** 種）から発見される。各アノマリーは **カテゴリ / タイプ / 難易度 / 必要日数** を持つ。
- プレイヤーは **探検隊** を編成（規模 小/中/大）して派遣し、探検完了ごとに新アノマリーを発見する。
- 発見したアノマリーは **未解析 → 解析中 → 解析済み** と状態遷移する。
- UI は独立ウィンドウ（`bsm_AS_window`）＋発見ポップアップ（`bsm_AS_event_window`）。

### 状態遷移

```
[DB:327種] --探検隊が発見--> 未解析(bsm_AS_unanalyzed)
   未解析 --「解析」(UC -100)--> 解析中(bsm_AS_researching)
   解析中 --週次進行 100%到達--> 解析済み(bsm_AS_completed) + 報酬アイデア付与
   解析中 --「中止」--> 未解析
   未解析 --「放棄」--> 破棄(リストから削除)
```

---

## 2. リソースと定数

| 項目 | 値 | 備考 |
|---|---|---|
| 研究コスト | 100 UC | 解析開始時に消費（`National_Unity_Power`） |
| 探検隊 維持費 | 小=5 / 中=20 / 大=50 UC/月 | on_monthly で合計を徴収 |
| 探検隊 上限 | 3（`bsm_AS_exp_max`） | 初期値。拡張余地あり |
| 探検進行速度 | 12 + 練度×2 /週 | 100% で発見＆練度+1 |
| 研究進行速度 | (100/必要日数)×7×(1+研究ボーナス) /週 | ボーナス=`bsm_stellaris_anomaly_research_bonus` |
| カテゴリ ID | 1政治 / 2陸軍 / 3海軍 / 4空軍 / 5信仰 / 6文明 / 7経済 | DB の category |
| 難易度値 | 85朝飯前 / 80簡単 / 60日常的 / 40困難 / 25地獄 | DB の difficulty（数値が大きいほど易しい） |

---

## 3. データモデル

### 3.1 静的グローバル（全国共通・起動時1回構築）

`bsm_AS_build_lookups`（`_bsm_AS_lookup_arrays.txt`, 自動生成）が構築。index0 はダミーで **index == アノマリー番号 N**。

| 配列 | 内容 |
|---|---|
| `global.AS_AN_days_by_id^N` | 必要日数 |
| `global.AS_AN_cat_by_id^N` | カテゴリ(1–7) |
| `global.AS_AN_diff_by_id^N` | 難易度(25/40/60/80/85) |
| `global.AS_AN_total` | アノマリー総数（327） |

> 既存の `global.AS_AN_database_id_N`（token/cat/type/diff/days の並列配列, `_bsm_anomaly_system.txt`）を参照元として、loc で扱いやすいフラット配列へ正規化したもの。

### 3.2 アノマリー在庫（per-country, 値 = N）

| 配列 | 内容 |
|---|---|
| `bsm_AS_unanalyzed` | 未解析（発見済・未研究） |
| `bsm_AS_researching` | 解析中 |
| `bsm_AS_completed` | 解析済み |
| `bsm_AS_prog_by_n^N` | 解析進捗 0–100（遅延初期化: `bsm_AS_ensure_prog_array`） |
| `bsm_AS_discover_cursor` | 次の発見探索の開始位置 |

> legacy の `AN_*_list`（スカラ/配列が混在し衝突）は使わず、専用配列で独立管理する。

### 3.3 探検隊（per-country, indexed-variable 方式）

primary 配列 `bsm_AS_exp_ids`（現役チームIDの一覧）。各チームのデータは ID をサフィックスに持つ indexed-variable。

| 変数 | 内容 |
|---|---|
| `bsm_AS_exp_ids` | 現役チームIDの配列 |
| `bsm_AS_exp_next_id` | 次に発行するID |
| `bsm_AS_exp_max` | 稼働可能上限 N |
| `bsm_AS_exp_upkeep` | 月額維持費合計（逐次増減） |
| `bsm_AS_exp_count` | 稼働中数（GUI表示用、再構築時に更新） |
| `bsm_AS_exp_size_@var:ID` | 規模 1=小/2=中/3=大 |
| `bsm_AS_exp_level_@var:ID` | 練度 |
| `bsm_AS_exp_status_@var:ID` | 0=待機/1=探検中/2=解析支援中 |
| `bsm_AS_exp_target_@var:ID` | 対象（0=なし） |
| `bsm_AS_exp_icon_@var:ID` | アイコンID |
| `bsm_AS_exp_prog_@var:ID` | 探検進捗 0–100 |

#### 表示用 位置配列（`bsm_AS_rebuild_team_display` が変更毎に再構築）

dynamic_list の `index = as_team_idx` で loc から `^as_team_idx` 参照するため、`bsm_AS_exp_ids` の並び順に対応した固定名配列を複製する。

`bsm_AS_team_id_arr` / `bsm_AS_team_size_arr` / `bsm_AS_team_lv_arr` / `bsm_AS_team_status_arr` / `bsm_AS_team_prog_arr` / `bsm_AS_team_icon_arr`

### 3.4 UI 状態変数（per-country）

| 変数 | 内容 |
|---|---|
| `bsm_AS_window_open` | メインウィンドウ表示(0/1) |
| `bsm_AS_active_tab` | 1未解析/2解析中/3解析済み/4探検隊 |
| `bsm_AS_form_open` | 編成ダイアログ表示(0/1) |
| `bsm_AS_form_size` | 編成する規模 |
| `bsm_AS_event_open` | 発見ポップアップ表示(0/1) |
| `bsm_AS_event_anomaly` | ポップアップ対象のアノマリーN |
| `bsm_AS_cur` / `bsm_AS_cur_anomaly` | ループ/GUI操作で動的サフィックスに使う作業変数 |

---

## 4. ファイル構成

| 種別 | パス | 役割 |
|---|---|---|
| Effects | `common/scripted_effects/_bsm_AS_expedition.txt` | 本体ロジック（init/編成/解体/派遣/維持費/探検tick/発見/研究） |
| Effects(生成) | `common/scripted_effects/_bsm_AS_reward_grant.txt` | `bsm_AS_grant_reward`（N→アイデア付与、327分岐） |
| Effects(生成) | `common/scripted_effects/_bsm_AS_lookup_arrays.txt` | `bsm_AS_build_lookups`（フラット参照配列） |
| Scripted GUI | `common/scripted_guis/bsm_AS_window.txt` | メインウィンドウ（タブ/dynamic_lists/effects/triggers） |
| Scripted GUI | `common/scripted_guis/bsm_AS_event.txt` | 発見ポップアップ（3アクション/画像可視性） |
| Scripted loc | `common/scripted_localisation/bsm_AS_names_scripted_loc.txt` | `GetASAnomalyName`/`GetASEventName`（327分岐, 生成） |
| Scripted loc | `common/scripted_localisation/bsm_AS_scripted_loc.txt` | カテゴリ/難易度/規模/状態 ラベル |
| GUI | `interface/bsm_AS.gui` | メインウィンドウ＋エントリ container |
| GUI | `interface/bsm_AS_event.gui` | 発見ポップアップ |
| GFX | `interface/bsm_AS.gfx` | カテゴリー別4:3画像（プレースホルダ） |
| loc | `localisation/japanese/bakasekai/bsm_AS_l_japanese.yml` | UI/バッジ/イベント文言 |
| 画像一覧 | `documents/00_coding_contexts/bsm_AS_image_assets.md` | 未作成画像の差し替えガイド |

### 変更した既存ファイル

| パス | 変更 |
|---|---|
| `common/on_actions/_bsm_system.txt` | on_startup `bsm_AS_init` / on_monthly `bsm_AS_monthly_upkeep` / on_weekly `bsm_AS_weekly_tick` を追加 |
| `common/scripted_guis/bsm_stellaris.txt` | アノマリータブclick→`bsm_AS_window_open=1`、旧tab6 triggers 撤去 |
| `interface/bsm_stellaris.gui` | 旧tab6 placeholder textbox 撤去 |

---

## 5. 主要エフェクト API

| エフェクト | 引数（事前set） | 効果 |
|---|---|---|
| `bsm_AS_init` | — | per-country 初期化＋lookups 1回構築（on_startup） |
| `bsm_AS_form_team` | `bsm_AS_form_size`,`bsm_AS_form_icon` | チーム追加（上限/維持費更新） |
| `bsm_AS_disband_team` | `bsm_AS_cur`=ID | チーム解体（維持費減算） |
| `bsm_AS_dispatch_team` | `bsm_AS_cur`=ID | 待機→探検中 |
| `bsm_AS_recall_team` | `bsm_AS_cur`=ID | 探検中→待機 |
| `bsm_AS_monthly_upkeep` | — | UC 維持費徴収（on_monthly） |
| `bsm_AS_weekly_tick` | — | 探検tick＋研究weekly（on_weekly） |
| `bsm_AS_discover_anomaly` | — | 未所持アノマリーを1件発見→未解析へ＋ポップアップ |
| `bsm_AS_research_start` | `bsm_AS_cur_anomaly`=N | 未解析→解析中（UC -100） |
| `bsm_AS_research_cancel` | `bsm_AS_cur_anomaly`=N | 解析中→未解析 |
| `bsm_AS_grant_reward` | `bsm_AS_cur_anomaly`=N | マーカーアイデア `AS_AN_<token>` 付与 |
| `bsm_AS_event_discard` | — | ポップアップ対象を破棄して閉じる |
| `bsm_AS_event_analyze` | — | ポップアップ対象の解析開始して閉じる |

---

## 6. GUI 仕様

### 6.1 メインウィンドウ `bsm_AS_window`

- 500×580、右側オフセット表示、moveable。背景 `GFX_tiled_window2_1b_border`。
- ヘッダ: タイトル「アノマリー」＋close。
- タブ4種（未解析/解析中/解析済み/探検隊）。`bsm_AS_active_tab` で対応パネルを可視切替。
- 一覧パネル×3: gridbox に各在庫配列を bind（`value=as_val`, `index=as_idx`、エントリ container 共用 `bsm_AS_anomaly_entry`）。
  - エントリ右側ボタンは **メンバーシップ trigger** で切替: 未解析=[解析] / 解析中=進捗%＋[中止] / 解析済み=[完了]。
- 探検隊パネル: [編成]ボタン・稼働数・維持費・チーム一覧（`bsm_AS_team_id_arr`, `value=as_team_id`, `index=as_team_idx`）。
  - チームの状態で[派遣]/[呼戻し]を可視切替、[解体]は常時。
- 編成ダイアログ `bsm_AS_form_dialog`（`bsm_AS_form_open` で表示）: 小/中/大ボタンで即編成。

### 6.2 発見ポップアップ `bsm_AS_event_window`

- 520×420。カテゴリー別4:3画像（7枚を `global.AS_AN_cat_by_id^bsm_AS_event_anomaly` の可視性で1枚表示）。
- 名前 `[GetASEventName]`、説明、カテゴリ/難易度/日数バッジ。
- アクション: 放棄しよう(`bsm_AS_event_discard`) / 放っておけ(閉じる) / 解析しろ(`bsm_AS_event_analyze`)。

---

## 7. ローカライズの要点（重要な技術制約）

- loc の `[?...]` 内では `@var:` 動的連結が**使えない**。数値は **固定名配列 ^ 変数index** のみ表示可（mine システム流）。
  - 日数 `[?global.AS_AN_days_by_id^as_val|0]日`、進捗 `[?bsm_AS_prog_by_n^as_val|0]%`、練度 `[?bsm_AS_team_lv_arr^as_team_idx|0]`。
- アノマリー**名**と**報酬アイデア**は整数 N から直接引けないため、`AS_AN_alias`（327件）から `python` で **生成**（`GetASAnomalyName`/`GetASEventName`/`bsm_AS_grant_reward`）。
- scripted_loc は dynamic_list の `value`/`index` 変数を直接参照（例: `check_variable = { as_val = N }`）。

---

## 8. パフォーマンス配慮

- `bsm_AS_build_lookups` は global flag で **起動時1回のみ**（全国一括ループを回避。`anomaly_on_startup_hang` の教訓）。
- `bsm_AS_prog_by_n` は研究を行う国でのみ **遅延初期化**。
- on_weekly/on_monthly のチーム/研究ループは `^num > 0` で早期 return（探検隊・研究を持たない AI は即抜け）。

---

## 9. 既知の制約・拡張余地

- **要 in-game 確認**: dynamic_list（`change_scope=no`）エントリ内ボタンの effect が `value`(as_val/as_team_id) を読めること（EAパターン上は可）。
- 1回の週次 tick で複数発見が起きた場合、ポップアップは最後の1件のみ表示（他は未解析に残る）。
- 画像は**カテゴリー別プレースホルダ**（全カテゴリ同一の仮画像）。差し替えは `bsm_AS_image_assets.md` 参照。
- 「解析支援」派遣（drawio の研究支援/政治支援サブパネル）は未実装。status=2 の枠は確保済み。
- 探検隊の「アイコン選択」「名前入力」は簡略化（規模選択のみ）。研究者「顔」「特性」枠は未実装。
- 報酬はマーカーアイデアの付与のみ。固有効果は各 `AS_AN_<token>` アイデア定義側で拡張する。

---

## 10. テスト手順（in-game）

1. topbar → ステラリス → アノマリータブ → 独立ウィンドウ起動。
2. 探検隊タブで [編成]→小/中/大 → 稼働数(M/N)・維持費が更新されること。
3. チームを [派遣] → 週送りで進行 → 100% で **発見ポップアップ** 出現。
4. ポップアップ [解析しろ] → 解析中タブへ移動、UC -100。
5. 週送りで進捗% 上昇 → 100% で解析済みタブへ移動・アイデア付与。
6. 月送りで UC 維持費が引かれること。
7. `imgui show profiler` で on_weekly/on_monthly の負荷確認。
