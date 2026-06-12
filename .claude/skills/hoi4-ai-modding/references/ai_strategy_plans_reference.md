# ai_strategy_plans リファレンス

国ごとの「プレイ方針プラン」。NFの取得順序、研究配分、大臣・将軍特性の好み、個別NFの重みをまとめて定義する。
配置: `common/ai_strategy_plans/*.txt`(国別は `TAG.txt`)

## 基本構造(mod内 WES.txt 準拠)

```
WES_sahara_SAND = {
  name = "Sahara SAND"               # 内部名(デバッグ表示用、loc不要)
  desc = "プランの説明"

  allowed = {                        # ゲーム開始時に1回だけ評価(軽量化に重要)
    original_tag = WES
  }
  enable = {                         # プランが有効になる条件
    has_country_flag = WES_AI_RANDOM_SAND
  }
  abort = {                          # 有効後に破棄する条件(空なら破棄しない)
  }

  ai_national_focuses = {            # この順番でNFを取らせる(最優先リスト)
    WES_gone_with_the_sand
    WES_march_of_the_sand_division
    WES_sand_rifle
  }

  research = {                       # 研究カテゴリの重み(technology categoryごと)
    infantry_weapons = 50.0
    infantry_tech = 15.0
    artillery = 8.0
    support_tech = 6.5
  }

  ideas = {                          # 大臣・デザイナー採用の重み(idea token = factor)
    hjalmar_schacht = 10
    heinrich_himmler = 0             # 0で採用禁止
  }

  traits = {                         # 将軍・大臣特性の重み
    captain_of_industry = 5
  }

  # weightは小さく保つ。研究需要等の係数にも使われる。推奨は1.0前後
  weight = {
    factor = 1.0
    modifier = {
      factor = 1.0
    }
  }

  focus_factors = {                  # 個別NFの重み係数(ai_will_doに乗算)
    # WES_some_focus = 0             # 0でそのNFを取らせない
  }
}
```

## 各フィールドの要点

- `ai_national_focuses`: リスト順に取得を試みる。前提条件未達成のものはスキップして次へ。**リストにあるNFはai_will_doより優先される**
- `focus_factors`: リスト外のNFの調整に使う。`0` は事実上の禁止
- `research`: キーは `common/technology_tags/` のresearch category。値は相対重み
- `ideas` / `traits`: 政治力支出の優先度に影響
- `weight`: プラン同士の相対比較と研究需要係数。1.0前後を維持(コメントにもある通り大きくしない)
- 複数プランが同時にenableになり得る場合、`weight` と `enable` 条件で排他を設計する

## BSMパターン: country_flag によるランダムAI分岐

WES.txt は `WES_AI_RANDOM_SAND` のようなflagでプランを切り替えている。
ランダムAI用の分岐は次のセットで実装する:

1. ゲーム開始時(`on_startup` または初期イベント)に `random_list` でflagを1つ立てる
2. プランの `enable = { has_country_flag = ... }` で拾う
3. 歴史AI(`is_historical_focus_on`)の場合は固定flagまたは歴史用プランを別に用意

```
# scripted_effect または on_startup 内
WES_assign_ai_plan = {
  if = {
    limit = { is_historical_focus_on = yes }
    set_country_flag = WES_AI_HISTORICAL
  }
  else = {
    random_list = {
      50 = { set_country_flag = WES_AI_RANDOM_SAND }
      50 = { set_country_flag = WES_AI_RANDOM_OTHER }
    }
  }
}
```

## パフォーマンス

- `allowed` に `original_tag` / `tag` を必ず書く(全国家×全プランの評価を初回で打ち切る)
- `enable` はflagチェック中心にする

## mod内実例

- `bakasekai/common/ai_strategy_plans/WES.txt` — flag分岐ランダムプラン
- `bakasekai/common/ai_strategy_plans/CHN_civil_war.txt` — シナリオ連動
- `bakasekai/common/ai_strategy_plans/sew_strategy_plans.txt`

## 関連

- 個別NF側の `ai_will_do` 設計: [ai_content_weights_reference.md](ai_content_weights_reference.md)
- 外交・生産方針: [ai_strategy_reference.md](ai_strategy_reference.md)
