# 第二次エミュー戦争 コンテンツプラン（実装済み版）
## ブランチ: `feature/second-emu-war`
## 作成日: 2026-05-22 / 最終更新: 2026-05-22

---

## 概要・世界観

「第二次エミュー戦争」は、**エミュー帝国(AUS)** の支配する西オーストラリアで、
**ハットリバー公国(HRH)** が本土抵抗勢力として蜂起し、
タスマニアを拠点とする **オーストラリア連邦(AST)** が支援に駆けつけ、
さらに本国 **イギリス(GBR)** の思惑が絡む多角的な紛争シナリオ。

### 史実ベース（バカ世界地図解釈）
| 要素 | 史実 | 本MODでの解釈 |
|------|------|--------------|
| 大エミュー戦争(1932) | オーストラリア軍がエミュー駆除作戦に失敗 | エミューが勝利し「エミュー帝国」を樹立 |
| ハットリバー公国 | 1970年にオーストラリアから独立宣言した農場主 | 州1097を本拠地とする**本土抵抗勢力**。AUSに囲まれた孤立した抵抗組織 |
| イギリスとオーストラリア | コモンウェルス関係 | エミュー問題への干渉・コモンウェルス維持 vs 独立外交の駆け引き |

### HRHの正確な位置づけ
- **本土抵抗勢力**（亡命政権ではない）
- 拠点: 州1097（ハットリバー本拠地、HRH所有・core）
- 目標: 州884（西オーストラリア、AUS所有）を奪取して西海岸回廊を確保
- ASTの首都タスマニア(州518)とは海を隔てた関係 → ASTは海軍上陸が主要手段

---

## 関係国タグ一覧

| タグ | 国名 | 役割 | 拠点 |
|------|------|------|------|
| `AUS` | エミュー帝国 | 主敵 | 西オーストラリア全域 |
| `AST` | オーストラリア連邦 | 支援国・参戦勢力 | タスマニア（州518） |
| `HRH` | ハットリバー公国 | 本土抵抗勢力・主人公側 | ハットリバー（州1097） |
| `GBR` | イギリス | 第三勢力・コモンウェルス問題 | ロンドン |

---

## 実装済みファイル構成

```
bakasekai/
├── events/
│   └── second_emu_war_ast_support_events.txt  ✅ 実装済み
│       # Namespace: sew_support / sew_aus / sew_gbr
│       # 10イベント: sew_support.1〜8, sew_aus.1, sew_gbr.1
│
├── common/
│   ├── national_focus/
│   │   └── AST_second_emu_war.txt             ✅ 実装済み
│   │       # focus_tree id = ast_second_emu_war_focus
│   │       # 13フォーカス（3ブランチ+参戦+戦後）
│   │
│   ├── ideas/
│   │   └── second_emu_war_ideas.txt           ✅ 実装済み
│   │       # 16国家精神（AST×7 / HRH×6 / AUS×2 / GBR×1）
│   │
│   ├── ai_templates/
│   │   └── sew_templates.txt                  ✅ 実装済み
│   │       # 9テンプレート（HRH×3 / AST×3 / AUS×3）
│   │
│   ├── ai_strategy/
│   │   └── sew_strategies.txt                 ✅ 実装済み
│   │       # 19ストラテジー（HRH×6 / AST×8 / AUS×5）
│   │
│   └── ai_strategy_plans/
│       └── sew_strategy_plans.txt             ✅ 実装済み
│           # 3プラン（HRH×1 / AST×2）
│
└── localisation/japanese/bakasekai/
    └── second_emu_war_l_japanese.yml          ✅ 実装済み
        # 全コンテンツの日本語テキスト
```

---

## 既存コンテンツとの接続フロー

