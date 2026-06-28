# ai_templates リファレンス(師団テンプレート設計AI)

AIが師団テンプレートを設計・改良・置換する際のルール。
配置: `common/ai_templates/*.txt`

## ファイル構造(mod内 generic.txt 準拠)

トップレベルは「ロールグループ」。その中に個別テンプレート定義が並ぶ。

```
armor_generic = {                    # グループ名(一意)
  role = armor                       # このグループが担うロール

  upgrade_prio = {                   # グループ全体のアップグレード優先度
    base = 2
    modifier = {
      factor = 3
      OR = {
        has_tech = basic_medium_tank
        has_tech = basic_medium_tank_chassis
      }
    }
  }

  light_armor_early = {              # 個別テンプレート定義
    upgrade_prio = {
      base = 1
      modifier = { factor = 2 }
    }

    can_upgrade_in_field = {         # 前線配備中でも改良してよい条件
      has_equipment = { light_tank_chassis < 500 }
    }

    target_template = {              # AIに作らせたいテンプレート構成
      support = {
        engineer = 1
        mot_recon = 1
        artillery = 1
        anti_tank = 1
      }
      regiments = {
        light_armor = 5
        motorized = 4
      }
    }

    replace_at_match = 1.5           # 1.0超 = upgrade_prioが上回ったときのみ置換
    replace_with = medium_armor_early # 置換先のテンプレート定義名
    target_min_match = 0.5           # この一致率未満なら新規設計する
  }
}
```

## 設計方式は2種類

### 1. target_template 方式(推奨・BSM標準)

`target_template` で支援中隊と連隊構成を直接指定する。確実に意図どおりの師団になる。
mod内の `ai_templates_continental_major.txt` / `ai_templates_japan_major.txt` / `ai_templates_minor_cost_focus.txt` がこの方式。

### 2. stat_weights 方式(vanilla旧方式)

`target_width` / `width_weight` / `stat_weights`(約20個の数値リスト)でAIに自由設計させる。
mod内 generic.txt のコメントアウト部分に例があるが、結果が読みにくいため新規では使わない。

## 主要フィールド

| フィールド | 意味 |
|---|---|
| `role` | ロール名。`ai_strategy` の `role_ratio` と対応(infantry, armor, mountaineers 等) |
| `upgrade_prio` | グループ/テンプレートの優先度。技術進歩で次世代に切り替える条件をmodifierで書く |
| `target_template` | 目標構成。`support` + `regiments` |
| `replace_with` | 次世代テンプレートへの置換先 |
| `replace_at_match` | 置換のしきい値(1.0超で「優先度逆転時のみ」) |
| `target_min_match` | 既存テンプレートとの一致率がこれ未満なら新規作成 |
| `can_upgrade_in_field` | 戦闘配備中の改良許可条件 |
| `production_prio` | 生産優先度(グループレベル) |

## 新規国家にテンプレートAIを足す手順

1. 国の性格を決める: 大国型(`ai_templates_continental_major.txt`)か小国コスト型(`ai_templates_minor_cost_focus.txt`)か
2. 既存ファイルの該当グループに `enable`/トリガー分岐があるか確認し、追記 or 新規 `TAG_templates.txt` を作成
3. `target_template` の `regiments` キーは `common/units/*.txt` のユニット名と一致させる
4. 使用する装備の研究が `ai_strategy_plans` の `research` 重みでカバーされているか確認(研究してないユニットは作れない)

## 注意点

- `target_template` に書いたユニットの前提技術をAIが研究しないと、その師団は永遠に作られない。研究重み([ai_strategy_plans_reference.md](ai_strategy_plans_reference.md))とセットで設計する
- 支援中隊も同様(例: mot_recon には自動車化偵察の研究が必要)
- ロール比率自体(歩兵何%・戦車何%)は `ai_strategy` の `role_ratio`/`unit_ratio` で決まる。テンプレートAIは「各ロールの中身」を決めるだけ

## mod内実例

- `bakasekai/common/ai_templates/generic.txt`
- `bakasekai/common/ai_templates/ai_templates_continental_major.txt`
- `bakasekai/common/ai_templates/ai_templates_japan_major.txt`
- `bakasekai/common/ai_templates/ai_templates_minor_cost_focus.txt`
- `bakasekai/common/ai_templates/templates_WES.txt` — 国別カスタム例
