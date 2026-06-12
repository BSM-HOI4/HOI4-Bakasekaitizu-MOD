# 経済同盟システム v2 — コーダー向け包括ドキュメント

バカ世界地図MOD の経済同盟（Economic Alliance / EA）システム v2 の全体設計・データ構造・拡張方法をまとめる。
ブランチ: `feature/economic_alliance_v2`（`develop` ベース）。

---

## 1. 概要

各国は「経済同盟（陣営／sphere）」に加盟できる。盟主（leader）を中心に、加盟国は影響力に応じた**議席**を持ち、**全体方針（互恵／搾取）**・**役職（議長／外交担当）**・**同盟目標**・**投資/援助アクション**を通じて相互作用する。既存の統一通貨（Unified Currency, UC）システムと密結合している。

GUI は4タブ構成のフローティングウィンドウ（840×620）。AI は scripted_gui ボタンを押せないため、月次の専用 effect で駆動される。

---

## 2. ファイル構成

| 役割 | パス |
|---|---|
| GUI レイアウト | `bakasekai/interface/bsm_economic_alliance.gui` |
| GUI 配線（ボタン/可視性/動的リスト） | `bakasekai/common/scripted_guis/bsm_economic_alliance_sgui.txt` |
| 結成/加盟/離脱/誘致 ディシジョン | `bakasekai/common/decisions/bsm_economic_alliance_decisions.txt` |
| 陣営コア（作成/加盟/離脱/トークン/ソート） | `bakasekai/common/scripted_effects/bsm_ea_system_effects.txt` |
| 影響力・議席・バフ計算 | `bakasekai/common/scripted_effects/bsm_economic_alliance_calculations.txt` |
| 目標/投票/月次更新/クールダウン | `bakasekai/common/scripted_effects/bsm_ea_goals_effects.txt` |
| GUI データ更新 | `bakasekai/common/scripted_effects/bsm_economic_alliance_gui_effects.txt` |
| ビュー切替（次/前陣営） | `bakasekai/common/scripted_effects/bsm_ea_gui_interaction_effects.txt` |
| 投資/援助アクション（6種） | `bakasekai/common/scripted_effects/bsm_ea_action_effects.txt` |
| 役職（議長/外交担当） | `bakasekai/common/scripted_effects/bsm_ea_officials_effects.txt` |
| 全体方針（互恵/搾取）+UC徴収 | `bakasekai/common/scripted_effects/bsm_ea_policy_effects.txt` |
| AI 駆動 | `bakasekai/common/scripted_effects/bsm_ea_ai_effects.txt` |
| 加盟意欲バイアス（誘致/妨害） | `bakasekai/common/scripted_effects/bsm_ea_recruit_effects.txt` |
| 初期陣営生成（on_startup） | `bakasekai/common/scripted_effects/bsm_ea_initialization.txt` |
| 加盟ニュースイベント | `bakasekai/events/bsm_ea_news_events.txt`（`bsm_ea_news.1`） |
| 共通トリガ（加盟判定等） | `bakasekai/common/scripted_triggers/bsm_ea_system_triggers.txt` |
| AI 方針トリガ | `bakasekai/common/scripted_triggers/bsm_ea_ai_triggers.txt` |
| 役職/方針アイデア | `bakasekai/common/ideas/_bsm_ea_role_policy_ideas.txt` |
| 目標アイデア | `bakasekai/common/ideas/_bsm_ea_goal_spirits.txt` |
| modifier 定義 | `bakasekai/common/modifier_definitions/_bsm_core.txt`（`ea_influence_factor`） |
| dynamic modifier | `bakasekai/common/dynamic_modifiers/bsm_dynamic_modifiers.txt`（`bsm_economic_alliance_pp_buff`） |
| scripted_localisation | `bakasekai/common/scripted_localisation/bsm_ea_scripted_localisation.txt` / `bsm_ea_goals_sloc.txt` |
| on_actions | `bakasekai/common/on_actions/bsm_economic_alliance_on_actions.txt` |
| ローカライズ | `bakasekai/localisation/japanese/bsm_economic_alliance_gui_l_japanese.yml` 他 |

---

## 3. データモデル

### 3.1 トークンと陣営
- 陣営は数値トークン（`global.next_alliance_id`、10 開始でインクリメント）で識別。
- `global.bsm_ea_sphere_list` … 全陣営トークンの配列。
- `global.bsm_ea_member_list_@{token}` … その陣営のメンバー国配列。**index 0 が盟主**。
- `global.bsm_ea_goal_list_@{token}` … その陣営の有効な目標トークン配列。
- `global.bsm_ea_policy_@{token}` … 全体方針（0=互恵, 1=搾取）。
- `global.bsm_ea_diplomat_@{token}` … 外交担当の保有国（country スコープ値）。

