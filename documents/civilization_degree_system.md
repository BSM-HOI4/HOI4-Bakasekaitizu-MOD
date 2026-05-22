# 文明度システム (Cultural Degree System)

## 概要

文明度システムは、国家の文化的・技術的発展度を表すシステムです。0%から100%までの値で表され、様々なゲームシステムと連動しています。

### 変数名
- `Cultural_Degree` (0-100)

### 基本特性
- **初期値**: 0%
- **最小値**: 0%
- **最大値**: 100%
- **更新頻度**: 週次 (weekly)

## システム詳細

### 週次増減

**処理場所**: `common/on_actions/_bsm_system.txt:376-379`

```hoi4
every_country = {
    # 文明度の上昇
    add_to_variable = {
        Cultural_Degree = modifier@weekly_Cultural_Degree
    }
}
```

**関連変数**:
- `weekly_Cultural_Degree` - 週次増減量 (modifierとして使用)

**増減要因**:
- 国民精神 (`base_Cultural_Degree`)
- 政治顧問
- 宗教
- アノマリー報酬
- 伝統・アセンションパーク

### 特性スロット解放

文明度に応じて、ステラリス要素システムの特性（Traits）スロットが解放されます。

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

**解放条件**:
| 文明度 | 特性スロット数 |
|--------|---------------|
| 0-29% | 0スロット |
| 30-49% | 1スロット |
| 50-79% | 3スロット |
| 80-99% | 5スロット |
| 100% | 6スロット |

### 国家統合力への影響

文明度は国家統合力（National_Unity_Power）の獲得に寄与します。

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

### 統一通貨への影響

統一通貨の計算式に文明度が含まれます。

**処理場所**: `common/scripted_effects/_bsm_Unified_Currency.txt:30-31`

```hoi4
set_variable = { temp_sum_stabiluty_civilization = stability } # 安定度
add_to_variable = { temp_sum_stabiluty_civilization = Cultural_Degree } # 安定度+文明
```

**影響**:
- 安定度と文明度の合計値が民需出力に乗算される
- 文明度が高いほど、統一通貨の獲得量が増加

### アノマリー研究への影響

文明度はアノマリー研究の解禁条件と研究速度に影響します。

**解禁条件**: `common/scripted_triggers/_bsm_stellaris_triggers.txt:9-27`

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

**解禁テーブル**:
| 文明度 | 研究可能なアノマリー難易度 |
|--------|---------------------------|
| 20%以上 | 全難易度（制限なし） |
| 40%以上 | 困難(60)以下 |
| 60%以上 | 中等(60)以下 |
| 80%以上 | 簡単(40)以下 |

**研究速度ボーナス**: `common/scripted_effects/_bsm_stellaris_anomaly_integration.txt:57-61`

```hoi4
bsm_stellaris_anomaly_research_speed_calc = {
    set_temp_variable = { t_cd = Cultural_Degree }
    divide_temp_variable = { t_cd = 100 }

    set_variable = { bsm_stellaris_anomaly_research_bonus = t_cd }
    # ... 他のボーナス計算
}
```

**ボーナス計算**:
- 文明度 × 0.01（最大0.5）
- 例：文明度50%の場合、+50%の研究速度ボーナス

## 主要な獲得・消費要因

### 獲得要因

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
    # ...
}
```

**伝統・アセンションパーク**:

| アイテム | 文明度獲得量 |
|---------|--------------|
| 文明伝統 Lv1 | +5% |
| 文明伝統 Lv4 | +10% |
| 文明伝統 Lv5 | +15% |
| 社会伝統 Lv4 | +5% |
| 社会伝統 Lv5 | +10% |
| 特性「文化的遺産」 | +10% |
| アセンションパーク「精神的開花」 | +25% |

**特定アノマリー効果**:

| アノマリー | 効果 |
|-----------|------|
| バカ教育改革の資料 | +5%（恒久） |
| 北極ポーランド公文書 | +8（即時） |
| 知識集約型研究所 | 解析中は-10% |

### 消費・減少要因

| 要因 | 減少量 | 備考 |
|------|--------|------|
| 知識集約型研究所（解析中） | -10 | 一時的 |
| 原始回帰プロセス（解析中） | -20 | 一時的 |
| 南極封印破損（解析中） | 安定度-30% | 文明度には直接影響なし |

## 他システムとの連携

### 経済同盟信頼度計算

**処理場所**: `common/scripted_effects/bsm_ea_goals_effects.txt:119-148`

```hoi4
bsm_ea_calculate_trust = {
    set_temp_variable = { t_trust = 0 }

    # 文明度 (0~1) × 50
    if = {
        limit = { has_variable = Cultural_Degree }
        set_temp_variable = { t_cd = Cultural_Degree }
        multiply_temp_variable = { t_cd = 50 }
        add_to_temp_variable = { t_trust = t_cd }
    }
    # ...
}
```

**影響**:
- 文明度 × 50 が信頼度に加算
- 文明度100%の場合、信頼度+50

## 関連ファイル

### スクリプト効果
- `common/scripted_effects/_bsm_stellaris_effects.txt` - 特性スロット更新
- `common/scripted_effects/_bsm_stellaris_anomaly_integration.txt` - アノマリー報酬・研究速度
- `common/scripted_effects/_bsm_Unified_Currency.txt` - 統一通貨計算
- `common/scripted_effects/bsm_ea_goals_effects.txt` - 経済同盟信頼度

### トリガー
- `common/scripted_triggers/_bsm_stellaris_triggers.txt` - アノマリー解禁判定

### オンアクション
- `common/on_actions/_bsm_system.txt` - 週次処理

### アイデア
- `common/ideas/_bsm_system.txt` - `base_Cultural_Degree` modifierを持つアイデア

### ローカライズ
- `common/modifier_definitions/_bsm_core.txt` - modifier定義
- `localisation/japanese/bakasekai/bsm_system_l_japanese.yml` - 日本語ローカライズ

## チート用決定

デバッグ用として、文明度を設定する決定が存在します。

**場所**: `common/decisions/_debug_decisions.txt:390-397`

```hoi4
debug_cd_set = {
    icon = generic_independence
    fire_only_once = no
    remove_effect = {
        set_variable = { var = Cultural_Degree value = 0.8 }
    }
}
```

## 注意事項

1. **初期化**: ゲーム開始時、文明度は0からスタート
2. **上限**: 100%を超えないように処理が必要（`clamp_variable`などを使用）
3. **影響範囲**: 多くのシステムに影響するため、変動時は全体的なバランスを考慮
