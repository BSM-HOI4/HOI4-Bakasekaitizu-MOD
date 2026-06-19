# EA/NCS Math Expressions・Collections 実装計画

最終更新: 2026-06-14

## 目的

HOI4 の新機能である Math Expressions と Collections を活用し、既存の UC（統一通貨）、EA（経済同盟）、NCS（国家通貨）を拡張する。

主目的は以下の3点。

- UC/EA/NCS の月次・週次処理を数式化して temp 変数操作を削減する
- Collections によって「同盟内の該当国」「地域別通貨国」「危機国」などの抽出を再利用可能にする
- 経済同盟を単なるボーナス源ではなく、通貨危機・投資・資源安全保障・準備金を持つ動的な経済圏へ拡張する

## 対象システム

| システム | 既存の主ファイル | 変更方針 |
|---|---|---|
| UC | `bakasekai/common/scripted_effects/_bsm_Unified_Currency.txt` | 為替・EA統合度・準備金などを係数化 |
| EA | `bakasekai/common/scripted_effects/bsm_ea_*.txt` | 統合度、危機圧力、準備金、AI投資、資源目標を追加 |
| NCS | `bakasekai/common/scripted_effects/_bsm_national_currency.txt` | 通貨危機、通貨バスケット、表示リストを拡張 |
| Collections | `bakasekai/common/collections/collections.txt` | EA/NCS用の国・ステート集合を追加 |
| GUI | `bakasekai/interface/bsm_economic_alliance.gui` / `bakasekai/common/scripted_guis/bsm_economic_alliance_sgui.txt` | 既存Tab5通貨レートを拡張し、危機・投資候補・準備金表示を追加 |
| Localisation | `bakasekai/localisation/japanese/*.yml` | 新変数・新目標・GUI文言を追加 |

## 実装する機能一覧

| ID | 機能 | 優先度 | 実装段階 |
|---|---|---:|---|
| F1 | EA統合度スコア | 高 | Phase 1 |
| F2 | 通貨危機の伝播システム | 高 | Phase 2 |
| F3 | EA資源安全保障目標 | 中 | Phase 5 |
| F4 | UC決済基金 / 同盟準備金 | 高 | Phase 3 |
| F5 | EA投資AIのスコア制 | 高 | Phase 4 |
| F6 | 通貨バスケット制度 | 中 | Phase 6 |
| F7 | EA/NCSダッシュボード用 Collections | 高 | Phase 1-2 |
| F8 | GDP基盤（全指標の分母） | 高 | Phase 0.5 |

## Phase 0: 事前整理

### 作業内容

1. 既存EA/NCS変数の棚卸し
2. 新規変数名の確定
3. Collections の定義方針を確定
4. テスト用ディシジョンの追加方針を決める

### 新規変数案

| 変数 | スコープ | 用途 |
|---|---|---|
| `bsm_ea_integration_score` | 盟主 | 経済同盟の統合度 0-100 |
| `bsm_ea_avg_trust` | 盟主 | 加盟国平均信頼度 |
| `bsm_ea_avg_nc_stability` | 盟主 | 加盟国平均通貨安定度 |
| `bsm_ea_crisis_pressure` | 盟主 | 通貨危機伝播圧力 0-100 |
| `bsm_ea_reserve_uc` | 盟主 | 同盟準備金UC |
| `bsm_ea_investment_need_score` | 加盟国 | 投資優先度 |
| `bsm_ea_resource_security_score` | 盟主 | 資源安全保障スコア |
| `bsm_nc_basket_rate` | 盟主/加盟国 | 通貨バスケットの参照レート |
| `bsm_nc_basket_weight` | 加盟国 | バスケット内の重み |

### 注意点

- `clamp_variable` / `clamp_temp_variable` には必ず `var =` を付ける
- ローカライズ内の国変数は原則 `[?ROOT.variable]` とする
- `scripted_triggers` 内では `set_temp_variable` などの effect を使わない
- Collections は `collections:` / `collection:` プレフィックスを厳密に使い分ける

## Phase 0.5: GDP基盤（F8）

詳細設計は `documents/00_coding_contexts/bsm_economic_systems_design.md` §3。本計画では「F1統合度・F5投資の**分母**」として GDP を先に用意することだけ確定する。

### 目的

