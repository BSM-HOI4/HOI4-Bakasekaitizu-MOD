# 6. Using In-Game

## 参照リンク
- See also: Effect § Character scope
- See also: Effect § Characters

## 基本事項
キャラクターは作成後、必ず国家に割り当てる必要があります。

```hoi4
# /history/countries/TAG - ファイル内の例:
recruit_character = TAG_character_name
```

この行がファイルの最終行になると無効になるため、少なくとも1行はその後に記述が必要です。

## 国家リーダーの割り当て
イデオロギーごとに最初にリクルートされたキャラクターが、そのイデオロギーの政党リーダーになります。

```hoi4
recruit_character = TAG_marxist_leader      # ideology = marxism
recruit_character = TAG_stalinist_leader    # ideology = stalinism
recruit_character = TAG_liberal_leader      # ideology = liberalism
recruit_character = TAG_conservative_leader # ideology = conservatism
recruit_character = TAG_centrist_leader     # ideology = centrism
recruit_character = TAG_despotic_leader     # ideology = despotism
recruit_character = TAG_falangist_leader    # ideology = falangism
recruit_character = TAG_rexist_leader       # ideology = rexism

set_politics = {
  ruling_party = democratic
  elections_allowed = no
}
```

この場合:
- 民主主義：TAG_liberal_leader
- 共産主義：TAG_marxist_leader
- 非同盟：TAG_centrist_leader
- ファシズム：TAG_falangist_leader


## promote_character の使用
```hoi4
# キャラクタースコープ:
TAG_conservative_leader = {
    promote_character = yes
}
TAG_conservative_leader = {
    promote_character = conservatism
}

# 国家スコープ:
promote_character = TAG_conservative_leader
promote_character = {
    character = TAG_conservative_leader
    ideology = conservatism
}
```

## 空のキャラクターを後で役職に割り当てる
```hoi4
characters = {
  TAG_new_leader = {
    name = TAG_new_leader
    gender = female
    portraits = {
      civilian = {
        large = GFX_portrait_TAG_new_leader
      }
    }
  }
}

# リクルート
recruit_character = TAG_new_leader

# 後で役職付与
completion_reward = {
  add_country_leader_role = {
    character = TAG_new_leader
    promote_leader = yes
    country_leader = {
      ideology = conservatism
      traits = { my_trait }
    }
  }
}
```

## キャラクターの除去と復帰
```hoi4
# 除去
retire_character = TAG_character_name   # 国家スコープ
tag_character_name = { retire = yes }   # キャラクタースコープ

# 再度追加
set_nationality = TAG_character_name
```

### 推奨されないコマンド
- `kill_country_leader`
- `retire_country_leader`
- `kill_ideology_leader`
- `retire_ideology_leader`

代わりに `promote_character`, `remove_country_leader_role` を使用してください。

## その他の役職追加
```hoi4
add_corps_commander_role
add_field_marshal_role
add_naval_commander_role
add_advisor_role
```

### advisor_role 注意点
スクリプト付きアドバイザーに `remove_advisor_role` を使うと情報が失われます。`visible = { trigger }` を活用してください。

## アドバイザーの有効化
```hoi4
activate_advisor = TAG_character_name_token
```

## ポートレートの変更
```hoi4
# キャラクタースコープ
TAG_New_Leader = {
  set_portraits = {
    civilian = {
      large = "gfx/leaders/TAG/TAG_New_Leader.png"
      small = "gfx/advisors/TAG/TAG_New_Leader.png"
    }
  }
}

# 国家スコープ
set_portraits = {
  character = TAG_New_Leader
  civilian = {
    large = GFX_Large_Civilian_Portrait_TAG_New_Leader
    small = GFX_Small_Civilian_Portrait_TAG_New_Leader
  }
}
```

---

## 特殊ケース: `generate_character`

```hoi4
# historyファイルのテンプレートとして定義

every_country = {
  limit = { OR = { original_tag = KOR original_tag = SER original_tag = ICE } }
  generate_character = {
    token_base = army_chief_defensive_1
    name = "Character's Name"
    advisor = {
      idea_token = ac
      slot = army_chief
      traits = { army_chief_defensive_1 }
    }
  }
}

# 後で生成する場合:
generate_character = { token_base = army_chief_defensive_1 }
```

### 空のトリガーで即時生成を防ぐ
```hoi4
every_possible_country = {
  limit = { always = no }
  generate_character = {
    token_base = generic_guy
    name = "Advisor Clone"
    advisor = {
      slot = political_advisor
      idea_token = pol
      traits = { my_trait }
    }
  }
}

# 後から追加:
generate_character = { token_base = generic_guy }
```
