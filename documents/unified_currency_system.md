# 統一通貨システム (Unified Currency System)

## 概要

統一通貨システムは、国家の経済力を表すリソースです。民需工場出力、安定度、文明度、人口、インフラなど様々な要因に基づいて計算されます。探検隊派遣や未知の解明など、政府の様々な用途に使用されます。

### 変数名
- `Unified_Currency` (整数値)

### 基本特性
- **初期値**: 0
- **最小値**: 0
- **最大値**: なし（上限なし）
- **更新頻度**: 日次 (daily)

## 計算式

### 基本計算式

**完全な計算式**:

```
[
    SUM{ 人口(m) × (インフラ×1.25 + 飛行場×1.1 + 港湾×0.8) }
    × 民需出力 × (安定度 + 文明度)
    - (徴兵(m) × ステート数)
] / 100 × 係数
```

**係数の構成**:

```
係数 = 基本値(1)
      + UC獲得補正(modifier@Unified_Currency_gain_factor)
      + 生産効率ボーナス(production_factory_max_efficiency_factor × 0.5)
      + 消費財係数(consumer_goods_factor × 0.5)
      + 戦時ペナルティ(-1.5% × 月数 × (1 - 戦争支持率×0.5))
      + 経済同盟ボーナス(同盟数×10%, 上限30%)
      + 宗教係数(modifier@Unified_Currency_religion_factor)
```

### 詳細実装

**処理場所**: `common/scripted_effects/_bsm_Unified_Currency.txt:25-100`

```hoi4
ucs_add_Unified_Currency_month = {
    if = {
        limit = { has_variable = multiply_value }

        custom_effect_tooltip = tt_ucs_add_Unified_Currency_month
        set_variable = { temp_sum_stabiluty_civilization = stability } # 安定度
        add_to_variable = { temp_sum_stabiluty_civilization = Cultural_Degree } # 安定度+文明

        set_temp_variable = { temp_add_amount = num_of_civilian_factories } # 民需出力
        add_to_temp_variable = { var = temp_add_amount value = 1 } # 民需出力

        multiply_temp_variable = { temp_add_amount = temp_sum_stabiluty_civilization } # 民需出力 * ( 安定度+文明 )

        set_temp_variable = { temp_state_sum = 0 }
        for_each_scope_loop = {
            array = owned_controlled_states
            # SUM{ 人口(m) × (インフラ×1.25 + 飛行場×1.1 + 港湾×0.8) }
            set_temp_variable = { temp_state = state_population_k }
            divide_temp_variable = { temp_state = 1000 } # 人口(m)

            set_temp_variable = { temp_infra_contrib = infrastructure_level }
            multiply_temp_variable = { temp_infra_contrib = 1.25 } # インフラ × 1.25
            set_temp_variable = { temp_air_contrib = building_level@air_base }
            multiply_temp_variable = { temp_air_contrib = 1.1 } # 飛行場 × 1.1
            set_temp_variable = { temp_port_contrib = building_level@naval_base }
            multiply_temp_variable = { temp_port_contrib = 0.8 } # 港湾 × 0.8（海運・貿易）
            add_to_temp_variable = { temp_infra_contrib = temp_air_contrib }
            add_to_temp_variable = { temp_infra_contrib = temp_port_contrib }
            clamp_temp_variable = { var = temp_infra_contrib min = 1.0 } # 最低値1保証

            multiply_temp_variable = { temp_state = temp_infra_contrib }
            add_to_temp_variable = { PREV.temp_state_sum = temp_state }
        }
        multiply_temp_variable = { temp_add_amount = temp_state_sum } # 人口... × 民需出力 × (安定度+文明)
        set_temp_variable = { subtract_value = num_owned_controlled_states^num } # ステート数
        multiply_temp_variable = { subtract_value = deployed_army_manpower_k } # ステート数 * 徴兵(k)
        divide_temp_variable = { subtract_value = 1000 } # ステート数 * 徴兵(m)
        subtract_from_temp_variable = { temp_add_amount = subtract_value }
        divide_temp_variable = { temp_add_amount = 100 } # ... / 100

        # 係数
        set_temp_variable = { var = temp_factor value = 1 }
        add_to_temp_variable = { temp_factor = modifier@Unified_Currency_gain_factor }

        # 生産効率ボーナス（生産最大効率が高いほど経済効率↑）
        set_temp_variable = { temp_production_bonus = modifier@production_factory_max_efficiency_factor }
        multiply_temp_variable = { temp_production_bonus = 0.5 }
        add_to_temp_variable = { temp_factor = temp_production_bonus }

        # 消費財係数（民間経済の活発さ）
        set_temp_variable = { temp_consumer_bonus = modifier@consumer_goods_factor }
        multiply_temp_variable = { temp_consumer_bonus = 0.5 }
        add_to_temp_variable = { temp_factor = temp_consumer_bonus }

        # 戦時下（毎月悪化、戦争支持率で最大50%軽減）
        if = {
            limit = { has_variable = ucs_war_month_counter }
            set_temp_variable = { temp_war_penalty = ucs_war_month_counter }
            multiply_temp_variable = { var = temp_war_penalty value = -0.015 } # 毎月-1.5%
            set_temp_variable = { temp_ws_mitigation = war_support }
            multiply_temp_variable = { temp_ws_mitigation = -0.5 }
            add_to_temp_variable = { temp_ws_mitigation = 1 }
            multiply_temp_variable = { temp_war_penalty = temp_ws_mitigation }
            add_to_temp_variable = { temp_factor = temp_war_penalty }
        }

        # 経済同盟ボーナス（1陣営+10%、上限+30%）
        if = {
            limit = { check_variable = { economic_alliance_count > 0 } }
            set_temp_variable = { temp_alliance_bonus = economic_alliance_count }
            multiply_temp_variable = { var = temp_alliance_bonus value = 0.10 }
            clamp_temp_variable = { var = temp_alliance_bonus min = 0 max = 0.30 }
            add_to_temp_variable = { temp_factor = temp_alliance_bonus }
        }

        multiply_temp_variable = { temp_add_amount = temp_factor }
        add_to_variable = { Unified_Currency = temp_add_amount }
    }
}
```

