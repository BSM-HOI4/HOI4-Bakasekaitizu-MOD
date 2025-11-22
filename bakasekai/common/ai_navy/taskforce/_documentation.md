# Taskforce composition

## はじめに

特定の任務部隊（タスクフォース）の艦船数と、その部隊が利用可能な任務をスクリプト（記述）します。（注：利用可能な任務は、現在は1つに制限されています）

## スクリプト

```
generic_taskforce_1 = {
    allowed = {
        original_tag = GBR
    }
    ai_will_do = {
        # このテンプレートに対するAIの重み付け（ウェイト）修正値
        # 0以下の場合、AIはこのテンプレートを使用しません
        #
        # SCOPE（スコープ） = COUNTRY（国家）
        factor = 1
    }
    mission = { naval_patrol } # この任務部隊が実行できる適用可能な任務のリスト
    min_composition = { # 必要な最小編成（注：ここにはさらなる明確化が必要。ゴールシステムが任務部隊を使用する前の最小条件か？）
        carrier = 1 # 艦種と必要な数量
        battleship = 1
        heavy_cruiser = 1
        light_cruiser = 1
        destroyer = 1
    }
    
    optimal_composition = { # この任務部隊が保有する最大編成
        carrier = 2
        battleship = 2
        heavy_cruiser = 5
        light_cruiser = 3
        destroyer = 6
        submarine = 2
    }
}
```
