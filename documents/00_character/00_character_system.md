
# HOI4 キャラクターシステム解説（Emil Scarlet氏による）

## 1. 概要

Barbarossa（バルバロッサ）アップデート（1.11）で導入されたキャラクターシステムは、MODにおける人物管理を一元化し、バグ回避と効率化を図れる画期的な仕組みです。

### 利点
- 人物（将軍・閣僚・国家元首など）の情報を一元管理可能
- 国家移動の処理が簡略化
- 条件付き出現設定（flagやvisible等）
- 将校団との連携可能（参謀や長官など）

### 欠点
- 同君連合のような複数国家に登場させる仕様が難しい

---

## 2. キャラクターの対応範囲
- 国家元首（country_leader）
- 将軍/元帥（corps_commander / field_marshal）
- 提督（navy_leader）
- 閣僚（advisor：政治顧問、理論家、各長官、最高司令部）

---

## 3. 基本構文

```hoi4
TAG_hogehoge = {
  name = TAG_hogehoge
  portrait = {
    civilian = {
      large = "GFX_ポートレートの名前"
    }
    army = {
      large = "GFX_ポートレート"
      small = "GFX_アイコン"
    }
    navy = {
      large = "GFX_ポートレート"
      small = "GFX_アイコン"
    }
  }
}
```

### 各項目の説明
- `large`: 通常ポートレート（156x210）
- `small`: アイコン（65x67）
- `civilian`: 国家元首用
- `army`: 将軍・元帥用（smallが将校団アイコン）
- `navy`: 提督用

---

## 4. 各役職の定義

### 国家元首

```hoi4
country_leader = {
  ideology = fascism
  expire = "9999.1.1"
  traits = {}
  id = 100
  desc = "POLITICS_TAG_DESC"
}
```

### 将軍／元帥

```hoi4
corps_commander = {
  skill = 3
  attack_skill = 2
  defense_skill = 2
  planning_skill = 2
  logistics_skill = 2
  traits = {}
  legacy_id = -1
  visible = { }
}
```

### 提督

```hoi4
navy_leader = {
  skill = 3
  attack_skill = 2
  defense_skill = 2
  maneuvering_skill = 2
  coordination_skill = 2
  traits = {}
  legacy_id = -1
  visible = { }
}
```

### 閣僚

```hoi4
advisor = {
  slot = political_advisor
  idea_token = TAG_hogehoge
  ledger = civilian
  cost = 150
  allowed = { }
  traits = { }
  modifier = { }
  research_bonus = { }
  available = { }
  visible = { }
  ai_will_do = { }
}
```

---

## 5. キャラクターの配置方法

```hoi4
# history/countries/XXX - 国家ファイル
recruit_character = TAG_hogehoge
```

- `recruit_character` は `history` 内でのみ使用可能
- ファイル末尾に記述する場合、**EOFの改行を忘れずに**

---

## 6. 関連エフェクト

### 基本
```hoi4
retire_character = yes
set_nationality = TAG
```

### 役職の追加
```hoi4
add_country_leader_role = { ideology = ... traits = {} ... }
add_field_marshal_role = { ... }
add_corps_commander_role = { ... }
add_naval_commander_role = { ... }
add_advisor_role = { slot = ..., traits = {}, activate = yes }
```

### 役職の削除
```hoi4
remove_country_leader_role = { ideology = ... }
remove_unit_leader_role = yes
remove_advisor_role = { slot = political_advisor }
```

---

## おわりに

キャラクターシステムはMOD開発における管理・パフォーマンス・柔軟性の全てに寄与します。記述は少し複雑ですが、運用できれば非常に強力な仕組みとなります。