### 3.2 国（country）変数
| 変数 | 意味 |
|---|---|
| `bsm_ea_joined_spheres` | 加盟中トークン配列（複数所属可） |
| `bsm_ea_is_leader` / `bsm_ea_leader_of` | 盟主フラグ / 盟主であるトークン |
| `bsm_ea_sphere` | 最初に加盟したトークン（後方互換） |
| `bsm_ea_governance_mode` | 1=盟主主導, 2=共同運営(投票) |
| `bsm_ea_maturity` | 成熟度 1–5（目標解放条件） |
| `bsm_ea_influence` | 影響力（= IC × (1 + `modifier@ea_influence_factor`)） |
| `bsm_ea_member_seats` | 議席数（影響力比 × 100、四捨五入） |
| `bsm_ea_influence_pct` | 影響力％（表示用） |
| `bsm_ea_sphere_total_influence` | 盟主に保存される陣営合計影響力 |
| `economic_alliance_pp_buff_value` | UC/PP バフ配分値（影響力比、5%上限） |
| `bsm_ea_is_diplomat` | 外交担当フラグ |
| `bsm_ea_member_power` / `bsm_ea_total_power` / `bsm_ea_rank` / `bsm_ea_mem_count` | ランキング表示用 |
| `bsm_ea_cd_*` | 各アクションのクールダウン（日） |
| `bsm_ea_vote_*` | 投票状態（盟主に保存） |
| `bsm_ea_join_bias@{盟主TAG}` | その盟主の同盟への加盟意欲バイアス（-100..100） |

### 3.3 GUI 専用変数（プレイヤースコープ）
`bsm_ea_window_open`, `bsm_ea_active_tab`(1–4), `bsm_ea_selected_token`, `bsm_ea_is_selected_leader`, `bsm_ea_selected_maturity`, `bsm_ea_has_selected_member`, `bsm_ea_selected_policy`, `bsm_ea_has_diplomat`, `bsm_ea_goal_0X_active/available`, `bsm_ea_gui_vote_*`。
GUI キャッシュ配列: `global.bsm_ea_player_alliance_list`, `global.bsm_ea_gui_display_list`, `global.bsm_ea_sorted_sphere_list`。

---

## 4. 影響力モデル（議席）

`bsm_economic_alliance_calculations.txt`

- **影響力** `bsm_ea_influence = (民需+軍需) × (1 + modifier@ea_influence_factor)`（係数は下限0.1でクランプ）。
- `ea_influence_factor` は役職アイデア（議長+0.25、外交担当+0.10）等から供給される custom modifier。
- **議席** = `round(influence_i / total × 100)`。**影響力比**で `economic_alliance_pp_buff_value`（5%上限）を配分し、dynamic modifier `bsm_economic_alliance_pp_buff`（政治力・UC獲得をスケール）を15日付与。

> 重要: 表示用計算 `bsm_ea_calc_sphere_influence`（影響力/議席/％のみ、バフ非更新）と、週次のバフ配分を**分離**している。GUI 開時に表示計算を呼んでもバフが二重加算されない。週次 `bsm_update_economic_alliance_power_share` は「全メンバーのバフ値リセット → 各陣営で影響力計算 → 影響力比でバフ加算」の順。

---

## 5. 役職（議長 / 外交担当）

`bsm_ea_officials_effects.txt` / アイデア `_bsm_ea_role_policy_ideas.txt`

- **議長** = 盟主（`bsm_ea_is_leader`）。アイデア `bsm_ea_role_chair`（影響力+25%/政治力+10%）。
- **外交担当** = 任命制。アイデア `bsm_ea_role_diplomat`（影響力+10%/関係改善+20%）。`global.bsm_ea_diplomat_@{token}` に保有国。
- `bsm_ea_sync_my_roles`（月次 every_country 内）でアイデアを同期。
- 任命: GUI から `bsm_ea_assign_diplomat`（盟主が `event_target:bsm_ea_selected_member` を任命）。
- 離脱時 `bsm_ea_cleanup_my_roles`（残存陣営が無い場合のみアイデア除去）。

---

## 6. 全体方針（互恵 / 搾取）— UC 結合

`bsm_ea_policy_effects.txt`

