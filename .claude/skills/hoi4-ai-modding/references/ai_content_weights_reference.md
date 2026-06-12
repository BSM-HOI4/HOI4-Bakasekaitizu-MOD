# ai_will_do / ai_chance / ai_likelihood リファレンス

コンテンツ(NF・decision・イベント・idea・advisor)に埋め込むAI選択重み。
コンテンツ自体の作成は `hoi4-nf-creator` / `hoi4-decisions-helper` / `hoi4-event-helper` / `hoi4-idea-creator` を使い、AI重みの設計はここを参照する。

## 共通の形

```
ai_will_do = {
  factor = 5                # 基本値。0でAIは絶対に選ばない
  modifier = {
    factor = 0              # 条件付きで禁止
    has_war = yes
  }
  modifier = {
    factor = 2              # 条件付きで2倍
    has_country_flag = bsm_ai_policy_aggressive
  }
  modifier = {
    add = 10                # 加算も可
    surrender_progress > 0.1
  }
}
```

- `factor` は乗算、`add` は加算。`base` で基本値の置き換え(ai_chanceで使用可)
- modifier内のトリガーは「その重みが適用される条件」。トリガーを直接 modifier ブロック内に書く

## 置き場所ごとの仕様

### national_focus の ai_will_do

- 他の選択可能NFとの相対比較。`factor = 0` で取得禁止
- `ai_strategy_plans` の `ai_national_focuses` リストが優先され、`focus_factors` が乗算される
- 歴史準拠にするなら modifier で `is_historical_focus_on = yes` を見る

### decision / decision_category の ai_will_do

- decisionは毎回評価が走るため、重いトリガーは厳禁(CLAUDE.mdのパフォーマンス指針参照)
- mission型decisionは特に重い。`days_mission_timeout` 系は代替を検討
- `ai_will_do` の `factor` が他のdecisionとの優先度になる。政治力コストとの兼ね合いでAIが貯金するかも決まる

### event option の ai_chance

```
option = {
  name = event_id.opt_a
  ai_chance = {
    base = 80
    modifier = {
      factor = 0.5
      has_government = communism_ideology   # BSMはイデオロギー名が改名済みな点に注意
    }
  }
  # 効果...
}
```

- 全optionの値を正規化して確率として扱う(80/20なら8:2)
- optionが1つでも `ai_chance` を持つ場合、他のoptionにも明示すること(片方未指定はバグの元)
- BSM注意: イデオロギーは `communism_ideology` / `democratic_ideology` / `fascism_ideology` / `neutrality_ideology`

### idea / advisor の ai_will_do

- 大臣(advisor)の `ai_will_do` は政治力支出の優先度。`ai_strategy_plans` の `ideas` 重みと併用される
- `traits` 側の重みは `ai_strategy_plans` の `traits` ブロックで調整

### character (advisor slot) の ai_will_do

`common/characters/` の advisor ブロック内に書く。形式は同じ。

## BSMパターン: AI方針フラグ駆動

経済同盟(EA)システム等で使用している定番構成:

1. AIの大方針を country_flag で表現(例: `bsm_ea_ai_policy_reciprocal` / `bsm_ea_ai_policy_exploit`)
2. 方針決定は scripted_effect に集約し、`on_actions`(`on_monthly` 等)から呼ぶ
3. 各 decision / event option の `ai_will_do` / `ai_chance` は flag を見るだけにする(高速・一貫性)

```
# scripted_effects(月次で方針を再評価)
bsm_ea_ai_update_policy = {
  if = {
    limit = { check_variable = { bsm_ea_relation_score > 50 } }
    set_country_flag = bsm_ea_ai_policy_reciprocal
    clr_country_flag = bsm_ea_ai_policy_exploit
  }
  else = {
    set_country_flag = bsm_ea_ai_policy_exploit
    clr_country_flag = bsm_ea_ai_policy_reciprocal
  }
}

# decision側は flag を見るだけ
ai_will_do = {
  factor = 0
  modifier = {
    factor = 10
    has_country_flag = bsm_ea_ai_policy_exploit
  }
}
```

注意: `on_monthly` は全国家で月1回発火(国ごとに日がずれる)。重い方針計算はここに置き、`ai_will_do` 側は軽くする。

## デバッグ

- AIが選ばない場合: `factor = 0` になっていないか、modifierの合計を確認
- イベント選択肢の検証: `human_ai` でAI操作にして観察、または `event <id> <TAG>` で対象国に発火
- 詳細は [ai_debugging_reference.md](ai_debugging_reference.md)
