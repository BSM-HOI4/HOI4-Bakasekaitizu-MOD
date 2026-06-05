# 地球版・思想連動型ステラリス要素システム

## 概要

このドキュメントは、BSMmod の「研究・発見」画面で扱う地球版ステラリス要素の現行仕様をまとめる。

対象システムは以下の通り。

- 伝統: 探索、拡張、繁栄、軍備、外交、統治、調和
- アセンションパーク: 技術的卓越、世界規模行政、危機対処機構、破局への道、国土改造、国際交易網、人工進化計画、精神的覚醒
- 思想連動: 伝統コスト、アセンション取得可否、探検隊傾向、アノマリー報酬傾向
- 探検隊: 学術調査隊、軍事偵察隊、商業探検隊、科学調査隊
- アノマリー連携: 発見候補、研究速度、報酬、事故傾向

本システムは宇宙進出ではなく、地球上の調査、異常地形、秘匿資料、文明発展、社会変質を扱う。

## 実装ファイル

- `bakasekai/common/scripted_effects/_bsm_stellaris_effects.txt`
- `bakasekai/common/scripted_triggers/_bsm_stellaris_triggers.txt`
- `bakasekai/common/decisions/_bsm_stellaris_decisions.txt`
- `bakasekai/common/decisions/_bsm_stellaris_ascension_decisions.txt`
- `bakasekai/common/decisions/_bsm_stellaris_expedition_decisions.txt`
- `bakasekai/common/decisions/_bsm_stellaris_traits_decisions.txt`
- `bakasekai/common/ideas/_bsm_stellaris_traits_detailed.txt`
- `bakasekai/common/scripted_guis/bsm_stellaris.txt`
- `bakasekai/interface/bsm_stellaris.gui`
- `bakasekai/events/_bsm_stellaris_expedition_events.txt`
- `bakasekai/common/scripted_effects/_bsm_stellaris_anomaly_integration.txt`
- `bakasekai/common/scripted_effects/_bsm_stellaris_anomaly_mapping.txt`
- `bakasekai/common/scripted_effects/_bsm_anomaly_system.txt`
- `bakasekai/localisation/japanese/bakasekai/_bsm_stellaris_l_japanese.yml`

## 初期化

`common/on_actions/_bsm_system.txt` の `on_startup` から `bsm_stellaris_init` を呼ぶ。

`bsm_stellaris_init` は `bsm_stellaris_initialized` グローバルフラグがない場合のみ実行され、各国に `bsm_stellaris_country_init` を適用する。

既存セーブ向けの補完・移行処理は持たない。新仕様の変数は初期化時に作成される前提とする。

## 主要変数

伝統進捗:

- `bsm_stellaris_tradition_exploration` 0-7
- `bsm_stellaris_tradition_expansion` 0-7
- `bsm_stellaris_tradition_prosperity` 0-7
- `bsm_stellaris_tradition_armaments` 0-7
- `bsm_stellaris_tradition_diplomacy` 0-7
- `bsm_stellaris_tradition_governance` 0-7
- `bsm_stellaris_tradition_harmony` 0-7

伝統取得補助:

- `bsm_stellaris_tradition_category`
- `bsm_stellaris_tradition_cost`
- `bsm_stellaris_tradition_has_affinity`
- `bsm_stellaris_ascension_adopted`

アセンション:

- `bsm_stellaris_ascension_slots`
- `bsm_stellaris_ascension_perks_taken`
- `bsm_stellaris_ascension_park_token`

特性:

- `bsm_stellaris_trait_slots`
- `bsm_stellaris_traits_equipped`
- `bsm_stellaris_trait_id`
- `bsm_stellaris_trait_token`

探検隊:

- `bsm_stellaris_expedition_count`
- `bsm_stellaris_expedition_active`
- `bsm_stellaris_expedition_type`

アノマリー:

- `bsm_stellaris_anomaly_research_bonus`
- `bsm_stellaris_anomaly_research_field`
- `bsm_stellaris_anomaly_difficulty_level`
- `bsm_stellaris_anomaly_accident_risk`
- `AN_research_slot_1_token`
- `AN_research_slot_2_token`

## 伝統ツリー

各伝統ツリーは Stellaris 風の「採用 + 5伝統 + 完成」形式で、進捗は 0-7。

- 0: 未採用
- 1: 採用ボーナス
- 2-6: 個別伝統 1-5
- 7: 完成ボーナス

完成時にアセンションスロット計算へ寄与する。

### ツリー一覧

| カテゴリ値 | ツリー | 変数 | 主題 |
| --- | --- | --- | --- |
| 1 | 探索 | `bsm_stellaris_tradition_exploration` | 調査、アノマリー発見、異常地形解析 |
| 2 | 拡張 | `bsm_stellaris_tradition_expansion` | 辺境開発、影響圏、到達範囲 |
| 3 | 繁栄 | `bsm_stellaris_tradition_prosperity` | 産業、交易、資源循環 |
| 4 | 軍備 | `bsm_stellaris_tradition_armaments` | 軍備、兵站、危険物管理 |
| 5 | 外交 | `bsm_stellaris_tradition_diplomacy` | 国際協力、共同調査、危機連絡 |
| 6 | 統治 | `bsm_stellaris_tradition_governance` | 官僚制、統合庁、監査 |
| 7 | 調和 | `bsm_stellaris_tradition_harmony` | 社会安定、文化受容、精神的耐性 |