- `global.bsm_ea_policy_@{token}`: 0=互恵（既定）, 1=搾取。
- `bsm_ea_apply_policy`（入力 `bsm_ea_token`）: 全メンバーの方針アイデアを除去 → 現方針を付与。
  - 互恵 `bsm_ea_policy_mutual`（全員 UC+5%/安定度+2%）
  - 搾取 `bsm_ea_policy_extractive_leader`（盟主 UC+20%/政治力+10%） / `bsm_ea_policy_extractive_member`（加盟国 UC-10%/安定度-5%）
- `bsm_ea_toggle_policy`（盟主のみ、GUI から）。
- `bsm_ea_apply_policy_extraction`（月次）: 搾取方針の陣営で**各加盟国 UC の 5% を盟主へ移転**。既存 `ucs_on_monthly` の属国徴収式に倣う。
- 月次 `bsm_ea_monthly_update` のスフィアループで `apply_policy` + `apply_policy_extraction` を実行。

---

## 7. 目標 / 投票

`bsm_ea_goals_effects.txt`
- 目標6種（`bsm_ea_goal_01_cooperation`…`06_tech_sharing`）。成熟度で段階解放。
- 盟主主導（governance=1）なら即時 `bsm_ea_add_goal_to_sphere`、共同運営（=2）なら `bsm_ea_start_goal_vote`（30日、過半数で可決）。
- 目標06は技術共有グループ（`bsm_ea_tsg_10`…`49`、トークン10–49の固定連鎖）を連動。**40陣営が上限**（拡張時は連鎖を増やす）。

---

## 8. 投資 / 援助アクション

`bsm_ea_action_effects.txt`（UC建て、`event_target:bsm_ea_selected_member` 対象）
ODA(50) / 長期融資(100) / 短期融資(200) / 負債肩代わり(300) / インフラ投資(150) / 技術支援(250)。各クールダウンあり。

---

## 9. 加盟意欲バイアス（誘致 / 妨害）★ v2 追加

`bsm_ea_recruit_effects.txt` + ディシジョン `bsm_ea_recruit_country` / `bsm_ea_discourage_country`

- 変数 `bsm_ea_join_bias@{盟主TAG}`（対象国スコープ, -100..100）。
- **modder API**（ROOT = 誘致する盟主）:
  ```
  対象国 = { save_event_target_as = bsm_ea_recruit_target }
  bsm_ea_recruit_promote = yes      # +30
  # または
  bsm_ea_recruit_discourage = yes   # -30
  # または任意増減:
  set_temp_variable = { t_delta = 15 }
  bsm_ea_apply_join_bias = yes
  ```
- **ディシジョン**: 盟主が政治力30を払い、隣接対象国の加盟意欲を ±25。
- **反映先**: `bsm_join_economic_alliance` の `ai_will_do`（ROOT=加盟希望国, FROM=盟主）が `bsm_ea_join_bias@FROM` を読み、+で加盟しやすく/−で加盟しにくくする（>49で×2、<-49で×0）。

> 仕組み: `bsm_ea_join_bias@PREV`（誘致側=PREV/ROOT）として対象国に保存 → join 側では FROM（盟主）= 同一国なので `@FROM` で読める。

---

## 9.5 加盟ニュースイベント ★ v2 追加

`events/bsm_ea_news_events.txt`（`bsm_ea_news.1`）

- `bsm_ea_join_sphere` 末尾の `bsm_ea_fire_join_news`（`bsm_ea_system_effects.txt`）から発火。
- `event_target:bsm_ea_news_joiner`（加盟国）/ `bsm_ea_news_leader`（盟主）を保存し、**陣営メンバー全員**へ `news_event = bsm_ea_news.1` を送る。
- 加盟国本人と既存メンバーで option 文言を出し分け（`tag = event_target:bsm_ea_news_joiner`）。
- **起動時の初期一括生成中は抑制**: `bsm_ea_init_initial_factions` がグローバルフラグ `bsm_ea_news_suppressed` を set→clr し、その間は発火しない。新規ニュースを join 経路に足す場合も同フラグを尊重すること。
- 監査を広げたい場合は `for_each_loop` の対象を `every_country`/majors に変更。

## 10. AI 挙動

`bsm_ea_ai_effects.txt` / トリガ `bsm_ea_ai_triggers.txt`

scripted_gui ボタンは AI が押せないため、月次 `bsm_ea_ai_monthly`（`bsm_ea_monthly_update` 末尾）で盟主 AI を駆動:
1. **全体方針**: フラグに応じ互恵/搾取を選択し適用。
2. **外交担当**: 未任命なら index1 の国を任命。
3. **目標**: `bsm_ea_ai_pick_goal` が成熟度に応じ1つずつ追加（盟主主導モード時）。
4. **投資**: 互恵 AI が最貧加盟国へ ODA（GUI 選択を汚さない `event_target:bsm_ea_ai_target` 使用）。