## 主要因の解説

### 1. 人口とインフラ

**計算**: 各ステートごとに計算

```
ステート寄与 = 人口(m) × (インフラ×1.25 + 飛行場×1.1 + 港湾×0.8)
```

**最低値保障**: インフラ・飛行場・港湾の合計が1.0未満の場合、1.0として扱う

**解説**:
- 人口が多いほど経済活動が活発になり、統一通貨獲得量が増加
- インフラ、飛行場、港湾はそれぞれ異なる重み付け
  - インフラ (1.25): 最も重視される。道路、鉄道など経済活動の基盤
  - 飛行場 (1.1): 空輸、観光など
  - 港湾 (0.8): 海運、貿易など

### 2. 民需出力

**計算**: 民需工場数 + 1

**解説**:
- 民需工場が多いほど、経済生産力が高くなる
- +1されているのは、最低値の保証

### 3. 安定度と文明度

**計算**: 安定度 + 文明度

**解説**:
- 安定度が高いと、国内が安定しており、経済活動が活発
- 文明度が高いと、文化的・技術的発展があり、経済効率が向上

### 4. 徴兵とステート数

**計算**: 徴兵(m) × ステート数

**解説**:
- 徴兵人数が多いほど、経済活動に従事する人口が減少
- ステート数が多いほど、管理コストが増加
- この値は統一通貨獲得量から引かれる

### 5. 係数の各要素

#### 5.1 基本値

- **初期値**: 1.0

#### 5.2 UC獲得補正

**modifier**: `Unified_Currency_gain_factor`

**影響**: 直接的に加算される

#### 5.3 生産効率ボーナス

**modifier**: `production_factory_max_efficiency_factor`

**計算**: 最大生産効率 × 0.5

**解説**:
- 生産効率が高い工場は、より効率的に生産できるため、経済効率が向上
- 最大100%のボーナスがあっても、係数としては+0.5

#### 5.4 消費財係数

**modifier**: `consumer_goods_factor`

**計算**: 消費財係数 × 0.5

**解説**:
- 消費財比率が高いことは、民間経済が活発であることを示す
- 民間消費が多いほど、経済活動が活発になり、統一通貨獲得量が増加

#### 5.5 戦時ペナルティ

**計算**:

```
戦時ペナルティ = 戦争月数 × -1.5% × (1 - 戦争支持率 × 0.5)
```

**解説**:
- 戦争が長引くほど、経済に負担がかかる
- 戦争支持率が高いと、国民が戦争を支持しているため、ペナルティが軽減
  - 戦争支持率100%の場合: ペナルティ × (1 - 0.5) = ペナルティ × 0.5（50%軽減）
  - 戦争支持率0%の場合: ペナルティ × (1 - 0) = ペナルティ（軽減なし）

