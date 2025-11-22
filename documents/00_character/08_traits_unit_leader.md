# 8. Unit Leader Traits

U# 8. 師団指揮官の特性

> ℹ️ **注:** これはコミュニティによって維持されているwikiです。間違いを見つけた場合は、修正にご協力ください。

師団指揮官の特性は、`/Hearts of Iron IV/common/unit_leader/*.txt` 内の任意のファイルで定義され、あらゆる種類の師団指揮官キャラクターや諜報員に割り当てることが可能です。各特性は `leader_traits = { ... }` ブロック内に、特性のIDを名前として持つ個別のエントリとして定義されます。

---

## ローカライゼーション

ローカライゼーションは、任意のローカライゼーションファイル内で特性の名前をローカライゼーションキーとして使用して定義します。例えば、`my_trait: "私の特性"` のように記述します。説明を追加するには、末尾に `_desc` を付けて `my_trait_desc: "私の説明"` のようにします。

---

## GFX（グラフィック）

画像は、`/Hearts of Iron IV/interface/*.gfx` ファイル内で `GFX_trait_<trait's name>` という名前の `spriteType` として定義されます。例えば、`not_polish_person` という名前の特性の場合、`GFX_trait_not_polish_person` という名前のスプライト定義が使用されます。特性名が `trait_`で始まる場合、スプライト名で `trait_` を二重にする必要はありません。例えば、`trait_example` のスプライトは `GFX_trait_example` として定義されます。

両方のスプライトを含む `/Hearts of Iron IV/interface/*.gfx` ファイルの内容は次のようになります：
```plaintext
spriteTypes = {
    spriteType = {
        name = GFX_trait_not_polish_person
        texturefile = gfx/foldername/filename.dds
    }
    spriteType = {
        name = GFX_trait_example
        texturefile = gfx/foldername/filename.dds
    }
}
```

---

## 一般的な引数

| 引数 | 値の種類 | 例 | 効果 | 注記 |
| --- | --- | --- | --- | --- |
| `type` | タイプ | `type = corps_commander`<br>`type = { land navy }` | 特性にタイプを割り当て、どのキャラクターがそれを受け取れるかを決定します。 | タイプには `all`, `land`, `navy`, `operative`, `corps_commander`, `field_marshal` があります。 |
| `trait_type` | 特性タイプ | `trait_type = assignable_trait` | ユーザーインターフェース上の配置場所や、割り当て可能かどうか、いつ可能かを決定します。 | タイプには `basic_trait` (諜報員用), `personality_trait`, `assignable_trait`, `basic_terrain_trait`, `assignable_terrain_trait`, `status_trait`, `exile` があります。 |
| `show_in_combat` | 真偽値 | `show_in_combat = yes` | 指定された特性を戦闘メニューのボーナスの中に表示させます。 | |
| `allowed` | トリガー | `allowed = { FROM = { tag = POL } }` | 師団指揮官に特性を割り当てようとするときにチェックされ、偽の場合は割り当てに失敗します。師団指揮官のスコープでチェックされます。 | `FROM` はキャラクターを雇用した国です。 |
| `ai_will_do` | MTTHブロック | `ai_will_do = { base = 3 }` | AIがこの特性を選ぶ際の重みを決定します。 | 重みが0の場合、AIは決して選びません。 |
| `new_commander_weight` | MTTHブロック | `new_commander_weight = { base = 0 }` | 新しくランダムに生成される師団指揮官に対して特性が持つ重みを決定します。 | 重みが0の場合、ランダム生成の指揮官には決して現れません。`personality_trait` タイプを持つ特性に対してのみ定義可能です。 |
| `slot` | 士官スロット | `slot = army_chief` | この師団指揮官に割り当て可能な将校団の役割が使用する顧問スロットを決定します。 | |
| `specialist_advisor_trait` | 国家指導者特性 | `specialist_advisor_trait = my_trait` | 指定された顧問特性をベースとして、この師団指揮官に割り当て可能な専門家レベルの将校団の役割を作成します。 | |
| `expert_advisor_trait` | 国家指導者特性 | `expert_advisor_trait = my_trait` | 指定された顧問特性をベースとして、この師団指揮官に割り当て可能なエキスパートレベルの将校団の役割を作成します。 | |
| `genius_advisor_trait` | 国家指導者特性 | `genius_advisor_trait = my_trait` | 指定された顧問特性をベースとして、この師団指揮官に割り当て可能な天才レベルの将校団の役割を作成します。 | |
| `unit_type` | サブユニットタイプ | `unit_type = { type = infantry }` | 補正が適用されるユニットの選択を、そのサブユニットを編成に含むものに限定します。 | サブユニットは `/Hearts of Iron IV/common/units/*.txt` ファイルで定義されます。 |
| `unit_trigger` | トリガー | `unit_trigger = { division_has_majority_template = camelry }` | ユニットが補正を受けるために満たす必要がある師団スコープのトリガーブロックを適用します。 | |

---

## 補正と効果

これらの引数は、特性が師団指揮官に与える補正や、それに関連するものです。