結成/加盟は `ai_will_do`（form/join ディシジョン）で制御。誘致ディシジョンにも `ai_will_do` あり。

### AI 方針フラグ（国フラグがグローバルより優先）
| 種別 | フラグ | 効果 |
|---|---|---|
| グローバル | `ea_ai_global_disabled` | 全AIのEA AI停止 |
| | `ea_ai_global_expansion` | 結成/加盟に積極化 |
| | `ea_ai_global_exploit` | 盟主が搾取志向 |
| | `ea_ai_global_benevolent` | 盟主が互恵+投資志向 |
| 国 | `ea_ai_disabled` | この国はEAに関与しない |
| | `ea_ai_expansionist` / `ea_ai_isolationist` | 結成/加盟に積極/不参加 |
| | `ea_ai_exploit` / `ea_ai_benevolent` | 盟主時に搾取/互恵を選択 |

設定例:
```
# history やイベントで
GER = { set_country_flag = ea_ai_benevolent }
set_global_flag = ea_ai_global_expansion
```

---

## 11. on_actions / 実行頻度

`bsm_economic_alliance_on_actions.txt`
- `on_weekly`: `bsm_update_economic_alliance_power_share`（影響力/バフ/ランキング）+ 投票週次更新。
- `on_monthly`: `bsm_ea_monthly_update`（信頼度/クールダウン/役職同期/方針適用/UC徴収/AI駆動）。

> **重要**: HOI4 の `on_monthly` / `on_weekly` / `on_daily` は**月/週/日に1回のみ発火**（per-country ではない）。根拠: 同 on_actions 内の `global.passed_month` 加算や、既存のクールダウン-30（非冪等）が壊れていない。したがって月次の**非冪等処理（搾取徴収・AI投資）は1回で正しく動作する**。新しい非冪等処理を月次に足す場合もこの前提に依存してよい。

---

## 12. GUI 構造（タブ）

- ウィンドウ `bsm_economic_alliance_window`（840×620）、`bsm_ea_active_tab`(1–4) で出し分け。
- タブ: ①議会（議席/運営/議題/投票）②経済（UC/方針トグル/投資アクション）③外交・役職（所属同盟/役職/任命/離脱）④ランキング。
- 議席は国別カラースプライトを作らず、`GetFlag` + 影響力％/議席数のテキスト列で表現。
- 動的リスト: player/member/target/appoint/ranking。`target` と `appoint` は同一配列 `global.bsm_ea_gui_display_list` を別 gridbox で参照。
- 配線は `bsm_economic_alliance_sgui.txt`（effects=ボタン、triggers=可視/有効、dynamic_lists）。

---

## 13. 拡張ガイド

- **新アクション追加**: `bsm_ea_action_effects.txt` に effect → `.gui` にボタン → `_sgui.txt` の effects/triggers に配線 → loc。
- **新目標追加**: `_bsm_ea_goal_spirits.txt` にアイデア → `bsm_ea_init_goal_system` の master_list → 解放条件（`bsm_ea_refresh_selection_data`）→ GUI ボタン/配線 → loc。
- **役職追加**: アイデア（`_bsm_ea_role_policy_ideas.txt`）+ 同期ロジック（`bsm_ea_sync_my_roles`）+ 任命 effect + GUI。
- **影響力源の追加**: アイデア/modifier に `ea_influence_factor` を持たせるだけで議席・バフに反映される。
- **AI 挙動の調整**: `bsm_ea_ai_effects.txt` と `ai_will_do`。方針はフラグで上書き可能。
- **41陣営以上**: `bsm_ea_join_tech_group` / `bsm_ea_leave_tech_group` の固定連鎖と `bsm_ea_tsg_*` を拡張。

---

## 14. 検証

```
mcp__hoi4__hoi4_cwtools_validate  <dir>   # 構文/ブレース/BOM
mcp__hoi4__hoi4_lint              <dir>   # 構文エラー
mcp__hoi4__hoi4_find_missing_keys bakasekai  # loc 欠落
```
ゲーム内: 4タブ切替 → 結成 → 外交担当任命 → 方針互恵↔搾取 → 翌月のUC徴収 → 誘致/妨害で AI 加盟意欲が変化 → `imgui show profiler` で週次/月次負荷確認。