## 思想適性と伝統コスト

伝統取得時に `bsm_stellaris_get_ideology_tradition_affinity` を呼び、現在の `bsm_stellaris_tradition_category` と国家思想から適性を判定する。

- 適性あり: `bsm_stellaris_tradition_cost = 75`
- 適性なし: `bsm_stellaris_tradition_cost = 100`

決定の `available` も同じ方針で、適性ありなら統合力 75、適性なしなら統合力 100 を要求する。

### 思想適性表

| 思想 | 適性伝統 |
| --- | --- |
| `civilism` | 繁栄、統治、調和 |
| `futurism` | 拡張、軍備 |
| `intellectualism` | 探索、繁栄 |
| `mythologicalism` | 探索、調和 |
| `technicalism` | 探索、軍備 |
| `philanthropy` | 外交、調和 |
| `transformationism` | 拡張、繁栄 |
| `ruinism` | 軍備 |
| `stupidism` | 探索、アノマリー傾向強化 |
| `longitudinalism` | 探索、地形改変傾向 |
| `horizontalism` | 探索、地形改変傾向 |
| `hinnulism` | 調和、文化ネタ系傾向 |
| `kyonulism` | 調和、文化ネタ系傾向 |
| `democratic_ideology` | 外交、統治、調和 |
| `conservative_democracy` | 外交、統治、調和 |
| `direct_democracy` | 外交、統治、調和 |
| `constitutional_monarchy` | 外交、統治 |
| `communism_ideology` | 拡張、統治、調和 |
| `anarchism` | 拡張、統治、調和 |
| `fascism_ideology` | 拡張、軍備、統治 |
| `rightneutrality` | 拡張、軍備、統治 |
| `neutrality_ideology` | 探索、繁栄、統治 |

## アセンションパーク

伝統ツリー完成ごとにアセンションスロットを得る。全7ツリー完成時は追加で1スロットを得るため、最大8スロット。

取得済みパーク数は `bsm_stellaris_ascension_perks_taken` で管理し、空きスロットは `bsm_stellaris_ascension_slots` に反映する。

取得時は各パークの明示条件を通したうえで `bsm_stellaris_ascension_park_token` にidea tokenを設定し、共通処理で `add_ideas = var:bsm_stellaris_ascension_park_token` を実行する。

| ID | 名称 | 主な適性思想 | 備考 |
| --- | --- | --- | --- |
| `bsm_stellaris_ascension_park_1` | 技術的卓越 | `technicalism`, `intellectualism`, `futurism` | 技術・解析系 |
| `bsm_stellaris_ascension_park_2` | 世界規模行政 | `civilism`, 民主系, 中立系 | 統治・行政系 |
| `bsm_stellaris_ascension_park_3` | 危機対処機構 | `philanthropy`, `civilism`, 民主系 | `破局への道` と相互排他 |
| `bsm_stellaris_ascension_park_4` | 破局への道 | `ruinism`, `futurism`, 軍国系 | `危機対処機構` と相互排他 |
| `bsm_stellaris_ascension_park_5` | 国土改造 | `longitudinalism`, `horizontalism`, `transformationism` | 地形改変系 |
| `bsm_stellaris_ascension_park_6` | 国際交易網 | `civilism`, `philanthropy`, 民主系, 中立系 | 交易・協力系 |
| `bsm_stellaris_ascension_park_7` | 人工進化計画 | `transformationism`, `technicalism`, `intellectualism` | 人工進化・社会変質系 |
| `bsm_stellaris_ascension_park_8` | 精神的覚醒 | `mythologicalism`, `philanthropy`, `hinnulism`, `kyonulism` | 精神・文化系 |

## 探検隊

探検隊は統合力 50 を消費して作成する。

内部データとしては以下を基本形とする。

```hoi4
{ TAG, ICON, NAME, SIZE, LEVEL, STATUS, TRAIT }
```

派遣先は以下を基本形とする。

```hoi4
{ NAME, CATEGORY, COST, DAYS, REWARD_POOL }
```

現在の簡易実装では `bsm_stellaris_expedition_type` で隊種を持ち、開始イベントから60日後に完了イベントを呼ぶ。

| type | 隊種 | 傾向 |
| --- | --- | --- |
| 1 | 学術調査隊 | 知識・文明・文書系 |
| 2 | 軍事偵察隊 | 軍事・危険物・破局系 |
| 3 | 商業探検隊 | 交易・資源・経済系 |
| 4 | 科学調査隊 | 技術・異常現象系 |

## 思想別アノマリー傾向

探検隊完了時、思想に応じて `AN_analyzed_list` に発見候補を追加する。