| 引数 | 値の種類 | 例 | 効果 | 注記 |
| --- | --- | --- | --- | --- |
| `modifier` | 補正 | `modifier = { planning_speed = 0.2 }` | 指揮官が率いる師団に特性が与える補正を割り当てます。 | 地形を指定してスコープすることも可能です。 |
| `non_shared_modifier` | 補正 | `non_shared_modifier = { experience_gain_factor = 0.3 }` | 師団指揮官自身に特性が与える補正を割り当てます。 | ツールチップが異なるため、ゲーム内での表示が変わります。 |
| `corps_commander_modifier` | 補正 | `corps_commander_modifier = { max_commander_army_size = 3 }` | 軍団長として部隊を直接率いる際に、特性が与える補正を割り当てます。 | |
| `field_marshal_modifier` | 補正 | `field_marshal_modifier = { supply_consumption_factor = 0.5 }` | 元帥として他の将軍を率いる際に、特性が与える補正を割り当てます。 | |
| `sub_unit_modifiers` | 補正 | `sub_unit_modifiers = { artillery_brigade = { max_strength = 0.1 } }` | 指揮官が率いる師団を構成する旅団に、特性が与える補正を割り当てます。 | |
| `<skill type>` | 整数 | `attack_skill = 2` | 指定されたスキルに固定ボーナスを追加します。 | |
| `<skill type>_factor` | パーセント | `defense_skill_factor = 1` | 指定されたスキルに乗算ボーナスを追加します。1は100%追加を意味します。 | |
| `override_effect_tooltip` | ローカライゼーションキー | `override_effect_tooltip = my_effect_tt` | 特性の効果を隠し、ツールチップをこのローカライゼーションキーの値に置き換えます。 | |
| `custom_effect_tooltip` | ローカライゼーションキー | `custom_effect_tooltip = my_effect_tt` | 特性の効果を示すツールチップに、このローカライゼーションキーの値を追加します。 | |
| `enable_ability` | アビリティ | `enable_ability = my_ability` | 指揮官が戦闘で使用できるアビリティを有効にします。 | アビリティは `/Hearts of Iron IV/common/abilities/*.txt` で定義されます。 |
| `on_add` | 効果 | `on_add = { promote_leader = yes }` | 特性が追加されたときに師団指揮官に実行される効果を定義します。 | |
| `on_remove` | 効果 | `on_remove = { remove_unit_leader = yes }` | 特性が削除されたときに師団指揮官に実行される効果を定義します。 | |
| `daily_effect` | 効果 | `daily_effect = { gain_xp = 1 }` | 特性を持っている場合に毎日師団指揮官に実行される効果を定義します。 | |

---

## 選択

これらの引数は、特性を選択するメニューに関連します。経験値も含まれます。特性が手動でのみ割り当てられる場合、これらは省略できます。

| 引数 | 値の種類 | 例 | 効果 | 注記 |
| --- | --- | --- | --- | --- |
| `mutually_exclusive` | 特性 | `mutually_exclusive = my_trait` | 指定された特性を他の特性と相互排他的にし、メニューに矢印を描画します。 | 両方の特性でこれを定義する必要があります。 |
| `parent` | 特性 | `parent = my_trait` | 指定された特性を親としてマークし、現在の特性を選ぶために必要とし、メニューに線を描画します。 | `parent = my_trait_2` を複数回定義することで、複数の親を指定できます。 |
| `num_parents_needed` | 整数 | `num_parents_needed = 3` | 特性を選択するために必要な親の数を設定します。 | 省略または-1に設定した場合、すべての親が必要と見なされます。 |
| `gui_row` | 整数 | `gui_row = 3` | 特性が配置される行を設定します。 | 0から始まります。 |
| `gui_column` | 整数 | `gui_column = 3` | 特性が配置される列を設定します。 | 省略した場合、`trait_type` に応じて自動的に選択されます。 |
| `prerequisites` | トリガー | `prerequisites = { defense_skill_level > 3 }` | 特性を割り当てるために満たす必要があるトリガー。 | 師団指揮官スコープでチェックされます。 |
| `custom_prerequisite_tooltip` | ローカライゼーションキー | `custom_prerequisite_tooltip = my_prerequisite_tt` | 特性を選択するための条件のツールチップを変更します。 | |
| `cost` | 数値 | `cost = 1500` | この特性を師団指揮官に割り当てるために必要な経験値。 | |
| `gain_xp` | トリガー | `gain_xp = { is_amphibious_invasion = yes }` | この特性の割り当てを可能にする経験値を得るために満たす必要があるトリガー。 | 戦闘員スコープでチェックされます。 |
| `gain_xp_leader` | トリガー | `gain_xp_leader = { num_units > 10 }` | この特性の割り当てを可能にする経験値を得るために満たす必要があるトリガー。 | 師団指揮官スコープでチェックされます。 |
| `gain_xp_on_spotting` | 数値 | `gain_xp_on_spotting = 7` | 提督が敵艦隊を発見したときに得られる経験値の量。 | |
| `custom_gain_xp_trigger_tooltip` | ローカライゼーションキー | `custom_gain_xp_trigger_tooltip = my_prerequisite_tt` | 経験値を得るための条件のツールチップを変更します。 | |
| `trait_xp_factor` | トリガー | `trait_xp_factor = { my_trait = 0.1 }` | 指揮官がこの特性を持っている場合、他の特性に向けて得られる経験値の量を修正します。 | 0.1は経験値が10%多くなることを意味します。 |