統合度・投資必要度・準備金拠出を絶対値（UC額・工場数）でなく **GDP比** で表し、極端な国でも 0–100 / 0–1 に収めてオーバーフローとクランプ調整を減らす。

> 補足(2026-06-19): `every_collection` 数式集約は実機検証済み（`00_coding_contexts/bsm_economic_systems_design.md` §11、反復版と完全一致）。GDP集約・地域/世界合計・`bsm_resource_value` は `for_each_loop` でなく **1式の数式集約**で書けるため、本計画の Collections（F7）と相性が良い。

### 実装する変数 / effect

| 変数 | スコープ | 用途 |
|---|---|---|
| `bsm_gdp_real` | 加盟国/全国 | 実質GDP（スケール済み） |
| `bsm_gdp_last` | 加盟国/全国 | 前月値（成長率算出用） |
| `bsm_resource_value` | 加盟国/全国 | 自国資源産出額（スポット価格×産出, 価格未実装時は固定単価） |

- effect `bsm_econ_update_gdp`（country）: 上記設計 §3.1 の数式で `bsm_gdp_real` を更新し、末尾で `bsm_gdp_last` を退避。
- 接続: `bsm_ea_monthly_update` のスフィアループ内、`bsm_ea_update_sphere_metrics` の**前**に各加盟国で呼ぶ（統合度・投資スコアが当月GDPを読めるようにする）。

### F1/F5 への供給

- F1 統合度: `member_count * 6` の規模項を `Σ member GDP` ベースに置換可能（任意）。
- F5 投資必要度: `max(100 - Unified_Currency, 0)` を `max(基準GDP比 - 自国GDP比, 0)` に拡張可能（任意）。
- まずは GDP を**保存・表示するだけ**でも可。式の置換は段階的に。

### 検証

- 加盟国0/1/複数で `bsm_gdp_real` がエラーなく 0–1000000 に収まること
- `bsm_gdp_last` 退避で成長率が NaN/極端値にならないこと（0除算は `+1` 保険）
- 価格未実装の段階では `bsm_resource_value` を固定単価でフォールバックできること

## Phase 1: EA/NCS Collections 基盤とEA統合度スコア

### 目的

EA内の状態を毎回 `for_each_loop` で直接数えるのではなく、Collections と Math Expressions で再利用可能な指標に変換する。

### 追加する Collections 案

`bakasekai/common/collections/collections.txt` に以下を追加する。

```txt
bsm_nc_world_currency_users = {
  input = game:all_countries
  operators = {
    limit = {
      bsm_nc_show_in_list = yes
    }
  }
  name = COLLECTION_BSM_NC_WORLD_CURRENCY_USERS
}

bsm_nc_weak_currency_countries = {
  input = collection:bsm_nc_world_currency_users
  operators = {
    limit = {
      check_variable = { bsm_nc_strength_cat = 2 }
    }
  }
  name = COLLECTION_BSM_NC_WEAK_CURRENCY_COUNTRIES
}
```

EAメンバーは既存の `global.bsm_ea_member_list_@{token}` 配列で管理されているため、トークン別Collections化が難しい場合は、まず匿名 collection を使う。

### 実装する effect

`bsm_ea_goals_effects.txt` または新規 `bsm_ea_metrics_effects.txt` に追加。

- `bsm_ea_update_integration_score`
- `bsm_ea_update_alliance_averages`
- `bsm_ea_update_crisis_counts`

### 統合度の計算式案

```txt
integration =
  avg_trust * 0.35
  + avg_nc_stability * 0.25
  + min(member_count * 6, 30)
  + goal_count * 5
  - crisis_pressure * 0.30
  - influence_concentration_penalty
```

Math Expressions 例。

```txt
set_variable = {
  var = bsm_ea_integration_score
  value = {
    value = bsm_ea_avg_trust
    multiply = 0.35
    add = { value = bsm_ea_avg_nc_stability  multiply = 0.25 }
    add = { value = bsm_ea_member_count  multiply = 6  min = 30 }
    add = { value = global.bsm_ea_goal_list_@var:bsm_ea_token^num  multiply = 5 }
    subtract = { value = bsm_ea_crisis_pressure  multiply = 0.30 }
    clamp = { min = 0 max = 100 }
  }
}
```

### 既存処理への接続

- `bsm_ea_monthly_update` のスフィアループ内で呼び出す
- `bsm_ea_update_sphere_metrics` 後に実行する
- 盟主に保存し、GUIと目標解放条件で読む

