# ai_strategy リファレンス

戦略AI。外交方針(同盟/敵対/宣戦)、戦争準備、占領方針などを国単位で重み付けする。
配置: `common/ai_strategy/*.txt`

## 基本構造

```
bsm_example_strategy = {          # ブロック名はファイル内で一意
  enable = {                      # 毎日評価される。軽いトリガーを先頭に
    original_tag = RED
    has_country_flag = bsm_some_flag
  }
  abort = {                       # これがtrueになると戦略を破棄
    always = no
  }
  # abort_when_not_enabled = yes  # abortの代わりに「enableが偽になったら破棄」

  ai_strategy = {
    type = alliance               # 戦略タイプ
    id = ESP                      # 対象国TAG(タイプにより不要)
    value = 200                   # 重み。負値で抑制も可
  }
  # ai_strategy ブロックは1つの戦略定義に複数並べてよい
}
```

- `value` は加算的。複数の定義・`add_ai_strategy` の値が同じ type/id に合算される
- 既存値の打ち消しには負の `value` を使う(例: vanillaが `conquer` を積むのを `value = -1000` で抑制)

## 主要な戦略タイプ

### 外交・戦争方針(id = 対象国TAG)

| type | 効果 |
|---|---|
| `alliance` | 陣営に誘う/参加したい度合い |
| `befriend` | 関係改善・協調行動の優先度 |
| `support` | 独立保障・レンドリース等の支援意欲 |
| `protect` | 防衛対象として扱う |
| `influence` | 政治工作・傀儡化等の影響力行使 |
| `antagonize` | 敵視(正当化対象候補になる) |
| `conquer` | 征服目標としての優先度 |
| `contain` | 封じ込め(陣営拡大・保障で対抗) |
| `declare_war` | 宣戦の意欲(正当化済みCBが前提) |
| `prepare_for_war` | 開戦準備(軍備・配備を対象国向けに) |
| `invade` | 上陸侵攻の優先対象 |
| `ignore` | 脅威評価から除外(国境防備を薄くする) |
| `ignore_claim` | 対象国の請求権を無視 |
| `consider_weak` | 対象を弱いとみなす(開戦判断が強気になる) |
| `send_volunteers_desire` | 義勇軍派遣の意欲 |
| `dont_defend_ally_borders` | 同盟国国境の防衛をやめる(id=同盟国) |
| `force_defend_ally_borders` | 同盟国国境の防衛を強制 |
| `occupation_policy` | 占領方針(value=占領法インデックス) |
| `activate_crypto` / `decrypt_target` | 諜報: 暗号解読の対象選択 |

この一覧は `documents/00_coding_contexts/dynamic_variables_documentation.md` の `ai_strategy_*` 変数群と対応。
上記以外の生産・配備系タイプ(`unit_ratio`, `role_ratio`, `area_priority`, `building_target`,
`equipment_production_min_factories`, `theatre_distribution_demand_increase` 等)はvanillaの
`common/ai_strategy/default.txt` に実例があるため、使用前にvanilla定義を確認すること。

### 生産・配備系の例(idがユニット種や建物になる)

```
bsm_example_production = {
  enable = { original_tag = WES }
  abort_when_not_enabled = yes

  ai_strategy = {
    type = unit_ratio             # 陸軍構成比
    id = infantry
    value = 100
  }
  ai_strategy = {
    type = building_target        # 建設目標数
    id = air_base
    value = 3
  }
  ai_strategy = {
    type = area_priority          # ai_areasで定義したエリアへの優先度
    id = north_africa             # common/ai_areas/default.txt のキー
    value = 50
  }
}
```

## add_ai_strategy effect(動的制御)

イベント・NF・decision・scripted_effect から一時的に戦略を積む。

```
# イベントのoption内など(COUNTRYスコープ)
add_ai_strategy = {
  type = befriend
  id = "ESP"        # effectではTAGをクォートする書き方が安全
  value = 200
}
```

- 積んだ値はセーブに保存され、自前で打ち消さない限り残る。恒久方針なら `common/ai_strategy/` に静的定義する方が管理しやすい
- BSMの定番パターン: country_flag を立てて静的定義の `enable` で拾う(打ち消し・条件変更がflag操作だけで済む)

```
# scripted_effect 側
bsm_set_ai_policy_aggressive = {
  set_country_flag = bsm_ai_policy_aggressive
  clr_country_flag = bsm_ai_policy_defensive
}

# common/ai_strategy/ 側
bsm_policy_aggressive_conquer = {
  enable = { has_country_flag = bsm_ai_policy_aggressive }
  abort_when_not_enabled = yes
  ai_strategy = { type = conquer id = ESP value = 100 }
}
```

## 戦略値の読み取り(トリガー・表示)

戦略値は動的変数として読める: `ai_strategy_<type>@<TAG>`

```
# トリガー
check_variable = { ROOT.ai_strategy_befriend@ESP > 100 }

# localisation(デバッグ表示)
[?ROOT.ai_strategy_conquer@ESP]
```

## mod内実例

- `bakasekai/common/ai_strategy/bsm_iberian_ai_strategy.txt` — alliance/befriend の最小例
- `bakasekai/common/ai_strategy/sew_strategies.txt` — シナリオ用戦略群
- `bakasekai/common/ai_strategy/CHN_civil_war.txt` — 内戦シナリオ
- `bakasekai/common/ai_strategy/default.txt` — vanillaベースの全体調整

## 注意点

- `enable` は毎日全国家で評価される。`original_tag = X` や `has_country_flag` を必ず先頭に置く
- 同名ブロックが複数ファイルにあると後勝ちで上書きされる(vanilla上書きに利用できるが、意図しない衝突に注意)
- 歴史AI(`is_historical_focus_on`)とランダムAIで分岐させる場合は `enable` 内で `has_game_rule` / `is_historical_focus_on` を確認
- AIが宣戦しない場合の典型原因: CB(正当化)がない、`declare_war` 値不足、陣営リーダーの許可待ち、戦争準備度不足。[ai_debugging_reference.md](ai_debugging_reference.md) 参照
