# TAOG Update Guide

この文書は、HOI4 TAOG (Thunder at Our Gates) 対応で必要になった移行作業の記録と、今後同種のファイルを更新するときの確認用チェックリストです。

## 対象範囲

- BSM の `bakasekai/` 配下で、バニラの TAOG 追加内容が `replace_path` や既存定義によって隠れる箇所。
- 優先度は CTD 回避、旧構文の置換、師団デザイナー互換、ブックマーク表示、OOS 予防の順。
- このガイドは実装時点の移行方針であり、最終確認はゲーム起動後の `error.log` と対象画面の手動確認で行う。

## 最優先の移行項目

### Army HQ テンプレート

TAOG では Army HQ 用テンプレートが必要です。全国家に HQ テンプレートがないと CTD する可能性があります。

- 追加先: `bakasekai/history/general/taog_hq_template.txt`
- 最低限、`every_possible_country` で汎用 HQ テンプレートを付与する。
- DLC 限定機能のため、必要に応じて `has_dlc = "Thunder at Our Gates"` で制限する。
- HQ テンプレートには `is_army_hq = yes` を設定する。

### アビリティ旧構文の置換

`add_temporary_buff_to_units` を使った旧アビリティ構文は TAOG 以降では機能しません。`unit_modifiers` に移行します。

代表的な対応:

```txt
combat_offense = 0.2
```

を以下へ置換:

```txt
offence = 0.2
```

主な対応表:

- `combat_offense` -> `offence`
- `combat_defense` -> `defence`
- `combat_breakthrough` -> `breakthrough_factor`
- `org_damage_multiplier` -> 同名で維持
- `str_damage_multiplier` -> 同名で維持
- `war_support_reduction_on_damage` -> 同名で維持
- `cannot_retreat_while_attacking` -> 同名で維持
- `cannot_retreat_while_defending` -> 同名で維持

確認コマンド:

```sh
rg -n "add_temporary_buff_to_units" bakasekai/common/abilities
```

### 勲章 XP の置換

ユニット勲章の `one_time_effect = { add_divisional_commander_xp = ... }` は、TAOG の新形式では `officer_xp = ...` に移行します。

```txt
officer_xp = 100
```

艦長対応のため、陸軍向け `unit_modifiers` に対応する `ship_modifiers` も可能な範囲で追加します。

例:

- `army_org_factor` -> `navy_org_factor`
- `army_strength_factor` -> `naval_critical_effect_factor`
- `army_attack_factor` -> `naval_damage_factor`
- `army_defence_factor` -> `naval_defense_factor`
- `army_fuel_consumption_factor` -> `navy_fuel_consumption_factor`
- `experience_loss_factor` -> `experience_gain_navy_unit_factor`

注意: `common/raids/` ではバニラ TAOG でも `add_divisional_commander_xp` が使われる箇所があるため、機械的に全リポジトリから削除しない。

確認コマンド:

```sh
rg -n "add_divisional_commander_xp|one_time_effect\s*=\s*\{" bakasekai/common/unit_medals
```

## 支援中隊と師団デザイナー

TAOG 以降、支援中隊は師団支援と連隊支援に分かれます。既存の支援中隊は原則として師団支援へ寄せます。

### 既存支援中隊

既存の `group = support` 系は、基本的に以下を設定します。

```txt
group = support
categories = {
  category_divisional_support_battalions
}
regimental = no
```

大きな比率補正、塹壕、回復率、信頼性、トリクルバック、師団全体に効く補正を持つものは師団支援扱いにします。

### 連隊支援

野砲、機関銃、迫撃砲、対空、対戦車、自走対空、駆逐戦車など、列ごとの小さな補助火力として扱うものは連隊支援にします。

```txt
group = support
categories = {
  category_regimental_support_battalions
}
divisional = no
allowed_battalion_groups = {
  infantry
  mobile
  combat_support
}
```

必要な前線大隊数は define 側の `REGIMENTAL_SUPPORT_REQUIRED_BATTALIONS` に依存します。