### 検証

- 加盟国0/1/複数でエラーが出ないこと
- `bsm_ea_integration_score` が 0-100 に収まること
- 既存の成熟度 `bsm_ea_maturity` が壊れないこと

## Phase 2: 通貨危機の伝播システム

### 目的

NCSの国別通貨危機をEA全体に伝播させ、通貨同盟や準備金の重要性を上げる。

### 新規変数

| 変数 | スコープ | 内容 |
|---|---|---|
| `bsm_ea_crisis_pressure` | 盟主 | 危機伝播圧力 |
| `bsm_ea_weak_currency_count` | 盟主 | 弱い通貨国数 |
| `bsm_ea_high_inflation_count` | 盟主 | 高インフレ国数 |
| `bsm_ea_uc_deficit_count` | 盟主 | UC赤字国数 |

### 危機圧力の計算式案

```txt
pressure =
  weak_currency_count * 8
  + high_inflation_count * 12
  + uc_deficit_count * 10
  - integration_score * 0.15
  - reserve_uc / 100
```

### 効果

| 条件 | 効果 |
|---|---|
| `bsm_ea_crisis_pressure >= 30` | 軽度警戒。GUI表示のみ |
| `>= 50` | 加盟国の通貨安定度に軽いペナルティ |
| `>= 75` | 盟主へ危機イベント |
| `>= 90` | 通貨同盟離脱圧力を加速 |

### 実装候補ファイル

- `bakasekai/common/scripted_effects/_bsm_national_currency.txt`
- `bakasekai/common/scripted_effects/bsm_ea_goals_effects.txt`
- `bakasekai/events/_bsm_national_currency_events.txt`
- `bakasekai/common/dynamic_modifiers/_bsm_national_currency_modifiers.txt`

### イベント案

| ID | 内容 |
|---|---|
| `nc.10` | EA通貨危機の警告 |
| `nc.11` | EA通貨危機への共同対応 |
| `nc.12` | 危機対応失敗による離脱圧力上昇 |

### 検証

- 弱い通貨国を2-3国作り、盟主の `bsm_ea_crisis_pressure` が増えること
- 準備金や統合度が高いと危機圧力が抑制されること
- `nc.5` の既存通貨同盟危機とイベント連打しないこと

## Phase 3: UC決済基金 / 同盟準備金

### 目的

EAの互恵方針に実体を持たせ、UC黒字国から同盟準備金を積み立て、危機国や投資対象へ配分できるようにする。

### 新規 effect

| effect | 用途 |
|---|---|
| `bsm_ea_collect_reserve_uc` | 月次拠出 |
| `bsm_ea_spend_reserve_for_crisis` | 危機対応 |
| `bsm_ea_spend_reserve_for_investment` | 投資支援 |
| `bsm_ea_update_reserve_status` | GUI用状態更新 |

### 拠出額の計算式案

```txt
contribution =
  max(Unified_Currency - 100, 0)
  * 0.03
  * policy_factor
  * trust_factor
```

方針係数。

| 方針 | `policy_factor` |
|---|---:|
| 互恵 | 1.0 |
| 搾取 | 0.3 |

信頼係数。

```txt
trust_factor = clamp(bsm_ea_trust / 100, 0.25, 1.25)
```

### 配分ルール

| 条件 | 支出 |
|---|---|
| 通貨安定度 < 30 | 準備金25消費、安定度 +10 |
| UC < 0 | 準備金50消費、対象UC +50 |
| インフレ > 20 | 準備金40消費、インフレ -5 |
| 危機圧力 > 75 | 準備金100消費、危機圧力 -20 |

### GUI表示

EAの経済タブまたは通貨タブに以下を追加。

- 同盟準備金UC
- 月次拠出見込み
- 危機対応可否
- 自動支援ON/OFF

### 検証

- UC黒字国のみ拠出すること
- 準備金がマイナスにならないこと
- 搾取方針の既存UC徴収と二重に過大徴収しないこと

## Phase 4: EA投資AIのスコア制

### 目的

現在の「最貧加盟国へODA」から、通貨・安定度・工場・信頼度を見た投資判断へ拡張する。

### 新規変数

| 変数 | スコープ | 内容 |
|---|---|---|
| `bsm_ea_investment_need_score` | 加盟国 | 投資必要度 |
| `bsm_ea_preferred_action` | 加盟国 | 推奨支援種別 |

