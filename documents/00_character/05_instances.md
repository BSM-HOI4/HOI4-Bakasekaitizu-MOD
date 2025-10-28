# 5. Instances

`instance = {}` を使うことで、ゲーム開始時の条件に応じてキャラクターの状態を切り替えることが可能です。

各 `instance` ブロックには必ず `allowed = {}` 条件が含まれており、条件を満たすインスタンスのみが適用されます。

これは、DLCの有無などによってキャラクターの役割や特性を変化させる際に便利です。

---

## 📘 例: DLCの有無によって役職が変化するキャラクター

```hoi4
my_character = {
    instance = {
        allowed = { has_dlc = "Poland: United and Ready" }
        advisor = {
            slot = political_advisor
            traits = { polish_person }
        }
    }

    instance = {
        allowed = { NOT = { has_dlc = "Poland: United and Ready" } }
        corps_commander = {
            skill = 10
            attack_skill = 10
            defense_skill = 10
            planning_skill = 10
            logistics_skill = 10
            traits = { not_polish_person }
        }
    }
}
```
## ✅ ポイント
 - 複数の instance を持つキャラクターに使用する。

 - 各 instance は allowed = {} を持たなければならない。

 - 条件に応じて、異なる役割（advisor, corps_commanderなど）を持たせることができる。

 - もし状態が一つしかないなら、instance ブロックは不要。