### 技術アンロック

TAOG の支援中隊追加に合わせて、以下のような初期アンロック漏れを確認します。

- `support_weapons` で `fire_support` と `mot_fire_support` を有効化する。
- `gw_artillery` で `field_guns` を有効化する。

## 特殊部隊ドクトリン

TAOG の特殊部隊ドクトリンは新しいトラック式の仕組みに移っています。旧 `common/technologies/special_forces_doctrine.txt` を持ち続けると、バニラ側の新ドクトリンと競合する可能性があります。

- BSM 側で同等機能を再実装しない限り、旧技術ファイルは削除または無効化する。
- 新規追加時は `allow_in_multiple_tracks` と `xor` の使い方をバニラに合わせる。

## Army HQ と捕虜

国家元首など、捕虜化されると困る将軍には `can_be_captured = no` を追加します。

対象の目安:

- 同じキャラクターブロック内に `country_leader` と `corps_commander` がある。
- 同じキャラクターブロック内に `country_leader` と `field_marshal` がある。

配置位置はキャラクターの `name` 直下付近に置きます。

```txt
can_be_captured = no
```

## AI 海軍

TAOG ではタスクフォーステンプレートに `keep_updated = yes` が追加されています。AI の新造艦配備やテンプレート更新に関わる可能性があるため、汎用テンプレートへ追加します。

対象例:

- `bakasekai/common/ai_navy/taskforce/generic_taskforce_templates.txt`

## ブックマークラベル

TAOG 以降のブックマークフィルターでは、任意ラベルを追加できます。

ブックマーク側:

```txt
filters = {
  label
}
```

各国側:

```txt
label = {
  bsm_bm_major
  bsm_bm_democratic
}
```

ローカライズ:

- 配置: `bakasekai/localisation/japanese/*.yml`
- `l_japanese:` ヘッダー必須
- UTF-8 with BOM
- ラベルキー名がそのまま表示キーになる。

## Synchronized Dynamic Tokens

カスタム `modifier_definitions` などの動的トークンは、マルチプレイ OOS 防止のため `common/synchronized_dynamic_tokens/` に列挙します。

追加先:

```txt
bakasekai/common/synchronized_dynamic_tokens/_bsm_tokens.txt
```

エラーログに以下のような警告が出た場合は、そのトークンを追加します。

```txt
Token <token_name> is a dynamic token, this can cause OOS depending on how it's used
```

## Math Expressions

TAOG では数式構文が追加されています。高頻度処理で一時変数を多用している箇所は、将来的に `check_expr` や数式対応の変数効果へ置換できます。

ただし、今回の互換対応では既存挙動の維持を優先し、性能改善目的の大規模置換は別作業に分けます。

## 確認手順

最低限の静的確認:

```sh
git diff --check
rg -n "add_temporary_buff_to_units|add_divisional_commander_xp" bakasekai/common/abilities bakasekai/common/unit_medals
rg -n "one_time_effect\s*=\s*\{" bakasekai/common/unit_medals
```

手動確認:

- 1936 年ブックマークを開き、ラベルフィルターが表示されること。
- 師団デザイナーで既存支援中隊が師団支援欄に出ること。
- 連隊支援が列条件を満たした時だけ配置できること。
- Army HQ 配備画面または将軍配備関連画面で CTD しないこと。
- 旧アビリティを発動し、効果が戦闘補正として反映されること。
- 勲章付与時に XP と陸海補正がエラーを出さないこと。
- `Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log` に新規構文エラーがないこと。

## 追加作業時の注意

- 旧構文を見つけても、バニラ TAOG が同じ場所で使っているものは用途を確認してから置換する。
- 支援中隊は「師団全体への大きな補正か」「列ごとの小補助か」で分類する。
- `replace_path` でバニラの新規ファイルを隠していないかを優先して確認する。
- ローカライズ追加時は BOM と重複キーを確認する。
- 実ゲーム確認なしで互換完了扱いにしない。