### スコア計算式案

```txt
need =
  max(100 - Unified_Currency, 0) * 0.20
  + max(60 - bsm_nc_stability, 0) * 0.80
  + max(10 - num_of_civilian_factories, 0) * 4
  + max(10 - num_of_military_factories, 0) * 2
  + inflation_penalty
  + trust_bonus
```

推奨アクション。

| 条件 | アクション |
|---|---|
| `Unified_Currency < 0` | ODA / 短期融資 |
| `bsm_nc_stability < 40` | 通貨安定化支援 |
| 工場不足 | インフラ投資 |
| 信頼度高かつ技術遅れ | 技術支援 |

### 既存AIへの接続

`bsm_ea_ai_invest` を以下の流れに変更する。

1. 全加盟国の `bsm_ea_investment_need_score` を更新
2. 最大スコア国を選ぶ
3. 盟主UC・準備金・クールダウンから支援種別を選ぶ
4. 支援を実行

### 検証

- 最貧国だけでなく、通貨危機国が優先されること
- 盟主のUC不足時に投資しないこと
- GUI選択用 event_target を汚さないこと

## Phase 5: EA資源安全保障目標

### 目的

Collections の `has_resources_in_collection` を使い、EA全体の資源不足を目標・AI・投資に反映する。

### 新規目標案

| 目標 | 解放条件 | 効果 |
|---|---|---|
| `bsm_ea_goal_07_resource_security` | 成熟度2以上 | 資源不足国への採掘/インフラ投資 |
| `bsm_ea_goal_08_strategic_stockpile` | 成熟度3以上 | 同盟準備金で資源備蓄補正 |
| `bsm_ea_goal_09_energy_settlement` | 成熟度4以上 | 石油・燃料関連補正 |

### Collections / triggers 例

```txt
has_resources_in_collection = {
  collection = {
    input = game:scope
    operators = { faction_members }
    name = BSM_EA_MEMBERS
  }
  resource = oil
  amount < 20
  extracted = no
}
```

EAは通常の陣営 faction とは別管理のため、まずは `global.bsm_ea_member_list_@token` の for_each で不足値を計算し、将来的に匿名 collection へ寄せる。

### 既存システムとの接続

- EA目標リスト `global.bsm_ea_goal_master_list` に追加
- `bsm_ea_ai_pick_goal` に資源不足時の優先ロジックを追加
- 投資アクションに「資源開発支援」を追加

### 検証

- 資源不足時だけAIが資源系目標を選ぶこと
- 既存Goal01-06の解放順を壊さないこと
- GFX/loc欠落がないこと

## Phase 6: 通貨バスケット制度

### 目的

Goal03通貨同盟を「盟主通貨への単純同期」から、加盟国の重み付き通貨バスケットへ発展させる。

### 適用条件

以下のいずれかで有効化する。

- Goal03通貨同盟が有効
- 統合度スコア70以上
- 準備金UC 300以上

### 重み計算式案

```txt
weight =
  influence_pct * 0.50
  + bsm_nc_stability * 0.30
  + clamp(Unified_Currency / 1000, 0, 20)
```

バスケットレート。

```txt
basket_rate =
  SUM(member_rate * member_weight) / SUM(member_weight)
```

### 実装メモ

- HOI4 script でSUMを作るため、陣営メンバー配列の `for_each_loop` は必要
- 各メンバー側では `bsm_nc_basket_weight` を Math Expressions で算出する
- 盟主側に `bsm_nc_basket_rate` と `bsm_nc_basket_total_weight` を保存する
- 加盟国の `bsm_nc_rate` は収斂度に応じて `bsm_nc_basket_rate` へ近づける

### 収斂式案

```txt
new_rate =
  current_rate * (1 - convergence_ratio)
  + basket_rate * convergence_ratio
```

`convergence_ratio = clamp(bsm_nc_union_convergence / 100, 0.1, 0.8)`

### 検証

- 盟主1国だけの場合は既存同期と同じ結果になること
- 極端なレート通貨が入っても clamp で破綻しないこと
- 通貨同盟離脱時に元通貨へ復帰できること

## Phase 7: EA/NCSダッシュボード拡張

### 目的

既存のEA通貨レートタブを、通貨・危機・投資・準備金を一覧できる運用画面にする。

### 表示モード

