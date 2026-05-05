# 国家統合力システム (National Unity Power System)

## 概要

国家統合力システムは、国家の統合度を表すリソースです。伝統取得、探検隊派遣など、様々なアクションのコストとして使用されます。文明度システムと密接に関連しています。

### 変数名
- `National_Unity_Power` (0-∞)

### 基本特性
- **初期値**: 0
- **最小値**: 0
- **最大値**: なし（上限なし）
- **更新頻度**: 日次 (daily)

## システム詳細

### 日次獲得

**処理場所**: 毎日 `modifier@daily_National_Unity_Power_gain` に基づいて獲得

**関連modifier**:
- `daily_National_Unity_Power_gain` - 日次獲得量
- `National_Unity_Power_gain_factor` - 獲得補正

**獲得要因**:
- 国民精神
- 政治顧問
- 宗教
- 特定の国家方針

### 週次獲得（文明度連動）

文明度に応じて毎週統合力を獲得します。

**処理場所**: `common/on_actions/_bsm_system.txt:380-383`

```hoi4
every_country = {
    # 国家統合力に文明度を追加
    add_to_variable = {
        National_Unity_Power = Cultural_Degree
    }
}
```

**影響**:
- 毎週、文明度の値が国家統合力に加算される
- 文明度50%の場合、毎週50の統合力を獲得

## 主な消費先

### 伝統取得

ステラリス要素システムの伝統（Traditions）を取得するために消費します。

**コスト**: 100統合力 / 伝統

**処理場所**: `common/scripted_effects/_bsm_stellaris_effects.txt:73-118`

```hoi4
bsm_stellaris_unlock_tradition = {
  if = {
    limit = {
      has_variable = bsm_stellaris_tradition_category
      has_variable = bsm_stellaris_tradition_cost
      has_variable = National_Unity_Power
    }

    subtract_from_variable = { National_Unity_Power = 100 }

    if = {
      limit = { check_variable = { var = bsm_stellaris_tradition_category value = 1 compare = equals } }
      if = {
        limit = { check_variable = { var = bsm_stellaris_tradition_economy value = 5 compare = less_than } }
        add_to_variable = { bsm_stellaris_tradition_economy = 1 }
        add_ideas = bsm_stellaris_tradition_economy_@var:bsm_stellaris_tradition_economy
      }
    }
    # ... 他の伝統カテゴリ
  }
}
```

**伝統カテゴリ**:
- 経済伝統 (5レベル)
- 軍事伝統 (5レベル)
- 社会伝統 (5レベル)
- 文明伝統 (5レベル)

**決定場所**: `common/decisions/_bsm_stellaris_decisions.txt`

```hoi4
bsm_stellaris_unlock_economy_tradition_decision = {
    icon = gfx/interface/icons/ideas/economy.dds
    allowed = { always = yes }
    available = {
      has_variable = National_Unity_Power
      check_variable = { var = National_Unity_Power value = 100 compare = greater_than_or_equals }
      has_variable = bsm_stellaris_tradition_economy
      check_variable = { var = bsm_stellaris_tradition_economy value = 5 compare = less_than }
    }
    complete_effect = {
      set_variable = { bsm_stellaris_tradition_category = 1 }
      set_variable = { bsm_stellaris_tradition_cost = 100 }
      bsm_stellaris_unlock_tradition = yes
    }
}
```

### 探検隊作成

ステラリス要素システムの探検隊を派遣するために消費します。

**コスト**: 50統合力 / 探検隊

**処理場所**: `common/scripted_effects/_bsm_stellaris_effects.txt:198-209`

```hoi4
bsm_stellaris_create_expedition = {
  if = {
    limit = {
      has_variable = bsm_stellaris_expedition_type
      has_variable = National_Unity_Power
      check_variable = { var = National_Unity_Power value = 50 compare = greater_than_or_equals }
    }
    subtract_from_variable = { National_Unity_Power = 50 }
    add_to_variable = { bsm_stellaris_expedition_count = 1 }
    add_to_variable = { bsm_stellaris_expedition_active = 1 }
  }
}
```

**探検隊タイプ**:
- 学術調査隊 (Academic)
- 軍事偵察隊 (Military)
- 商業探検隊 (Commercial)
- 科学調査隊 (Scientific)

### アノマリー報酬

アノマリー研究完了時に統合力を獲得することがあります。

**処理場所**: `common/scripted_effects/_bsm_stellaris_anomaly_integration.txt:9-52`

```hoi4
bsm_stellaris_anomaly_tradition_bonus = {
    random = {
        chance = 10
        add_to_variable = { National_Unity_Power = 25 }
    }
    random = {
        chance = 15
        add_to_variable = { National_Unity_Power = 50 }
    }
    random = {
        chance = 20
        add_to_variable = { National_Unity_Power = 75 }
    }
    random = {
        chance = 25
        add_to_variable = { National_Unity_Power = 100 }
    }
}
```