| 思想 | 代表候補 |
| --- | --- |
| `intellectualism`, `technicalism` | `AS_AN_Knowledge_Intensive_Laboratory` |
| `futurism`, `ruinism` | `AS_AN_Manhattan_Project_Documents` |
| `mythologicalism` | `AS_AN_Antarctic_Containment_Breach` |
| `philanthropy` | `AS_AN_Peaceful_Militarism_Doctrine` |
| `transformationism` | `AS_AN_Primitive_Regression_Process` |
| `longitudinalism` | `AS_AN_Longitudinal_Stretching_Device` |
| `horizontalism` | `AS_AN_Horizontal_Compression_System` |
| `hinnulism` | `AS_AN_Hinnuism_Secret_Texts` |
| `kyonulism` | `AS_AN_Kyonuism_Manifesto` |
| `stupidism` | `AS_AN_Stupid_Education_Reform`、事故リスク上昇 |

アノマリーの構造は以下を基本形とする。

```hoi4
{ TAG, ICON, NAME, IMAGE, CATEGORY, SUBCATEGORY, DIFFICULTY, REQUIRED_DAYS, STATUS, REWARD }
```

既存の `AS_set_anomaly_data` は `TAG`, `CATEGORY`, `SUBCATEGORY`, `DIFFICULTY`, `REQUIRED_DAYS` を配列で登録している。

研究スロットで扱う報酬ideaは `AN_research_slot_1_token`, `AN_research_slot_2_token` に保存し、開始時は `AN_researching_list`、完了時は `AN_completed_list` を同じslot tokenで更新する。報酬付与は `add_ideas = var:AN_research_slot_*_token` で実行する。開始可否の判定は、現時点では対象ideaごとの明示条件で行う。

## アノマリー研究速度

`bsm_stellaris_anomaly_research_speed_calc` は文明度と伝統から `bsm_stellaris_anomaly_research_bonus` を計算する。

加算対象:

- `Cultural_Degree`
- 探索伝統
- 調和伝統
- 統治伝統
- 繁栄伝統

最終値は `0.01` から `0.5` にクランプする。

## 特性

特性は文明度でスロット数が増える。

- 30以上: 1
- 50以上: 3
- 80以上: 5
- 100以上: 6

装備・解除は `bsm_stellaris_trait_id` による明示分岐で安全条件を確認し、実際の付与・解除は `bsm_stellaris_trait_token` を使って `add_ideas = var:bsm_stellaris_trait_token` / `remove_ideas = var:bsm_stellaris_trait_token` で実行する。

固定特性:

- `bsm_stellaris_trait_aggressive`
- `bsm_stellaris_trait_peaceful`
- `bsm_stellaris_trait_expansionist`
- `bsm_stellaris_trait_isolationist`
- `bsm_stellaris_trait_spiritualist`
- `bsm_stellaris_trait_materialist`

追加特性例:

- `bsm_stellaris_trait_available_technologically_advanced`
- `bsm_stellaris_trait_technologically_advanced`

## 動的idea付与の方針

動的idea付与は全面禁止しない。

SSW由来コード、SSW互換コード、またはSSWで実用されている構文と同等の用途では、以下のような書き方を許容する。

```hoi4
add_ideas = some_idea_@var:some_variable
add_ideas = var:some_idea_token
remove_ideas = var:some_idea_token
```

`bsm_stellaris` 系でも、SSWで実績のある構文・スコープ・トークン管理に準じる場合は、以下のような使い方をしてよい。

```hoi4
add_ideas = var:bsm_stellaris_trait_token
remove_ideas = var:bsm_stellaris_trait_token
add_ideas = var:bsm_stellaris_ascension_park_token
add_ideas = var:AN_research_slot_1_token
add_to_array = { AN_researching_list = var:AN_research_slot_1_token }
remove_from_array = { AN_researching_list = var:AN_research_slot_1_token }
```

運用方針:

- 明示分岐の方が読みやすい小規模処理では明示分岐を優先する。
- 配列、リスト、SSW式GUI、汎用装備/解除処理など、動的トークンの方が保守性を上げる場合は動的付与を使ってよい。
- 使用時は `error.log` で `Unknown effect`, `Unknown trigger`, 無効なトークン展開が出ていないことを確認する。
- 動的トークンの生成元、想定idea、失敗時の影響を同じファイルまたは関連ドキュメントに明記する。

## 追加・変更時のチェックリスト

- 新伝統を追加したら `ideas`, `scripted_effects`, `decisions`, `scripted_guis`, `localisation` を揃える。
- 思想適性を変えたら `bsm_stellaris_has_*_tradition_affinity` と `bsm_stellaris_has_current_tradition_affinity` を揃える。
- アセンション条件を変えたら `bsm_stellaris_prefers_*_ascension` と決定の `available` を揃える。
- アノマリー傾向を変えたら `AS_set_anomaly_data` の実在TAGと照合する。
- 補完・移行処理は通常追加しない。必要な場合は別途明示的な移行イベントとして設計する。
- 実機確認では HOI4 ログで `Unknown effect`, `Unknown trigger`, `Invalid token`, `Invalid idea` を確認する。