```
【HRH既存フォーカスツリー】
HRH_focus_1 → focus_2(TECH_1) → focus_3 → focus_4/focus_4A
    └→ focus_A2 → focus_A3 → focus_AB3
    └→ focus_A4 → focus_5(TECH_2: militia+irregular解放)
                    └→ focus_6(HRH_recapture_started セット)

【既存ディシジョン】
HRH_recapture_neighborhood (30日, 70%成功率)
    └→ 州884をHRHへ移譲
    └→ フラグ: HRH_recapture_success セット
    └→ news_event: HRH.1

【既存イベント】
HRH_recapture_states.1 (HRH視点) → HRH_recapture_states.2 (AST視点)
    └→ create_faction = Bokka_Alliance
    └→ add_to_faction = HRH
    └→ ★★★ sew_support.1 を HRH に送信 ★★★（← 新コンテンツへの接続点）

【新コンテンツ起動】
sew_support.1 (HRH): 支援要請を出すか選択
    └→ option.a → AST に sew_support.2 を送信
```

---

## イベント設計（実装済み）

### Namespace: `sew_support`（HRH/AST支援交渉）

| ID | 受信国 | タイトル | 概要 |
|----|--------|---------|------|
| `sew_support.1` | HRH | ASTへの支援要請 | 支援要請を出すか選択。option.a → AST に sew_support.2 送信 |
| `sew_support.2` | AST | ハットリバーからの要請 | 4択: a)装備支援 / b)顧問派遣 / c)参戦確認 / d)拒否 |
| `sew_support.3` | HRH | ASTの拒否通知 | HRH_sew_alone_spirit 獲得 |
| `sew_support.4` | HRH | 物資到着報告 | AST装備到着を確認、AST に sew_support.6 送信 |
| `sew_support.5` | AST | 参戦最終確認 | a)即時宣戦(declare_war_on AUS) / b)60日後再確認 |
| `sew_support.6` | AST | 追加支援要請受信 | 継続支援の確認イベント |
| `sew_support.7` | HRH | AST参戦通知 | war_support +0.15 |
| `sew_support.8` | AST | 英国参観武官 | a)AST_sew_british_liaison 取得 / b)AST_sew_independence_spirit 取得 |

### Namespace: `sew_aus`（AUS反応）

| ID | 受信国 | タイトル | 概要 |
|----|--------|---------|------|
| `sew_aus.1` | AUS | AST参戦への対応 | AUS_sew_war_footing または AUS_sew_defensive_posture 取得 |

### Namespace: `sew_gbr`（GBR対応）

| ID | 受信国 | タイトル | 概要 |
|----|--------|---------|------|
| `sew_gbr.1` | GBR | コモンウェルス緊急対応 | コモンウェルス介入・仲介・傍観の3択 |

---

## ASTフォーカスツリー設計（実装済み）

**focus_tree id**: `ast_second_emu_war_focus`  
**解禁条件**: `is_in_faction_with = HRH` または `has_country_flag = AST_sew_hrh_contacted`、かつ `HRH.has_country_flag = HRH_recapture_success`

```
[AST_sew_respond_to_hrh] x=7,y=0  HRH連絡・支援意思表示
    │                   (→ sew_support.1 を HRH に送信)
    │
    ├── [左ブランチ: 物資・装備支援]
    │   [AST_sew_supply_hrh] x=4,y=1  装備3000+支援300をHRHに
    │       ├── [AST_sew_artillery_support] x=3,y=2  砲兵装備400+研究ボーナス
    │       └── [AST_sew_naval_support] x=5,y=2  海上補給路確保(idea付与)
    │
    ├── [中央ブランチ: 軍事顧問・合同作戦]
    │   [AST_sew_send_advisors] x=7,y=1  HRH_sew_ast_advisors idea+経験値
    │       ├── [AST_sew_joint_training] x=6,y=2  HRHにドクトリン研究ボーナス×2
    │       └── [AST_sew_combined_ops_plan] x=8,y=2  HRH_sew_combined_ops_bonus(戦時限定)
    │
    ├── [右ブランチ: 英国外交]
    │   [AST_sew_contact_gbr] x=10,y=1  sew_gbr.1 を GBR に送信
    │       ├── [AST_sew_gbr_military_aid] x=9,y=2  GBR装備2000+AST_sew_british_support_active
    │       └── [AST_sew_gbr_independent] x=11,y=2  ★相互排他★ 独立路線(安定度+0.05)
    │
    └── [合流: 参戦・戦後]
        [AST_sew_mobilize] x=7,y=3  動員(左右どちらか経由後)
            └── [AST_sew_declare_war] x=7,y=4  join HRH + declare_war AUS
                ├── [AST_sew_post_war_hrh_recognition] x=5,y=5  HRH自治承認
                ├── [AST_sew_reclaim_west] x=7,y=5  州879-885をASTコアに追加
                └── [AST_sew_gbr_thank_you] x=9,y=5  英国感謝外交(GBR支援ルート限定)
```

