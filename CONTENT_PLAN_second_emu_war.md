# 第二次エミュー戦争 コンテンツプラン
## ブランチ: `feature/second-emu-war`
## 作成日: 2026-05-22

---

## 概要・世界観

「第二次エミュー戦争」は、**エミュー帝国(AUS)** の勢力拡大に対し、
**オーストラリア連邦(AST)** と **ハットリバー公国(HRH)** が共同戦線を張り、
さらに本国イギリス **(GBR)** の介入・思惑が絡む多角的な紛争シナリオ。

### 史実ベース（バカ世界地図解釈）
| 要素 | 史実 | 本MODでの解釈 |
|------|------|--------------|
| 大エミュー戦争(1932) | オーストラリア軍がエミュー駆除作戦に失敗 | エミューが勝利し「エミュー帝国」を樹立 |
| ハットリバー公国 | 1970年にオーストラリアから独立宣言 | エミューに領土を奪われた亡命政権 |
| イギリスとオーストラリア | コモンウェルス関係 | エミュー問題への干渉・コモンウェルス維持 vs 放棄の駆け引き |

---

## 関係国タグ一覧

| タグ | 国名 | 役割 |
|------|------|------|
| `AUS` | エミュー帝国 | 今回の主な敵対勢力 |
| `AST` | オーストラリア連邦 | 主人公側・反エミュー連合の中核 |
| `HRH` | ハットリバー公国 | 亡命政権・AST側盟友 |
| `GBR` | イギリス | 第三勢力・コモンウェルス問題で介入 |

---

## 新規ファイル構成

```
bakasekai/
├── events/
│   ├── second_emu_war_events.txt       # 第二次エミュー戦争イベント群(AST/HRH視点)
│   ├── second_emu_war_gbr_events.txt   # イギリス介入イベント群
│   └── second_emu_war_aus_events.txt   # エミュー帝国側反応イベント群
├── common/
│   ├── national_focus/
│   │   ├── AST_second_emu_war.txt      # AST用フォーカスツリー拡張
│   │   ├── HRH_second_emu_war.txt      # HRH用フォーカスツリー拡張
│   │   └── GBR_emu_intervention.txt    # GBR介入フォーカス(小規模)
│   ├── ideas/
│   │   └── second_emu_war_ideas.txt    # 新国家精神・国家方針
│   └── decisions/
│       └── second_emu_war_decisions.txt # 関連ディシジョン
└── localisation/
    └── japanese/bakasekai/
        └── second_emu_war_l_japanese.yml
```

---

## フォーカスツリー設計

### AST（オーストラリア連邦）拡張ツリー
**フォーカスツリーID**: `ast_second_emu_war_focus`（既存`australia.txt`への追加も検討）

```
[AST_sew_root] 第二次エミュー戦争への備え
    │
    ├── [AST_sew_recall_emu_war]  大エミュー戦争の教訓
    │       └── [AST_sew_new_doctrine]  対エミュー戦闘教義
    │               └── [AST_sew_anti_emu_unit]  エミュー駆除部隊創設
    │
    ├── [AST_sew_hrh_alliance]  ハットリバーと手を組む
    │       └── [AST_sew_combined_arms]  合同作戦計画
    │               └── [AST_sew_liberation_of_west]  西部解放作戦
    │
    ├── [AST_sew_gbr_request]  英国への援助要請
    │       ├── [AST_sew_gbr_accepted]  英国軍の上陸支援(GBR友好時)
    │       └── [AST_sew_gbr_rejected]  独力で戦う(GBR拒否時)
    │
    └── [AST_sew_total_war]  総力戦宣言
            └── [AST_sew_final_push]  最終攻勢
                    └── [AST_sew_victory]  エミュー帝国の解体
```

---

### HRH（ハットリバー公国）拡張ツリー
**既存ツリーへの追加フォーカス**

```
[HRH_focus_8]（既存：牧歌同盟の結成）の後続
    │
    ├── [HRH_sew_rearm]         再武装計画
    │       └── [HRH_sew_militia_elite]  精鋭民兵団
    │
    ├── [HRH_sew_legitimacy]    正統性の宣言
    │       └── [HRH_sew_gbr_recognition] GBRへの承認要請
    │               ├── [HRH_sew_commonwealth_member] コモンウェルス加盟
    │               └── [HRH_sew_full_independence]  完全独立路線
    │
    └── [HRH_sew_intel_network]  諜報網構築
            └── [HRH_sew_sabotage]  エミュー帝国内部工作
```

---

### GBR（イギリス）介入フォーカス（小規模）

```
[GBR_emu_crisis] エミュー危機への対応
    ├── [GBR_emu_intervene]     軍事介入 → ASTへの軍事支援
    ├── [GBR_emu_mediate]       調停外交 → 停戦交渉
    └── [GBR_emu_abandon]       傍観      → コモンウェルス弱体化
```

