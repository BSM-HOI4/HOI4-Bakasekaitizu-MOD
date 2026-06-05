# ステラリス要素システム (Stellaris Elements System)

> 注: このファイルは旧4伝統時代の参考資料を含みます。現行の地球版・思想連動型仕様は [stellaris_earth_ideology_system.md](./stellaris_earth_ideology_system.md) を正としてください。

## 概要

ステラリス要素システムは、BSMmodにStellaris（ゲーム名）の要素を取り入れたシステムです。伝統（Traditions）、特性（Traits）、アセンションパーク（Ascension Perks）、探検隊（Expeditions）、アノマリー（Anomalies）を管理し、文明度（Cultural_Degree）と国家統合力（National_Unity_Power）と密接に関連しています。

### 主な変数名

**伝統**:
- `bsm_stellaris_tradition_economy` (0-5)
- `bsm_stellaris_tradition_military` (0-5)
- `bsm_stellaris_tradition_society` (0-5)
- `bsm_stellaris_tradition_civilization` (0-5)
- `bsm_stellaris_ascension_adopted` (0-20) - 伝統取得数の合計
- `bsm_stellaris_ascension_slots` (0-8) - 利用可能なアセンションパークスロット

**特性**:
- `bsm_stellaris_trait_slots` (0-6) - 文明度に応じて変動
- `bsm_stellaris_traits_equipped` (0-6) - 現在装備している特性数

**探検隊**:
- `bsm_stellaris_expedition_count` (0-∞) - 探検隊派遣数
- `bsm_stellaris_expedition_active` (0-∞) - 活動中の探検隊数

**アノマリー**:
- `bsm_stellaris_anomaly_research_bonus` (0.01-0.5) - アノマリー研究速度ボーナス

### 基本特性
- **初期化**: `on_startup` で `bsm_stellaris_init` を実行
- **更新頻度**: 週次（特性スロット更新、アノマリー研究速度計算）

## システム構成

### 1. 初期化

**処理場所**: `common/scripted_effects/_bsm_stellaris_effects.txt:9-44`

```hoi4
bsm_stellaris_init = {
  if = {
    limit = { NOT = { has_global_flag = bsm_stellaris_initialized } }
    set_global_flag = bsm_stellaris_initialized

    every_country = {
      bsm_stellaris_country_init = yes
    }
  }
}

bsm_stellaris_country_init = {
  set_variable = { bsm_stellaris_tradition_economy = 0 }
  set_variable = { bsm_stellaris_tradition_military = 0 }
  set_variable = { bsm_stellaris_tradition_society = 0 }
  set_variable = { bsm_stellaris_tradition_civilization = 0 }

  set_variable = { bsm_stellaris_ascension_adopted = 0 }
  set_variable = { bsm_stellaris_ascension_slots = 0 }

  set_variable = { bsm_stellaris_essence_energy = 0 }
  set_variable = { bsm_stellaris_essence_minerals = 0 }
  set_variable = { bsm_stellaris_essence_info = 0 }

  set_variable = { bsm_stellaris_trait_slots = 0 }
  set_variable = { bsm_stellaris_traits_equipped = 0 }

  set_variable = { bsm_stellaris_anomaly_research_bonus = 0 }
  set_variable = { bsm_stellaris_anomaly_research_field = 0 }
  set_variable = { bsm_stellaris_anomaly_difficulty_level = 0 }

  set_variable = { bsm_stellaris_expedition_count = 0 }
  set_variable = { bsm_stellaris_expedition_active = 0 }

  bsm_stellaris_update_trait_slots = yes
}
```

### 2. 特性スロット更新

文明度に応じて特性スロット数を更新します。

**処理場所**: `common/scripted_effects/_bsm_stellaris_effects.txt:49-68`

```hoi4
bsm_stellaris_update_trait_slots = {
  set_variable = { bsm_stellaris_trait_slots = 0 }

  if = {
    limit = { check_variable = { var = Cultural_Degree value = 30 compare = greater_than_or_equals } }
    set_variable = { bsm_stellaris_trait_slots = 1 }
  }
  if = {
    limit = { check_variable = { var = Cultural_Degree value = 50 compare = greater_than_or_equals } }
    set_variable = { bsm_stellaris_trait_slots = 3 }
  }
  if = {
    limit = { check_variable = { var = Cultural_Degree value = 80 compare = greater_than_or_equals } }
    set_variable = { bsm_stellaris_trait_slots = 5 }
  }
  if = {
    limit = { check_variable = { var = Cultural_Degree value = 100 compare = greater_than_or_equals } }
    set_variable = { bsm_stellaris_trait_slots = 6 }
  }
}
```