---

## 国家精神設計（実装済み）

### AST用（7件）
| ID | 効果 |
|----|------|
| `AST_sew_war_mobilization` | 徴兵+0.05、陸軍経験値+0.10 |
| `AST_sew_war_preparation` | 工場効率+0.10、PP-20/月 |
| `AST_sew_british_liaison` | 研究速度+0.05、英国関係良化 |
| `AST_sew_british_support_active` | 装備受領ボーナス |
| `AST_sew_independence_spirit` | 安定度+0.05、戦意+0.05 |
| `AST_sew_western_coast_supply_route` | 海上補給路確保(HRH支援効率UP) |
| `AST_sew_west_reclaimed` | 西部再統合記念、安定度+0.10 |

### HRH用（6件）
| ID | 効果 |
|----|------|
| `HRH_sew_ast_equipped` | 歩兵攻撃+0.10、irregular攻撃+0.15 |
| `HRH_sew_ast_advisors` | 組織力回復+0.05、ドクトリン研究速度+0.10 |
| `HRH_sew_ast_full_support` | 戦意+0.15、回復速度+0.10 |
| `HRH_sew_combined_ops_bonus` | 合同作戦中の攻撃力ボーナス |
| `HRH_sew_alone_spirit` | 孤立無援、戦意のみ+0.10（デバフあり） |
| `HRH_sew_ast_recognition` | 戦後自治承認、安定度+0.15 |

### AUS用（2件）
| ID | 効果 |
|----|------|
| `AUS_sew_war_footing` | 徴兵+0.05、陸軍士気+0.10 |
| `AUS_sew_defensive_posture` | 防御戦闘力+0.15 |

### GBR用（1件）
| ID | 効果 |
|----|------|
| `GBR_sew_commonwealth_duty` | コモンウェルス義務遂行精神 |

---

## AI師団編制テンプレート設計（実装済み）

### HRH（3テンプレート）
```
HRH_sew_infantry (role=infantry, upgrade_prio×3)
  ├─ HRH_irregular_core: irregular×4+militia×3, recon+engineer
  │     └→ replace_with HRH_irregular_reinforced (at 80% match)
  ├─ HRH_irregular_reinforced: irregular×5+militia×3+infantry×1, +artillery
  │     └→ replace_with HRH_regular_combined (at 90% match)
  │     ※ HRH_sew_ast_equipped idea取得でupgrade_prio×3
  └─ HRH_regular_combined: infantry×6+irregular×3, recon+engineer+artillery+anti_tank
       ※ HRH_sew_ast_advisors idea取得でupgrade_prio×4

HRH_sew_garrison (role=garrison, upgrade_prio×2)
  └─ HRH_garrison_militia: militia×4

HRH_sew_suppression (role=suppression, upgrade_prio×1)
  └─ HRH_suppression_light: irregular×3+militia×2
```

### AST（3テンプレート）
```
AST_sew_infantry (role=infantry, upgrade_prio×3)
  ├─ AST_standard_infantry: infantry×9, engineer+artillery
  │     └→ replace_with AST_assault_infantry (at 90% match)
  └─ AST_assault_infantry: infantry×9+anti_tank_brigade×1, +anti_tank+recon
       ※ AST_sew_war_mobilization idea取得でupgrade_prio×3

AST_sew_marines (role=marines, upgrade_prio×2)
  └─ AST_marine_landing: marine×4+infantry×2, engineer+recon
       ※ AST_sew_declare_war完了でupgrade_prio×4

AST_sew_garrison (role=garrison, upgrade_prio×1)
  └─ AST_garrison_standard: infantry×4
```

