# ai_equipment リファレンス(装備設計AI)

AIが戦車・艦船・航空機をモジュール式デザイナーで設計するルール(NSB/MtG/BBA式)。
配置: `common/ai_equipment/*.txt`(国別は `TAG_tank.txt` / `TAG_naval.txt` 等)

プレイヤー/OOB用の固定variantは `hoi4-unit-design-creator` / `hoi4-naval-oob-editor` スキルの領分。
**AI自身に設計させる**場合のみこのファイル群を使う。

## ファイル構造(mod内 generic_naval.txt 準拠)

トップレベルは「設計グループ」、その中に個別デザイン定義。

```
destroyers = {                       # 設計グループ名
  category = naval                   # naval / land / air

  roles = {                          # このグループが満たすロール
    naval_screen
  }

  priority = {                       # グループ全体の設計優先度
    factor = 2500
    modifier = {
      factor = 2
      is_major = no
    }
  }

  screen_default = {                 # 個別デザイン定義
    priority = {
      factor = 250
      modifier = {
        factor = 10
        is_major = no
      }
    }

    role_icon_index = 2              # 設計に付くロールアイコン

    enable = { ... }                 # (任意)このデザインを使う条件

    target_variant = {
      match_value = 2000.0           # 既存設計との一致スコア要求値

      type = ship_hull_light         # ベース装備(hull/chassis/airframe)
      modules = {                    # スロット = モジュール
        fixed_ship_battery_slot = ship_light_battery
        fixed_ship_fire_control_system_slot = ship_fire_control_system
        fixed_ship_radar_slot = ship_sonar
        fixed_ship_engine_slot = light_ship_engine
        fixed_ship_torpedo_slot = ship_torpedo
        rear_1_custom_slot = ship_depth_charge
      }
    }
  }
}
```

## 主要フィールド

| フィールド | 意味 |
|---|---|
| `category` | `naval` / `land` / `air` |
| `roles` | 充足するロール。陸: `tank_role` 系、海: `naval_screen`/`naval_capital`等、空: `air_fighter`等 |
| `priority` | どのグループ/デザインから設計するか。majorと minor で factor を分けるのが定番 |
| `target_variant` | 目標設計。`type` + `modules`(+ `upgrades`) |
| `match_value` | 既存variantがこのスコアを超えて一致すれば再設計しない |
| `requirements` | (任意)`module_not = X` 等の制約 |
| `enable` | デザインの有効条件(技術・年代分岐に使う) |

## モジュール指定の書き方

- スロット名・モジュール名は `common/units/equipment/modules/*.txt` と vanilla の定義に一致させる
- 技術レベルで分岐させたい場合は同グループ内に `*_early` / `*_late` のデザインを並べ、`enable` / `priority` の modifier で `has_tech` を見る
- モジュール値に `= current` を指定すると「研究済み最新」を使わせられる(vanillaパターン。使用前にvanilla `common/ai_equipment/` で書式確認)

## 新規国家に装備設計AIを足す手順

1. 既存の `generic_*.txt` でカバーされるか確認(genericはfallback。国別ファイルがあると優先される)
2. 国別にする場合 `TAG_tank.txt` / `TAG_naval.txt` を新規作成し、mod内の `JAP_tank.txt` 等を雛形にする
3. 必要モジュールの研究を `ai_strategy_plans` の `research` でカバーする(研究されないモジュールは使われない)
4. 海軍の場合、設計と艦隊運用はセット: [ai_navy_reference.md](ai_navy_reference.md) のtaskforce要求と整合させる

## 注意点

- 国別ファイルが存在する国にgenericの設計が混ざることがある。意図的に排他するなら priority の modifier で `tag` を見る
- `match_value` が低すぎるとAIが粗悪な既存設計を使い回し、高すぎると毎回再設計して陸軍/海軍経験値を浪費する
- AIの設計には経験値(army/navy/air XP)が必要。XPが無い場合は `ai_strategy` の `land_xp_spend_priority` 等で配分を調整

## mod内実例

- `bakasekai/common/ai_equipment/generic_naval.txt`, `generic_planes.txt`
- `bakasekai/common/ai_equipment/JAP_naval.txt`, `JAP_tank.txt`
- `bakasekai/common/ai_equipment/GER_tank.txt`, `SOV_tank.txt`, `USA_tank.txt` ほか