| モード | 表示対象 |
|---|---|
| 同盟内 | 自国EAメンバー |
| 世界 | 全通貨国 |
| 地域 | アジア/欧州/北米/南米/アフリカ/中東/大洋州 |
| 危機 | 弱い通貨、高インフレ、UC赤字 |
| 投資候補 | `bsm_ea_investment_need_score` 上位 |

### 既存処理の置換候補

`bsm_nc_prepare_rate_list` は地域ごとの `every_country` 分岐が多い。新しい Collections を使って表示対象抽出を共通化する。

### GUIに追加する列

| 列 | 内容 |
|---|---|
| 危機 | `bsm_nc_strength_cat` / `bsm_nc_stability` |
| 投資必要度 | `bsm_ea_investment_need_score` |
| 準備金支援 | 支援可能/不可 |
| 通貨同盟 | 収斂度/離脱圧力 |

### 検証

- `reload interface` でタブ切替が壊れないこと
- `parent_window_name` を維持し、OE方式タブ構造を崩さないこと
- リスト項目の重複がないこと

## 実装順序

1. `collections.txt` にNCS/EA用collectionを追加 ／ **GDP基盤 `bsm_gdp_real`（F8, Phase 0.5）を実装し F1統合度・F5投資の分母に供給**
2. `bsm_ea_metrics_effects.txt` を新規作成し、統合度・危機カウント・平均値を実装
3. `bsm_ea_monthly_update` に指標更新を接続
4. NCS通貨危機伝播とEA危機圧力を接続
5. 同盟準備金の徴収・支出を実装
6. 投資AIスコア制を実装
7. 資源安全保障目標を追加
8. 通貨バスケット制度を実装
9. GUI/ローカライズを拡張
10. テストディシジョンとデバッグ表示を追加

## テスト計画

### スクリプト検証

```txt
python3 .claude/skills/hoi4-searcher/scripts/search_defs.py --check <changed files>
```

可能なら変更ファイル単位で CWTools 相当の検証を行う。

### ゲーム内検証

| テスト | 手順 | 確認内容 |
|---|---|---|
| EA統合度 | テストEAを作成し月次更新 | 統合度が0-100で更新 |
| 通貨危機 | 加盟国の通貨安定度/インフレを悪化 | 危機圧力・イベント発火 |
| 準備金 | UC黒字国を複数加盟 | 準備金が増加 |
| 投資AI | AI盟主 + 危機国 | 適切な対象へ支援 |
| 資源目標 | 石油/鉄不足EA | 目標選択・補正付与 |
| 通貨バスケット | Goal03有効化 | バスケットレートへ収斂 |
| GUI | EA画面Tab5 | 表示モード切替・値表示 |

### デバッグディシジョン案

`bakasekai/common/decisions/bsm_ea_test_decisions.txt` に追加。

- EA指標を強制更新
- 危機圧力を +25 / 0 に戻す
- 準備金UCを +100 / 0 に戻す
- 選択国を弱通貨化
- 通貨バスケットを再計算

## リスクと対策

| リスク | 対策 |
|---|---|
| Collections がEA独自配列と噛み合わない | 最初は既存配列 `global.bsm_ea_member_list_@token` を併用し、世界/地域抽出からCollections化する |
| 月次処理が重くなる | every_country を増やさず、既存 `bsm_ea_monthly_update` の陣営ループに集約する |
| 通貨同盟危機イベントが連打される | 既存の `bsm_nc_union_crisis_recent` と同様に日数付きフラグを使う |
| 準備金と搾取徴収でUC移転が過剰になる | 方針係数と上限を設け、準備金徴収は黒字分のみ対象にする |
| GUIが複雑化する | Tab5内で表示モード切替に留め、新タブ追加は最後に判断する |
| 既存セーブ互換性 | 新変数は未定義時0として扱い、初回月次で自然初期化する |

## 完了条件

- 全機能が既存EA/NCS/UCフローに接続されている
- `bsm_ea_monthly_update` と `bsm_nc_monthly_update` がエラーなしで動く
- EA GUIで統合度、危機圧力、準備金、投資候補が確認できる
- 通貨危機、準備金支援、投資AI、資源目標、通貨バスケットをテストディシジョンで再現できる
- 追加ローカライズキーに欠落がない
- `imgui show profiler` の Script タブで月次処理の悪化が許容範囲内である