### AUS（3テンプレート）
```
AUS_sew_infantry (role=infantry, upgrade_prio×3)
  ├─ AUS_emu_standard: infantry×9+cavalry×1（哨戒用）, recon+engineer
  │     └→ replace_with AUS_emu_wartime (at 90% match)
  └─ AUS_emu_wartime: infantry×9+militia×2, recon+engineer+artillery+anti_tank
       ※ AUS_sew_war_footing idea取得でupgrade_prio×5

AUS_sew_garrison (role=garrison, upgrade_prio×2)
  └─ AUS_garrison_wide: infantry×4+militia×2（広大な本土の広域維持）

AUS_sew_suppression (role=suppression, upgrade_prio×1)
  └─ AUS_suppression_cavalry: cavalry×4
```

---

## AI戦略ストラテジー設計（実装済み）

### HRH（6ストラテジー）

| ストラテジーID | enable条件 | 主な内容 |
|----------------|-----------|---------|
| `HRH_sew_peacetime_force` | original_tag=HRH, has_war=no | infantry=90, armor/cavalry=-100, garrison=5 |
| `HRH_sew_wartime_force` | original_tag=HRH, has_war_with=AUS | infantry=85, garrison=10, 歩兵装備+60, 砲兵+20 |
| `HRH_sew_research_priority` | original_tag=HRH | infantry_weapons+40, support+30, land_doctrine+20, naval=-80 |
| `HRH_sew_diplomacy_support_ast` | HRH, AST存在 | befriend AST+200, alliance AST+100 |
| `HRH_sew_diplomacy_oppose_aus` | HRH, AUS存在 | antagonize AUS+100 |
| `HRH_sew_production_priority` | original_tag=HRH | arms_factory+100, infrastructure+20 |
| `HRH_sew_supplied_by_ast` | HRH_sew_ast_equipped取得時 | 歩兵装備生産-20（AST支給分を相殺） |

### AST（8ストラテジー）

| ストラテジーID | enable条件 | 主な内容 |
|----------------|-----------|---------|
| `AST_sew_base_force` | original_tag=AST | infantry=75, marines=5, garrison=10 |
| `AST_sew_wartime_force` | AST, has_war_with=AUS | marines=15, 海軍convoy+15, 歩兵装備+50 |
| `AST_sew_research_priority` | original_tag=AST | naval+35, infantry+30, support+25 |
| `AST_sew_diplomacy_hrh` | HRH.has_country_flag=HRH_recapture_success | befriend HRH+200, support HRH+100 |
| `AST_sew_diplomacy_gbr` | GBR存在 | befriend GBR+50 |
| `AST_sew_diplomacy_oppose_aus` | AUS存在 | antagonize AUS+150 |
| `AST_sew_supply_hrh_ai` | HRH戦争中, AST平時 | support HRH+150（自動支援意欲） |
| `AST_sew_area_priority` | AST, has_war_with=AUS | oceania+200, pacific+100, europe=-100, naval_invasion+200 |

### AUS（5ストラテジー）

| ストラテジーID | enable条件 | 主な内容 |
|----------------|-----------|---------|
| `AUS_sew_base_force` | original_tag=AUS | infantry=80, garrison=8, cavalry=3, armor=-80 |
| `AUS_sew_wartime_force` | AUS, 戦争中+war_footing | infantry=85, garrison=10, 歩兵装備+60 |
| `AUS_sew_defend_west` | AUS, has_war_with=HRH, 884未制御 | oceania+300, conquer HRH+100 |
| `AUS_sew_research_priority` | original_tag=AUS | infantry_weapons+40, land_doctrine+25 |
| `AUS_sew_oppose_gbr` | GBRがASTと同盟 or GBR_sew_commonwealth_duty | antagonize GBR+100 |

---

## AIストラテジープラン設計（実装済み）

