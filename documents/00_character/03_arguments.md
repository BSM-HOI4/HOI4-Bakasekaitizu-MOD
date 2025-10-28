# 3. Arguments
# HOI4 Character Modding: Argument Reference

## 3. Arguments

この章では、キャラクター定義に使用される各種引数について解説します。

---

## Name

```hoi4
name = my_character
```

* ローカライズキー `my_character` を指定。
* 対応ファイル例: `localisation/english/characters_l_english.yml`

```yaml
my_character: "My character's name"
```

---

## Portraits

```hoi4
portraits = {
    civilian = {
        large = GFX_my_country_leader_portrait
        small = GFX_my_advisor_portrait
    }
    army = {
        large = GFX_my_unit_leader_portrait
    }
}
```

ポートレートの定義:

* `civilian`, `army`, `navy` の3カテゴリ
* `large`, `small` サイズに分類

スプライトの定義（例）:

```hoi4
graphics = {
    spriteTypes = {
        spriteType = {
            name = GFX_my_advisor_portrait
            texturefile = gfx/foldername/advisor_filename.dds
        }
        spriteType = {
            name = GFX_my_country_leader_portrait
            texturefile = gfx/foldername/country_leader_filename.dds
        }
        spriteType = {
            name = GFX_my_unit_leader_portrait
            texturefile = gfx/foldername/army_leader_filename.dds
        }
    }
}
```

注意:

* `GFX_` で始まる一語のみ（ASCII文字）
* `.gfx` 拡張子、`spriteTypes = {}` ブロックが必要
* 小サイズ用スプライト例:

```hoi4
spriteType = {
    name = GFX_my_unit_leader_portrait_small
    texturefile = gfx/foldername/officer_minister_filename.dds
}
```

直接ファイルパスで定義する場合:

```hoi4
portraits = {
    civilian = {
        large = "gfx/leaders/TAG/TAG_Leader_civilian.png"
        small = "gfx/advisors/TAG/TAG_Leader_civilian.png"
    }
    army = {
        large = "gfx/leaders/TAG/TAG_Leader_army.png"
        small = "gfx/advisors/TAG/TAG_Leader_army.png"
    }
}
```

---

## Gender

```hoi4
gender = male  # または female, undefined
```

主に代名詞のローカライズに使用されます。

* `undefined` は `male` として扱われる
* `generate_character` により動的生成された場合、ランダムに決定

---

## Advisors

```hoi4
advisor = {
    slot = theorist
    idea_token = my_character
    ledger = army
    traits = { military_theorist }
    can_be_fired = no
}
```

* `slot`: `political_advisor`, `theorist`, `army_chief`, etc.
* `idea_token`: アイデアID（ユニークでなければならない）
* `traits`: 国家補正に使われる特性
* `on_add`, `on_remove`: キャラクタースコープを使用

---

## Country leaders

```hoi4
country_leader = {
    ideology = centrism
    desc = MY_LEADER_DESCRIPTION
    traits = { my_trait_1 my_trait_2 }
    expire = 1949.1.1
}
```

* `ideology`: 社会主義など、タイプ名（グループではない）
* `desc`: ローカライズキー
* `traits`: 国家リーダー特性

注意:

* `id = 100` は非推奨
* 他のリーダーと競合しないように管理

---

## Unit leaders

### Field Marshal

```hoi4
field_marshal = {
    traits = { my_trait_1 my_trait_2 }
    skill = 10
    attack_skill = 8
    defense_skill = 1
    planning_skill = 10
    logistics_skill = 10
}
```

### Corps Commander

```hoi4
corps_commander = {
    skill = 1
    attack_skill = 2
    defense_skill = 3
    planning_skill = 4
    logistics_skill = 5
}
```

### Navy Leader

```hoi4
navy_leader = {
    skill = 3
    attack_skill = 1
    defense_skill = 3
    maneuvering_skill = 5
    coordination_skill = 4
    visible = { has_stability > 0.3 }
}
```

| Skill                | 効果                      |
| -------------------- | ----------------------- |
| `attack_skill`       | 陸: +2.5%攻撃 / 海: +5%ダメージ |
| `defense_skill`      | 陸: +2.5%防御 / 海: +5%防御   |
| `planning_skill`     | 陸: +5%計画速度、+2%ボーナス上限    |
| `logistics_skill`    | 陸: -2.5%補給消費            |
| `maneuvering_skill`  | 海: +2.5%配置、+1%撤退速度      |
| `coordination_skill` | 海: +2%艦隊協調              |

---

## 備考

* `.gfx` と `.dds` のファイル命名規則は厳格に守ること。
* `traits` や `slot`、`ledger` の組み合わせミスに注意。
* 可視性条件 `visible = { ... }` は任意だが柔軟な条件分岐に使える。
* キャラクターIDの再利用は避ける。

---

以上がキャラクター定義における基本的な引数の解説です。より詳細な仕様やバグ回避方法は実際のMOD環境での検証や、Paradox公式フォーラム等も参考にしてください。