### 特定アノマリー効果

一部のアノマリーは即時の統合力獲得効果を持っています。

| アノマリー | 統合力獲得量 |
|-----------|--------------|
| バカ教育改革の資料 | +50（即時） |
| きょぬー主義宣言 | +25（即時） |
| 共産民主主義実験 | +150（即時） |

## 他システムとの連携

### 経済同盟信頼度計算

経済同盟システムの信頼度計算に使用されます。

**処理場所**: `common/scripted_effects/bsm_ea_goals_effects.txt:119-148`

```hoi4
bsm_ea_calculate_trust = {
    set_temp_variable = { t_trust = 0 }

    # 統合力 (0~1000+) × 0.05
    if = {
        limit = { has_variable = National_Unity_Power }
        set_temp_variable = { t_po = National_Unity_Power }
        multiply_temp_variable = { t_po = 0.05 }
        add_to_temp_variable = { t_trust = t_po }
    }

    clamp_temp_variable = { var = t_trust min = 0 max = 100 }
    set_variable = { bsm_ea_trust = t_trust }
}
```

**影響**:
- 統合力 × 0.05 が信頼度に加算（最大で100）
- 統合力2000の場合、信頼度+100（最大値）

### 探検隊成功率

一部の探検隊の成功率に影響します。

**軍事偵察隊**:
- 統合力に応じた成功率

## 主要な獲得要因

### アノマリー報酬

| チャンス | 獲得量 |
|---------|--------|
| 10% | +25 |
| 15% | +50 |
| 20% | +75 |
| 25% | +100 |

### 探検隊完了

**処理場所**: `common/scripted_effects/_bsm_stellaris_effects.txt:214-238`

```hoi4
bsm_stellaris_complete_expedition = {
  if = {
    limit = { check_variable = { var = bsm_stellaris_expedition_active value = 0 compare = greater_than } }
    subtract_from_variable = { bsm_stellaris_expedition_active = 1 }

    random = {
      chance = 30
      add_to_array = { AN_analyzed_list = token:AS_AN_International_Oxygen_Documents }
    }
    random = {
      chance = 30
      add_to_variable = { bsm_stellaris_essence_energy = 50 }
      add_to_variable = { bsm_stellaris_essence_minerals = 50 }
      add_to_variable = { bsm_stellaris_essence_info = 25 }
    }
    random = {
      chance = 20
      add_ideas = bsm_stellaris_trait_available
    }
    random = {
      chance = 20
      add_to_variable = { National_Unity_Power = 100 }
    }
  }
}
```

**成功率**: 20%で100統合力獲得

## 関連ファイル

### スクリプト効果
- `common/scripted_effects/_bsm_stellaris_effects.txt` - 伝統・探検隊取得処理
- `common/scripted_effects/_bsm_stellaris_anomaly_integration.txt` - アノマリー報酬
- `common/scripted_effects/bsm_ea_goals_effects.txt` - 経済同盟信頼度計算

### 決定
- `common/decisions/_bsm_stellaris_decisions.txt` - 伝統取得決定

### オンアクション
- `common/on_actions/_bsm_system.txt` - 週次処理（文明度からの加算）

### アイデア
- `common/ideas/_bsm_system.txt` - `daily_National_Unity_Power_gain` modifierを持つアイデア

### ローカライズ
- `common/modifier_definitions/_bsm_core.txt` - modifier定義
- `localisation/japanese/bakasekai/bsm_system_l_japanese.yml` - 日本語ローカライズ

## チート用決定

デバッグ用として、統合力を設定する決定が存在します。

**場所**: `common/decisions/_debug_decisions.txt:398-405`

```hoi4
debug_po_set = {
    icon = generic_independence
    fire_only_once = no
    remove_effect = {
        set_variable = { var = National_Unity_Power value = 0.8 }
    }
}
```

## 注意事項

1. **初期化**: ゲーム開始時、統合力は0からスタート
2. **週次増加**: 文明度に応じて毎週増加するため、文明度の重要性が高い
3. **消費計画**: 伝統（100統合力）と探検隊（50統合力）のバランスを考慮
4. **アノマリー研究**: アノマリー報酬からの統合力獲得チャンスがあるため、積極的に研究を進める価値がある

## 効率的な運用方法

1. **文明度の向上**: 毎週の自動獲得量を増やす
2. **アノマリー研究**: 報酬からの統合力獲得チャンスを狙う
3. **伝統と探検隊のバランス**: コスト対効果を考慮して消費を計画
4. **経済同盟への参加**: 統合力が高いと信頼度も高くなり、同盟メリットが増加
