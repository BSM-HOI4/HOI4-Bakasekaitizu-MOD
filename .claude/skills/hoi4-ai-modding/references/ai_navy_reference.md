# ai_navy リファレンス(目標ベース海軍AI)

HOI4 1.13系の海軍AI。「ゴール(goal)→オブジェクティブ(objective)→艦隊(fleet)→任務部隊(taskforce)」の階層で海軍運用を決める。
配置: `common/ai_navy/` 配下の3サブフォルダ。

**一次資料**: `bakasekai/common/ai_navy/_documentation.md`(日本語の詳細解説)を必ず読むこと。
このリファレンスは構造の早見表のみ。

## 全体像

1. **goals/** — 「何をしたいか」(制海権、船団護衛、上陸支援…)と優先度レンジ
2. ゲーム側がgoalから具体的なobjective(対象海域・対象侵攻)を生成しスコアリング
3. **fleet/** — objectiveを実行する艦隊テンプレート(必要taskforceの組み合わせ)
4. **taskforce/** — 任務部隊の艦種構成テンプレート

## goals/ の構造(goals_generic.txt 準拠)

```
generic_naval_dominance = {
  objective_type = naval_dominance   # エンジン定義のobjectiveタイプ
  min_priority = 1                   # 優先度レンジ下限
  max_priority = 16                  # 上限(objective重要度0〜1でレンジ内に写像)
  # enable = { ... }                 # (任意)有効条件
  # priority = { ... }               # (任意)動的優先度modifier
}
```

mod内 goals_generic.txt にある objective_type:
`naval_invasion_support`, `mines_sweeping`, `naval_invasion_defense`, `coast_defense`,
`convoy_protection`, `convoy_raiding`, `naval_dominance` ほか(mines_planting, naval_superiority系は_documentation.md参照)

## fleet/ の構造(generic_fleet_templates.txt 準拠)

```
generic_dominance_fleet_1 = {
  required_taskforces = {            # 艦隊成立に必須のtaskforceテンプレートと数
    StrikeForce_1 = 1
    PatrolDominanceForce_CA_1 = 2
    PatrolReconForce_1 = 2
  }
  optional_taskforces = {            # 余裕があれば追加
    StrikeForce_1 = 1
  }
}
```

## taskforce/ の構造

キー名(`StrikeForce_1` 等)が fleet/ から参照される。

```
ENG_StrikeForce_1 = {
  allowed = {                        # 使用国の限定(開始時1回評価)
    original_tag = GBR
  }
  ai_will_do = {
    factor = 1
  }
  mission = { naval_strike }         # 担当ミッション
  min_composition = {                # 成立に必要な最小構成
    destroyer = { amount = 8 }
  }
  optimal_composition = {            # 理想構成(ここまで増強する)
    carrier = { amount = 2 }
    battleship = { amount = 4 }
    heavy_cruiser = { amount = 4 }
    light_cruiser = { amount = 4 }
    destroyer = { amount = 28 }
  }
}
```

実例は `bakasekai/common/ai_navy/taskforce/`(国別ファイルはコメントアウト部分に書式例あり)。

## ai_equipment との整合

taskforceが要求する艦種ロール(naval_screen, naval_capital等)は、
[ai_equipment_reference.md](ai_equipment_reference.md) の設計グループ `roles` が供給する。
「設計されない艦種を要求するtaskforce」は永遠に編成されないので、国別に追加する際は両方を確認する。

## 国別カスタマイズ手順

1. `goals_generic.txt` / `generic_fleet_templates.txt` がfallbackとして適用される
2. 国別に変えたい場合は `goals_TAG.txt` / `TAG_fleet_templates.txt` を作成(既存の `goals_JAP.txt` 等を雛形に)
3. 優先度レンジの目安: mod内では 1〜16 の範囲。特定戦略を強制したいときは min_priority を他goalのmaxより上げる
4. 検証: 観戦モード(`human_ai` + tag切替)で艦隊の任務割当を確認

## mod内実例

- `bakasekai/common/ai_navy/_documentation.md` — 仕組みの解説(最重要)
- `bakasekai/common/ai_navy/goals/goals_generic.txt`, `goals_JAP.txt` ほか主要国分
- `bakasekai/common/ai_navy/fleet/generic_fleet_templates.txt`, 主要国別ファイル
- `bakasekai/common/ai_navy/taskforce/` — 任務部隊構成