---

## イベントシナリオ設計

### Namespace: `second_emu_war`（AST/HRH視点）

| ID | タイトル | 発火条件 | 概要 |
|----|---------|---------|------|
| `second_emu_war.1` | 第二次エミュー戦争の予兆 | AST, fire_only_once, date>1937.1.1 | エミュー帝国の膨張を察知したAST首脳部の緊急会議 |
| `second_emu_war.2` | 国境侵犯事件 | AST, AUSと隣接後N月 | AUSの小部隊がAST領土内に侵入 |
| `second_emu_war.3` | ハットリバーからの救援要請 | AST, HRH存在時 | HRHがASTに共同作戦を要請 |
| `second_emu_war.4` | 英国大使の訪問 | AST, GBR健在時 | GBRがコモンウェルス維持を条件に援助を申し出る |
| `second_emu_war.5` | 砂漠の罠 | AST, has_war=AUS | エミュー軍が砂漠地帯に誘引作戦を展開 |
| `second_emu_war.6` | ハットリバー民兵の奮闘 | HRH, has_war=AUS | HRH民兵が英雄的な防衛戦を展開 |
| `second_emu_war.7` | 開戦宣言 | AST, フォーカス完了時 | 正式な対エミュー帝国宣戦布告 |
| `second_emu_war.8` | 西部戦線の突破 | AST, 特定州占領後 | 西オーストラリア州の一部解放成功 |
| `second_emu_war.9` | エミュー皇帝の演説 | AUS視点でも通知 | エミュー帝国が「聖戦」を宣言 |
| `second_emu_war.10` | 停戦か継続か | AST, AUSの首都占領後 | 戦後処理の分岐点 |

---

### Namespace: `sew_gbr`（イギリス介入イベント）

| ID | タイトル | 発火条件 | 概要 |
|----|---------|---------|------|
| `sew_gbr.1` | エミュー問題とコモンウェルス | GBR, date>1937.3.1 | 議会でオーストラリア問題が議題に |
| `sew_gbr.2` | オーストラリアからの支援要請 | GBR, AST発火後 | ASTのSOSを受け取ったGBR |
| `sew_gbr.3` | 軍事顧問団の派遣 | GBR, 支援選択後 | GBR軍事顧問がAST軍を指導 |
| `sew_gbr.4` | コモンウェルス会議の招集 | GBR, 調停選択後 | カナダ・NZも巻き込んだ外交交渉 |
| `sew_gbr.5` | 英国の撤退 | GBR, 傍観選択後 | コモンウェルス関係の見直し通告 |

---

### Namespace: `sew_aus`（エミュー帝国反応）

| ID | タイトル | 発火条件 | 概要 |
|----|---------|---------|------|
| `sew_aus.1` | 侵略宣言の正当化 | AUS, AST宣戦後 | エミュー帝国議会が「防衛戦争」と宣言 |
| `sew_aus.2` | 英国干渉への警告 | AUS, GBR支援後 | GBRへの外交的抗議 |
| `sew_aus.3` | エミュー統一戦線 | AUS, 特定条件 | 野生エミューを徴兵する緊急令 |

---

## 国家精神（Ideas）設計

### `second_emu_war_ideas.txt`

```
# AST用
AST_sew_mobilization         # 総動員令 - 兵力+、安定度-
AST_sew_anti_emu_doctrine    # 対エミュー教義 - 対歩兵戦闘ボーナス
AST_sew_british_support      # 英国の支援 - 研究速度+、政治力+
AST_sew_independence_spirit  # 独立不羈の精神 - 降伏限界+（英国拒否ルート）

# HRH用
HRH_sew_liberation_cause     # 解放の大義 - 戦意+、士気+
HRH_sew_guerrilla_mastery    # ゲリラ戦の極意 - 防御戦闘+

# GBR関連
GBR_emu_intervention_cost    # 介入コスト - 消費財-、政治力消費+（軍事介入時ペナルティ）
GBR_colonial_scrutiny        # 植民地問題の監視 - 自治領独立傾向+（傍観ルートのペナルティ）

# AUS（エミュー帝国）用
AUS_sew_war_footing          # 第二次大戦体制 - 徴兵+、生産効率+
AUS_sew_surrounded           # 四面楚歌 - 防御+、攻撃-（包囲された場合）
```

---

## ディシジョン設計

### `second_emu_war_decisions.txt`