### HRH_sew_resistance_plan（常時有効）
- **概要**: 本土抵抗勢力として武装強化→外交→西海岸奪還の一本道
- **フォーカス順**: focus_1→2→A2→3→A3→4→4A→AB3→A4→5→6→7→8
- **research**: infantry_weapons=50, support_tech=30, land_doctrine=25, naval=-99
- **focus_factors**: focus_5×2.0 / focus_6×2.0 / focus_8×3.0
- **weight**: 基本1.0、HRH_recapture_success後×1.5

### AST_sew_intervention_plan（積極介入、Bokka_Alliance参加後に有効化）
- **概要**: HRH全面支援→参戦→西部奪還の積極路線
- **フォーカス順**: respond→send_advisors→supply→joint_training→artillery→naval→combined_ops→contact_gbr→gbr_aid→mobilize→declare→reclaim_west→recognition→gbr_thanks
- **research**: naval_equipment=45, infantry_weapons=35, support_tech=25
- **focus_factors**: send_advisors×3.0 / mobilize×2.5 / declare_war×3.0 / reclaim_west×2.0
- **weight**: 基本1.0、Bokka_Alliance参加で×2.0、参戦後×1.5

### AST_sew_defense_plan（国防優先、Bokka_Alliance未参加時）
- **概要**: タスマニア防衛優先・物資支援のみ・直接参戦回避
- **フォーカス順**: respond→supply→artillery→naval→contact_gbr→gbr_independent
- **research**: naval_equipment=40, infantry_weapons=40
- **focus_factors**: supply×2.0, naval_support×2.0, gbr_independent×2.5, mobilize=0.0, declare_war=0.0
- **weight**: 基本0.5、AST_sew_independence_spirit取得で×2.0、AUS戦争中は×0.0（プラン無効化）

---

## ゲームフロー（実装済みシナリオ）

```
1936年スタート
    │
    ├─ HRH：既存フォーカスツリー進行
    │   focus_1→2→3→4/4A→A2→A3→AB3→A4→5(TECH_2解放)→6(recapture_started)
    │                                                         ↓
    │              ディシジョン: HRH_recapture_neighborhood (30日, 70%成功)
    │                                                         ↓
    │              HRH_recapture_success フラグ → focus_7→8
    │                                                         ↓
    │              HRH_recapture_states.2 (AST視点) → Bokka_Alliance 結成
    │                                                         ↓
    │              sew_support.1 が HRH に届く ★新コンテンツ開始★
    │
    ├─ AST：sew_support.2 受信後の4択
    │   ├─ a) 装備支援 → HRH_sew_ast_equipped idea + 装備2000 + sew_support.4
    │   ├─ b) 顧問派遣 → HRH_sew_ast_advisors idea + tech_bonus
    │   ├─ c) 参戦確認 → AST_sew_ready_to_intervene フラグ → sew_support.5
    │   └─ d) 拒否 → HRH_sew_alone_spirit idea → sew_support.3
    │
    ├─ AST フォーカスツリー（ast_second_emu_war_focus）
    │   ├─ 積極介入プラン（AI: AST_sew_intervention_plan）
    │   │   respond→advisors/supply→joint/artillery/naval→mobilize→declare_war
    │   │       └→ 戦後: reclaim_west / recognition / gbr_thanks
    │   └─ 消極支援プラン（AI: AST_sew_defense_plan）
    │       respond→supply→naval→contact_gbr→gbr_independent
    │
    └─ AUS：sew_aus.1受信 → war_footing または defensive_posture を選択

【エンドステート分岐】
  A: AST勝利  → reclaim_west（州879-885がASTコア）+ HRH自治承認
  B: 交渉停戦 → gbr_thank_you（英国仲介ルート）
  C: AUS勝利  → HRH_sew_alone_spirit 持続、AST撤退
```

---

## ローカライゼーション（実装済み）

**ファイル**: `bakasekai/localisation/japanese/bakasekai/second_emu_war_l_japanese.yml`