**更新頻度**: 週次 (`on_weekly` で実行)

### 3. 伝統取得

国家統合力を消費して伝統を取得します。

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
    if = {
      limit = { check_variable = { var = bsm_stellaris_tradition_category value = 2 compare = equals } }
      if = {
        limit = { check_variable = { var = bsm_stellaris_tradition_military value = 5 compare = less_than } }
        add_to_variable = { bsm_stellaris_tradition_military = 1 }
        add_ideas = bsm_stellaris_tradition_military_@var:bsm_stellaris_tradition_military
      }
    }
    if = {
      limit = { check_variable = { var = bsm_stellaris_tradition_category value = 3 compare = equals } }
      if = {
        limit = { check_variable = { var = bsm_stellaris_tradition_society value = 5 compare = less_than } }
        add_to_variable = { bsm_stellaris_tradition_society = 1 }
        add_ideas = bsm_stellaris_tradition_society_@var:bsm_stellaris_tradition_society
      }
    }
    if = {
      limit = { check_variable = { var = bsm_stellaris_tradition_category value = 4 compare = equals } }
      if = {
        limit = { check_variable = { var = bsm_stellaris_tradition_civilization value = 5 compare = less_than } }
        add_to_variable = { bsm_stellaris_tradition_civilization = 1 }
        add_ideas = bsm_stellaris_tradition_civilization_@var:bsm_stellaris_tradition_civilization
      }
    }

    bsm_stellaris_update_tradition_count = yes
  }
}
```

**伝統カテゴリ**:
1. 経済伝統
2. 軍事伝統
3. 社会伝統
4. 文明伝統

### 4. アセンションパーク

伝統を一定数取得すると、アセンションパークを取得できるようになります。

**条件**: 伝統10つ取得ごとに1スロット解放（最大8スロット）

**処理場所**: `common/scripted_effects/_bsm_stellaris_effects.txt:123-144`

```hoi4
bsm_stellaris_update_tradition_count = {
  set_variable = { t_total = 0 }
  add_to_variable = { t_total = bsm_stellaris_tradition_economy }
  add_to_variable = { t_total = bsm_stellaris_tradition_military }
  add_to_variable = { t_total = bsm_stellaris_tradition_society }
  add_to_variable = { t_total = bsm_stellaris_tradition_civilization }
  set_variable = { bsm_stellaris_ascension_adopted = t_total }

  set_variable = { t_slots = 0 }

  if = {
    limit = { check_variable = { var = bsm_stellaris_ascension_adopted value = 10 compare = greater_than_or_equals } }
    add_to_variable = { t_slots = 1 }
  }
  if = {
    limit = { check_variable = { var = bsm_stellaris_ascension_adopted value = 20 compare = greater_than_or_equals } }
    add_to_variable = { t_slots = 1 }
  }
  # ... 80まで継続

  clamp_variable = { t_slots = 0 max = 8 }
  set_variable = { bsm_stellaris_ascension_slots = t_slots }
}
```

**アセンションパークの効果**:
1. 科学の頂点: 研究速度 +30%
2. 軍事機甲: 陸軍攻撃 +20%, 海軍攻撃 +20%, 空軍攻撃 +20%
3. 経済巨人: 民需工場出力 +25%, 軍需工場出力 +25%
4. 理想社会: 安定度 +20%, 戦争協力度 +20%
5. 精神的開花: 文明度 +25%
6. 外交の達人: 外交力 +1.0, 緊張度低減 +40%
7. アノマリーの探求者: アノマリー研究速度 +50%
8. 世界の覇者: 全研究速度 +10%, 全出力 +10%, 安定度 +10%

### 5. 特性（Traits）

文明度によって解放されたスロットに特性を装備できます。

**処理場所**: `common/scripted_effects/_bsm_stellaris_effects.txt:166-193`

```hoi4
bsm_stellaris_equip_trait = {
  if = {
    limit = {
      check_variable = { var = bsm_stellaris_traits_equipped value = bsm_stellaris_trait_slots compare = less_than }
      check_variable = { var = bsm_stellaris_trait_id value = 1 compare = equals }
      NOT = { has_idea = bsm_stellaris_trait_aggressive }
    }
    add_ideas = var:bsm_stellaris_trait_token
    add_to_variable = { bsm_stellaris_traits_equipped = 1 }
  }
}