#### 5.6 経済同盟ボーナス

**計算**:

```
経済同盟ボーナス = 経済同盟数 × 10%
経済同盟ボーナスの上限 = 30%
```

**解説**:
- 経済同盟に参加すると、貿易などの経済活動が活発になるため、ボーナスが発生
- 最大3つの経済同盟に参加しても、ボーナスは30%で止まる

#### 5.7 宗教係数

**modifier**: `Unified_Currency_religion_factor`

**影響**: 宗教によって異なるボーナスが加算される

### 6. 従属国ペナルティ

従属国は、自治度に応じてペナルティを受ける。

**処理場所**: `common/scripted_effects/_bsm_Unified_Currency.txt:106-249`

**テーブル**:

| Tier | 従属状態 | ペナルティ | 自治度 |
|------|---------|-----------|--------|
| 1 | 完全支配 | -30% | 0.0 |
| 2 | 高統制 | -24% | 0.1-0.3 |
| 3 | 中統制 | -18% | 0.3-0.5 |
| 4 | 低統制 | -10% | 0.5-0.65 |
| 5 | 緩やか | -5% | 0.65-0.8 |
| 6 | 名目的 | -2% | 0.8+ |

**解説**:
- 自治度が低い（宗主国の統制が強い）ほど、ペナルティが大きい
- 完全支配されている国は、独自の経済活動がほぼ不可能

## 初期化

**処理場所**: `common/scripted_effects/_bsm_Unified_Currency.txt:8-22`

```hoi4
ucs_first_setting = {
    if = {
        limit = { NOT = { has_country_flag = stop_Unified_Currency_gain } }
        set_variable = { var = Unified_Currency value = 0 } # リセット
        set_variable = { var = Unified_Currency_Last_Month_gain value = 0 } # リセット
        set_variable = { var = Unified_Currency_state_loss value = 0 } # リセット
        set_variable = { var = ucs_war_month_counter value = 0 } # 戦時カウンターリセット
        set_temp_variable = { var = multiply_value value = 6 } # 初期値は6ヶ月分
        ucs_add_Unified_Currency_month = yes
    }
}
```

**解説**:
- ゲーム開始時、6ヶ月分の統一通貨を獲得
- 変数は全て0からスタート

## 週次処理

**処理場所**: `common/on_actions/_bsm_system.txt:367-372`

```hoi4
on_daily = {
    effect = {
        # 獲得補正の計算
        combined_unified_currency = yes
    }
}
```

**解説**:
- 毎日、統一通貨が獲得される

## 主要な消費先

統一通貨は、以下のような用途で消費されます：

1. **探検隊派遣**: ステラリス要素システムで探検隊を派遣
2. **未知の解明**: アノマリー研究など
3. **商業探検隊**: 商業探検隊の成功率に影響
4. **金への変換**: 特定の決定で金に変換可能

## 関連ファイル

### スクリプト効果
- `common/scripted_effects/_bsm_Unified_Currency.txt` - 統一通貨計算
- `common/scripted_effects/bsm_ea_goals_effects.txt` - 経済同盟信頼度計算

### オンアクション
- `common/on_actions/_bsm_system.txt` - 日次処理

### アイデア
- `common/ideas/_bsm_system.txt` - modifierを持つアイデア

### ローカライズ
- `common/modifier_definitions/_bsm_core.txt` - modifier定義
- `localisation/japanese/bakasekai/bsm_system_l_japanese.yml` - 日本語ローカライズ

## 効率的な運用方法

1. **民需工場の増設**: 民需出力を上げる
2. **インフラの整備**: 特に道路（インフラ）を優先的に整備
3. **安定度と文明度の向上**: 国内を安定させ、文明を発展させる
4. **消費財比率の適切化**: 民間経済を活発にする
5. **経済同盟への参加**: 貿易などの経済活動を活発にする
6. **戦争の短期化**: 戦争が長引くと経済に負担がかかる

## 注意事項

1. **初期値**: ゲーム開始時、6ヶ月分の統一通貨を獲得
2. **従属国の影響**: 自治度が低い従属国は、経済力が大幅に制限される
3. **戦争の影響**: 戦争が長引くと、経済に大きな負担がかかる
4. **人口の重要性**: 人口が多いほど、経済活動の規模が大きくなる
5. **文明度との連携**: 文明度が高いと、統一通貨の獲得効率が向上