収録テキスト:
- フォーカス名・説明文（13フォーカス分）
- イベントタイトル・本文・選択肢テキスト（10イベント分）
- 国家精神名・フレーバーテキスト（16精神分）
- 関連ツールチップ（`_tt` キー）

---

## 実装状況チェックリスト

| 項目 | ステータス | コミット |
|------|-----------|---------|
| ブランチ作成 (`feature/second-emu-war`) | ✅ 完了 | — |
| コンテンツプランドキュメント初版 | ✅ 完了 | `1de65044` |
| HRH「本土抵抗勢力」方針確認 | ✅ 完了 | — |
| AST支援イベント (`second_emu_war_ast_support_events.txt`) | ✅ 完了 | `f66a895b` |
| ASTフォーカスツリー (`AST_second_emu_war.txt`) | ✅ 完了 | `f66a895b` |
| 国家精神 (`second_emu_war_ideas.txt`) | ✅ 完了 | `f66a895b` |
| 日本語ローカライゼーション | ✅ 完了 | `f66a895b` |
| AI師団編制テンプレート (`sew_templates.txt`) | ✅ 完了 | `a311d160` |
| AIストラテジー (`sew_strategies.txt`) | ✅ 完了 | `a311d160` |
| AIストラテジープラン (`sew_strategy_plans.txt`) | ✅ 完了 | `a311d160` |
| コンテンツプランドキュメント修正版 | ✅ 完了 | — |

---

## 将来の拡張候補（未実装）

| 優先度 | 作業 | 備考 |
|--------|------|------|
| 🟡 中 | `HRH_second_emu_war.txt` | HRHフォーカスツリー拡張（focus_8以降の継続） |
| 🟡 中 | `GBR_emu_intervention.txt` | GBR介入フォーカス3本 |
| 🟡 中 | `second_emu_war_decisions.txt` | AST/HRH/GBR追加ディシジョン群 |
| 🟢 低 | sew_aus追加イベント | AUSの詳細な反応イベント追加 |
| 🟢 低 | 英語ローカライゼーション | `second_emu_war_l_english.yml` |
| 🟢 低 | GFXアイコン | カスタムフォーカスアイコン追加 |

---

## 注意事項・実装ガイドライン

### 既存コンテンツとの接続ポイント
- **接続点**: `HRH_recapture_states.2`（AST側イベント）内で `sew_support.1` を HRH に送信
- **既存ディシジョン**: `HRH_recapture_neighborhood` (decisions/HRH.txt) は無改変で動作
- **AIテンプレート競合**: `ai_templates_minor_cost_focus.txt` の `available_for` にHRHが既含 → 新テンプレートは `upgrade_prio×3` 以上で上書き

### 技術的制約
- HRH_TECH_2（militia+irregular解放）は `HRH_focus_5` 完了で自動取得 → AIテンプレートで安全に使用可
- ASTの海軍上陸が主軸（タスマニア→西オーストラリア）→ marines roleとnaval_invasion_focusが重要
- Bokka_Alliance（`create_faction = Bokka_Alliance`）は既存イベントで作成済み

### コーディング規約
- イベントID: `sew_support.N`, `sew_aus.N`, `sew_gbr.N`
- フォーカスID: `AST_sew_*`
- アイデアID: `AST_sew_*`, `HRH_sew_*`, `AUS_sew_*`, `GBR_sew_*`
- テンプレートID: `HRH_sew_*` / `AST_sew_*` / `AUS_sew_*`
- ストラテジーID: `HRH_sew_*` / `AST_sew_*` / `AUS_sew_*`
- プランID: `HRH_sew_*` / `AST_sew_*`

### バカ世界地図の精神
- エミューはあくまで「勝利した知性を持つ鳥」として描写
- シリアスになりすぎず、笑えるフレーバーテキストを心がける
- ハットリバーの「農場主が独立を宣言した」設定を活かした小国感
- イギリスは「なぜかコモンウェルスで鳥と戦う羽目になった」感を演出
- エミュー帝国の「防衛戦争」宣言は徹底したギャグ路線で