bsm_stellaris_unequip_trait = {
  if = {
    limit = {
      check_variable = { var = bsm_stellaris_trait_id value = 1 compare = equals }
      has_idea = bsm_stellaris_trait_aggressive
    }
    remove_ideas = var:bsm_stellaris_trait_token
    subtract_from_variable = { bsm_stellaris_traits_equipped = 1 }
  }
}
```

**固定特性**:
- 好戦的: 戦争支持度 +10%, 陸軍経験値 +20%
- 平和的: 世界緊張度への影響 -20%, 外交力 +0.2
- 拡張主義: 占領コスト -15%, 外交的包囲獲得 +20%
- 孤立主義: 請求権捏造コスト -25%, 外交的包囲獲得 -20%
- 霊主義的: 安定度 +10%, 政治力獲得 +15%
- 唯物主義的: 研究速度 +10%, 民需工場出力 +5%

**追加特性**:
- 技術的に進歩している: 研究速度 +15%
- 軍国主義者: 陸軍経験値 +30%, 海軍経験値 +30%
- 外交的: 外交力 +0.5, 緊張度低減 +25%
- 環境配慮: 安定度 +15%, 戦争協力度 +10%
- 工業力: 民需工場出力 +15%, 軍需工場出力 +10%
- 文化的遺産: 文明度 +10%, 政治力獲得 +20%
- 科学的ブレークスルー: 研究速度 +25%
- 戦争に栄光あり: 戦争支持度 +15%, 組織度回復 +25%
- 貿易の拠点: 外交力 +0.3, 資源獲得 +10%
- 海軍至上主義: 海軍経験値 +40%, 海軍攻撃 +10%

### 6. 探検隊（Expeditions）

国家統合力を消費して探検隊を派遣し、60日後に帰還します。

**コスト**: 50統合力 / 探検隊

**処理場所**: `common/scripted_effects/_bsm_stellaris_effects.txt:198-238`

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

**探検隊タイプ**:
1. 学術調査隊: 文明度に応じた成功率、新アノマリー発見確率 +10%
2. 軍事偵察隊: 統合力に応じた成功率、軍事関連発見確率 +10%
3. 商業探検隊: 統一通貨に応じた成功率、経済関連発見確率 +10%
4. 科学調査隊: 研究関連発見確率 +10%

**報酬**:
- 新アノマリー (30%)
- エッセンシャル (30%)
- 新特性 (20%)
- 統合力100 (20%)

### 7. アノマリー（Anomalies）

文明度に応じて研究が可能になり、研究速度は文明度と伝統によって増加します。

**解禁条件**: 文明度に応じたアノマリー難易度

**処理場所**: `common/scripted_triggers/_bsm_stellaris_triggers.txt:9-27`

```hoi4
bsm_stellaris_anomaly_can_research = {
  OR = {
    AND = {
      check_variable = { var = Cultural_Degree value = 20 compare = greater_than_or_equals }
    }
    AND = {
      check_variable = { var = Cultural_Degree value = 40 compare = greater_than_or_equals }
      check_variable = { var = anomaly_difficulty value = 85 compare = less_than }
    }
    AND = {
      check_variable = { var = Cultural_Degree value = 60 compare = greater_than_or_equals }
      check_variable = { var = anomaly_difficulty value = 60 compare = less_than }
    }
    AND = {
      check_variable = { var = Cultural_Degree value = 80 compare = greater_than_or_equals }
      check_variable = { var = anomaly_difficulty value = 40 compare = less_than }
    }
  }
}
```

**研究速度計算**: `common/scripted_effects/_bsm_stellaris_anomaly_integration.txt:57-79`

```hoi4
bsm_stellaris_anomaly_research_speed_calc = {
    set_temp_variable = { t_cd = Cultural_Degree }
    divide_temp_variable = { t_cd = 100 }

    set_variable = { bsm_stellaris_anomaly_research_bonus = t_cd }

    set_temp_variable = { t_economy = bsm_stellaris_tradition_economy }
    multiply_temp_variable = { t_economy = 0.05 }
    add_to_variable = { bsm_stellaris_anomaly_research_bonus = t_economy }

    set_temp_variable = { t_military = bsm_stellaris_tradition_military }
    multiply_temp_variable = { t_military = 0.05 }
    add_to_variable = { bsm_stellaris_anomaly_research_bonus = t_military }

    set_temp_variable = { t_society = bsm_stellaris_tradition_society }
    multiply_temp_variable = { t_society = 0.05 }
    add_to_variable = { bsm_stellaris_anomaly_research_bonus = t_society }

    set_temp_variable = { t_civilization = bsm_stellaris_tradition_civilization }
    multiply_temp_variable = { t_civilization = 0.05 }
    add_to_variable = { bsm_stellaris_anomaly_research_bonus = t_civilization }

    clamp_variable = { bsm_stellaris_anomaly_research_bonus = 0.01 max = 0.5 }
}
```

**研究速度ボーナスの構成**:
- 文明度 × 0.01
- 各伝統 × 0.05
- 合計: 0.01（最小）〜 0.5（最大）

**アノマリー報酬**: `common/scripted_effects/_bsm_stellaris_anomaly_integration.txt:9-52`

```hoi4
bsm_stellaris_anomaly_tradition_bonus = {
    random = {
        chance = 5
        add_to_variable = { Cultural_Degree = 2 }
    }
    random = {
        chance = 8
        add_to_variable = { Cultural_Degree = 4 }
    }
    random = {
        chance = 12
        add_to_variable = { Cultural_Degree = 6 }
    }
    random = {
        chance = 15
        add_to_variable = { Cultural_Degree = 8 }
    }
    random = {
        chance = 5
        add_ideas = bsm_stellaris_trait_available_technologically_advanced
    }
    # ...
}
```

**報酬**:
- 文明度 (2, 4, 6, 8)
- 統合力 (25, 50, 75, 100)
- 新特性解放

## 文明度・統合力との関係

### 文明度の影響

1. **特性スロット解放**: 30%→1スロット, 50%→3スロット, 80%→5スロット, 100%→6スロット
2. **アノマリー解禁**: 文明度が高いほど難易度の高いアノマリーが研究可能
3. **アノマリー研究速度**: 文明度 × 0.01 のボーナス
4. **統合力獲得**: 毎週、文明度の値が統合力に加算
5. **統一通貨獲得**: 安定度と文明度の合計が民需出力に乗算される

### 統合力の影響

1. **伝統取得**: 100統合力 / 伝統
2. **探検隊派遣**: 50統合力 / 探検隊
3. **アノマリー報酬**: 25-100の統合力獲得チャンス
4. **探検隊成功率**: 軍事偵察隊の成功率に影響
5. **経済同盟信頼度**: 統合力 × 0.05 が信頼度に加算

## 関連ファイル

### スクリプト効果
- `common/scripted_effects/_bsm_stellaris_effects.txt` - 伝統・特性・探検隊
- `common/scripted_effects/_bsm_stellaris_anomaly_integration.txt` - アノマリー報酬・研究速度
- `common/scripted_effects/_bsm_stellaris_anomaly_mapping.txt` - アノマリーカテゴリマッピング
- `common/scripted_effects/_bsm_anomaly_system.txt` - アノマリーデータベース
- `common/scripted_effects/_bsm_anomaly_effects.txt` - アノマリー研究進行

### トリガー
- `common/scripted_triggers/_bsm_stellaris_triggers.txt` - アノマリー解禁判定

### 決定
- `common/decisions/_bsm_stellaris_decisions.txt` - 伝統取得決定

### GUI
- `common/scripted_guis/bsm_stellaris.txt` - 研究・発見画面

### アイデア
- `common/ideas/_bsm_stellaris_traits_detailed.txt` - 伝統・特性アイデア

### ローカライズ
- `localisation/japanese/bakasekai/_bsm_stellaris_l_japanese.yml` - 日本語ローカライズ

### オンアクション
- `common/on_actions/_bsm_system.txt` - 週次処理（特性スロット更新、アノマリー研究速度計算）

## 効率的な運用方法

1. **文明度の優先**: 特性スロットを解放し、アノマリー研究を可能にする
2. **統合力の確保**: 伝統取得と探検隊派遣のバランスを考える
3. **伝統の選択**: 経済・軍事・社会・文明伝統をバランスよく取得
4. **特性の選択**: プレイスタイルに合わせて特性を装備
5. **アノマリー研究**: 報酬からの文明度・統合力獲得を狙う
6. **探検隊の派遣**: 新特性やアノマリーを発見する

## 注意事項

1. **初期化**: ゲーム開始時、全ての変数が0からスタート
2. **特性スロット**: 文明度が低いと特性を装備できない
3. **伝統のコスト**: 伝統1つにつき100統合力を消費
4. **アセンションパーク**: 伝統10つ取得ごとに1スロット解放（最大8スロット）
5. **アノマリー研究**: 文明度が低いと高難易度のアノマリーが研究できない
6. **週次処理**: 特性スロットとアノマリー研究速度は毎週更新される