```
# AST用ディシジョン
AST_sew_call_hrh_alliance    # ハットリバーに合流を呼びかける（HRH参戦促進）
AST_sew_scorched_earth       # 焦土作戦（エミュー追撃妨害、プロビンス破壊と引き換え）
AST_sew_demand_gbr_help      # GBRへの正式援助要請
AST_sew_war_bonds            # 戦時国債発行（工場建設資金）

# HRH用ディシジョン
HRH_sew_request_recognition  # GBRへ国家承認を要請
HRH_sew_partisan_ops         # エミュー帝国領内でのパルチザン活動
HRH_sew_covert_supply        # ASTから非公式に武器供給を受ける

# GBR用ディシジョン
GBR_sew_deploy_advisors      # 軍事顧問団の派遣（AST強化）
GBR_sew_naval_blockade       # 海上封鎖（AUSの輸入妨害）
GBR_sew_broker_ceasefire     # 停戦仲介（AUSとASTの交渉）
```

---

## ゲームフロー（シナリオ分岐）

```
1936年スタート
    │
    ├─ HRH：沿岸奪還フォーカス（既存）完了
    │       ↓
    │    牧歌同盟の結成(既存) → [新] 第二次エミュー戦争フォーカス解禁
    │
    ├─ AST：第二次エミュー戦争フォーカスツリー開始
    │   │
    │   ├─ 英国援助要請ルート
    │   │   ├─ GBR受諾 → 英国顧問団+コモンウェルス戦争
    │   │   └─ GBR拒否 → 独立路線（安定度ボーナス、GBR関係悪化）
    │   │
    │   └─ 総力戦宣言ルート
    │       └─ HRH合流 → 西部解放作戦 → AUS首都包囲
    │
    └─ AUS：防衛・反撃フォーカスが発動
        │
        ├─ GBR干渉なし → AUS拡張継続、AST苦境
        └─ GBR介入あり → AUS多正面作戦で苦境

【エンドステート分岐】
  A: AST勝利  → エミュー帝国解体、HRH独立承認、オーストラリア再統一
  B: 停戦     → 暫定国境線で膠着、GBR調停成立
  C: AUS勝利  → AST敗北、HRH消滅、エミュー帝国がコモンウェルスを脅かす
```

---

## ローカライゼーション計画

### `second_emu_war_l_japanese.yml`

- フォーカス名・説明テキスト（日本語）
- イベントタイトル・本文・選択肢（日本語）
- 国家精神名・説明（日本語）
- ディシジョン名・説明（日本語）

※英語ローカライゼーション (`second_emu_war_l_english.yml`) は後続作業

---

## 優先実装順序

| 優先度 | 作業 | 備考 |
|--------|------|------|
| 🔴 高 | `second_emu_war_events.txt` | コアとなるイベント10本 |
| 🔴 高 | `second_emu_war_ideas.txt` | 国家精神6本 |
| 🔴 高 | `second_emu_war_l_japanese.yml` | 全テキストのローカライゼーション |
| 🟡 中 | `AST_second_emu_war.txt` | ASTフォーカスツリー拡張 |
| 🟡 中 | `HRH_second_emu_war.txt` | HRHフォーカスツリー拡張 |
| 🟡 中 | `second_emu_war_decisions.txt` | ディシジョン8本 |
| 🟢 低 | `sew_gbr_events.txt` | GBRイベント5本 |
| 🟢 低 | `sew_aus_events.txt` | AUSイベント3本 |
| 🟢 低 | `GBR_emu_intervention.txt` | GBRフォーカス3本 |

---

## 注意事項・実装ガイドライン

### 既存コンテンツとの接続ポイント
- **HRHフォーカス**: `HRH_focus_8`（牧歌同盟の結成）の完了後に `HRH_sew_rearm` を解禁
- **ASTフォーカス**: `AST_commonwealth` コスメティックタグ使用中なので国旗・UI維持に注意
- **AUSフォーカス**: `AUS_great_emu_war_victory` の後続ルートとして位置づける
- **イベント namespace 競合**: 既存 `emu`, `emu_empire`, `HRH`, `HRH_recapture_states` と重複しないこと

### コーディング規約
- イベントID: `second_emu_war.N`、`sew_gbr.N`、`sew_aus.N`
- フォーカスID: `AST_sew_*`、`HRH_sew_*`、`GBR_sew_*`
- アイデアID: `AST_sew_*`、`HRH_sew_*`、`GBR_sew_*`、`AUS_sew_*`
- ディシジョンID: `AST_sew_*`、`HRH_sew_*`、`GBR_sew_*`

### バカ世界地図の精神
- エミューはあくまで「勝利した知性を持つ鳥」として描写
- シリアスになりすぎず、笑えるフレーバーテキストを心がける
- ハットリバーの「農家が独立を宣言した」設定を活かした小国感
- イギリスは「なぜかコモンウェルスで鳥と戦う羽目になった」感を演出
