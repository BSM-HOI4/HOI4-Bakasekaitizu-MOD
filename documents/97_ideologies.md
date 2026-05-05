# イデオロギーシステム技術仕様書 (Ideology System Technical Specification)

## 概要

BSMmodのイデオロギーシステムは、vanilla HOI4の4つのイデオロギー（民主主義、共産主義、ファシズム、中道派）から大幅に拡張され、**21の主要イデオロギー**と**86のサブイデオロギー**で構成されています。このシステムにより、プレイヤーはより多様で複雑な政治的・社会的シミュレーションを体験できます。

### 主な特徴

- **21の主要イデオロギー**: vanillaの4つに加え、独自の17のイデオロギーを追加
- **86のサブイデオロギー**: 各主要イデオロギー内で、より具体的な思想や政策を表現
- **独自のModifier**: 各イデオロギーは独自の政治的・経済的・軍事的効果を持つ
- **AI挙動のカスタマイズ**: 各イデオロギーに最適化されたAI挙動を設定
- **世界緊張度への影響**: イデオロギーによって戦争や陣営形成が世界緊張度に与える影響が異なる

## システム構造

### イデオロギー定義ファイルの場所

```
bakasekai/common/ideologies/00_ideologies.txt
```

### 基本的な構造

```hoi4
ideologies = {
    [ideology_key] = {
        types = {
            [sub_ideology_key] = {
                can_be_randomly_selected = yes/no  # オプション
            }
        }
        color = { R G B }
        rules = { ... }
        modifiers = { ... }
        faction_modifiers = { ... }
        dynamic_faction_names = { ... }
        can_host_government_in_exile = yes/no
        can_collaborate = yes/no
        war_impact_on_world_tension = 0.x
        faction_impact_on_world_tension = 0.x
        ai_[behavior] = yes
    }
}
```

### 主要なパラメータ説明

| パラメータ | 説明 |
|-----------|------|
| `types` | サブイデオロギーの定義 |
| `color` | マップ上の色（RGB値、0-255） |
| `rules` | 外交・軍事行動の制限ルール |
| `modifiers` | 国全体に与える効果 |
| `faction_modifiers` | 陣営メンバーに与える効果 |
| `dynamic_faction_names` | 陣営名の候補リスト |
| `can_host_government_in_exile` | 亡命政府を受け入れ可能か |
| `can_collaborate` | 協力政府に参加可能か |
| `war_impact_on_world_tension` | 戦争が世界緊張度に与える影響（0-1） |
| `faction_impact_on_world_tension` | 陣営形成が世界緊張度に与える影響（0-1） |
| `ai_[behavior]` | AI挙動（democratic/communist/fascist/neutral） |

## 主要イデオロギー一覧

### 1. 民主主義 (democratic_ideology)

**色**: RGB(20, 20, 255) - 青

**AI挙動**: `ai_democratic`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.25
- `faction_impact_on_world_tension`: 0.1

**外交ルール**:
```hoi4
rules = {
    can_create_collaboration_government = no
    can_declare_war_on_same_ideology = no
    can_force_government = yes
    can_send_volunteers = no
    can_puppet = no
    can_lower_tension = yes
    can_only_justify_war_on_threat_country = yes
    can_guarantee_other_ideologies = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: yes
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    generate_wargoal_tension = 1
    join_faction_tension = 0.8
    lend_lease_tension = 0.5
    send_volunteers_tension = 0.5
    guarantee_tension = 0.25
    annex_cost_factor = 0.5
    civilian_intel_to_others = 20
    army_intel_to_others = 5
    navy_intel_to_others = 20
    airforce_intel_to_others = 5
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0.5  # +50% 貿易意見
}
```

**サブイデオロギー**:
1. `liberalism` (自由主義)
2. `socialism` (社会主義)

**ローカライズキー**:
- `democratic_ideology`: "民主主義"
- `democratic_ideology_desc`: "民主主義政府"

---

### 2. 共産主義 (communism_ideology)

**色**: RGB(255, 0, 0) - 赤

**AI挙動**: `ai_communist`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.75
- `faction_impact_on_world_tension`: 0.5

**外交ルール**:
```hoi4
rules = {
    can_force_government = no
    can_send_volunteers = yes
    can_puppet = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: yes

**主要Modifiers**:
```hoi4
modifiers = {
    puppet_cost_factor = -0.3
    civilian_intel_to_others = 10
    army_intel_to_others = 7.5
    navy_intel_to_others = 12.5
    airforce_intel_to_others = 7.5
    hidden_modifier = {
        join_faction_tension = -0.1
    }
}
```

**動的陣営名**:
```
"FACTION_NAME_COMMUNIST_1"
"FACTION_NAME_COMMUNIST_2"
"FACTION_NAME_COMMUNIST_3"
"FACTION_NAME_COMMUNIST_4"
"FACTION_NAME_COMMUNIST_5"
```

**サブイデオロギー**:
1. `marxism` (マルクス主義)
2. `anarchist_communism` (アナルコ共産主義)
3. `leninism` (レーニン主義)
4. `stalinism` (スターリン主義)

**ローカライズキー**:
- `communism_ideology`: "共産主義"
- `communism_ideology_desc`: "全ての生産手段は国家という名の巨大なロボットが管理する。労働者はロボットのために働き、ロボットは皆のためにパンを焼く...はずだ。"

---

### 3. ファシズム (fascism_ideology)

**色**: RGB(150, 75, 0) - 茶色

**AI挙動**: `ai_fascist`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 1.0
- `faction_impact_on_world_tension`: 1.0

**外交ルール**:
```hoi4
rules = {
    can_force_government = no
    can_send_volunteers = yes
    can_puppet = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: yes

**主要Modifiers**:
```hoi4
modifiers = {
    justify_war_goal_when_in_major_war_time = -0.8
    civilian_intel_to_others = 15
    army_intel_to_others = 10
    navy_intel_to_others = 10
    airforce_intel_to_others = 10
    hidden_modifier = {
        join_faction_tension = -0.1
    }
}
```

**動的陣営名**:
```
"FACTION_NAME_FASCIST_1"
"FACTION_NAME_FASCIST_2"
"FACTION_NAME_FASCIST_3"
"FACTION_NAME_FASCIST_4"
"FACTION_NAME_FASCIST_5"
```

**サブイデオロギー**:
1. `nazism` (ナチズム)
2. `fascism_ideology` (ファシズム)
3. `gen_nazism` (ジェネリック・ナチズム)
4. `falangism` (ファランジズム)
5. `rexism` (レクシズム)
6. `coastisim` (海岸主義) ※ `can_be_randomly_selected = no`

**ローカライズキー**:
- `fascism_ideology`: "ファシズム"
- `fascism_ideology_desc`: "国家こそが絶対であり、国民はその栄光のために全てを捧げる運命共同体。力強い指導者の下、世界を自分たちの色に塗り替えることを目指す。"

---

### 4. 中道派 (neutrality_ideology)

**色**: RGB(124, 124, 124) - 灰色

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.25
- `faction_impact_on_world_tension`: 0.1

**外交ルール**:
```hoi4
rules = {
    can_force_government = no
    can_puppet = yes
    can_send_volunteers = no
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    generate_wargoal_tension = 0.5
    join_faction_tension = 0.4
    lend_lease_tension = 0.4
    send_volunteers_tension = 0.4
    guarantee_tension = 0.4
    drift_defence_factor = -0.3
    civilian_intel_to_others = 20
    army_intel_to_others = 10
    navy_intel_to_others = 20
    airforce_intel_to_others = 10
}
```

**動的陣営名**:
```
"FACTION_NAME_NONALIGNED_1"
"FACTION_NAME_NONALIGNED_2"
"FACTION_NAME_NONALIGNED_3"
"FACTION_NAME_NONALIGNED_4"
"FACTION_NAME_NONALIGNED_5"
```

**サブイデオロギー**:
1. `oligarchism` (寡頭制)
2. `moderatism` (穏健主義)
3. `centrism` (専制未来主義)
4. `boarderisum` (長国境主義) ※ `can_be_randomly_selected = no`

**ローカライズキー**:
- `neutrality_ideology`: "中道派"
- `neutrality_ideology_desc`: "中道派政府"

---

### 5. 市民主義 (civilism)

**色**: RGB(192, 249, 36) - 薄緑色

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.7
- `faction_impact_on_world_tension`: なし

**外交ルール**:
```hoi4
rules = {
    can_create_collaboration_government = no
    can_declare_war_on_same_ideology = no
    can_force_government = yes
    can_send_volunteers = no
    can_puppet = no
    can_lower_tension = yes
    can_only_justify_war_on_threat_country = yes
    can_guarantee_other_ideologies = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: yes
- `can_collaborate`: yes

**主要Modifiers**:
```hoi4
modifiers = {
    # サブイデオロギーに基づく平均効果
    # urban_civicism: +10% 産業, +5% 研究, -5% 戦争支持
    # peasantism: +5% 兵力, +5% 徴兵, -10% 産業, +5% 安定度
    # comp_civilism: +5% 政治力, +10% 研究, +5% 意見獲得
    industrial_capacity_factory = 0.02
    research_speed_factor = 0.08
    war_support_factor = -0.02
    conscription_factor = 0.02
    stability_factor = 0.02
    political_power_factor = 0.02
    opinion_gain_monthly_factor = 0.02

    # オリジナルModifiers
    generate_wargoal_tension = 0.7
    join_faction_tension = 0.8
    lend_lease_tension = 0.8
    send_volunteers_tension = 0.8
    guarantee_tension = 0.8
    annex_cost_factor = 0.8
    civilian_intel_to_others = 0.85
    army_intel_to_others = 0.7
    navy_intel_to_others = 0.7
    airforce_intel_to_others = 0.7
    justify_war_goal_when_in_major_war_time = 0.4
    drift_defence_factor = 0.8
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0.8  # +80% 貿易意見
}
```

**サブイデオロギー**:
1. `urban_civicism` (都市市民主義)
2. `peasantism` (農民主義)
3. `comp_civilism` (山民主義)

**ローカライズキー**:
- `civilism`: "市民主義"
- `civilism_desc`: "国家の主役は都市に住む者か、あるいは土地を耕す者か。市民の生活様式そのものが、国の形を定義する。"

---

### 6. 保守的民主主義 (conservative_democracy)

**色**: RGB(143, 225, 136) - 薄緑色

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.45
- `faction_impact_on_world_tension`: なし

**外交ルール**:
```hoi4
rules = {
    can_create_collaboration_government = yes
    can_force_government = yes
    can_send_volunteers = yes
    can_puppet = yes
    can_only_justify_war_on_threat_country = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: yes
- `can_collaborate`: yes

**主要Modifiers**:
```hoi4
modifiers = {
    # Conservatism: +5% 政治力, +10% 安定度, -5% 戦争支持
    political_power_factor = 0.05
    stability_factor = 0.10
    war_support_factor = -0.05
    industrial_capacity_factory = 0.05

    generate_wargoal_tension = 0.35
    join_faction_tension = 0.1
    lend_lease_tension = 0.25
    send_volunteers_tension = 0.5
    guarantee_tension = 0.25
    annex_cost_factor = 0.1
    civilian_intel_to_others = 0.35
    army_intel_to_others = 0.35
    navy_intel_to_others = 0.25
    airforce_intel_to_others = 0.35
    justify_war_goal_when_in_major_war_time = 0.4
    drift_defence_factor = 0.7
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0.75  # +75% 貿易意見
}
```

**サブイデオロギー**:
1. `Conservatism` (保守主義)

**ローカライズキー**:
- `conservative_democracy`: "保守的民主主義"
- `conservative_democracy_desc`: "古き良き伝統と秩序を守りつつ、民主的な手続きも尊重する。急進的な変化を嫌い、安定こそが最も価値あるものだと考える。"

---

### 7. 立憲君主政体 (constitutional_monarchy)

**色**: RGB(50, 111, 128) - 濃い青緑色

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.5
- `faction_impact_on_world_tension`: なし

**外交ルール**:
```hoi4
rules = {
    can_create_collaboration_government = yes
    can_send_volunteers = yes
    can_puppet = yes
    can_only_justify_war_on_threat_country = yes
    can_force_government = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: yes
- `can_collaborate`: yes

**主要Modifiers**:
```hoi4
modifiers = {
    # constitutional_royal_government: +10% 政治力, +5% 安定度, -5% 戦争支持
    # constitutional_emperor: +10% 政治力, +10% 意見獲得, +5% 安定度, -10% 戦争支持
    political_power_factor = 0.10
    stability_factor = 0.05
    opinion_gain_monthly_factor = 0.05
    war_support_factor = -0.075

    join_faction_tension = 0.45
    lend_lease_tension = 0.25
    send_volunteers_tension = 0.5
    guarantee_tension = 0.25
    annex_cost_factor = -0.2
    civilian_intel_to_others = 0.5
    army_intel_to_others = 0.4
    navy_intel_to_others = 0.4
    airforce_intel_to_others = 0.4
    justify_war_goal_when_in_major_war_time = 0.55
    drift_defence_factor = 0.55
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0.8  # +80% 貿易意見
}
```

**サブイデオロギー**:
1. `constitutional_royal_government` (立憲王政) ※ `can_be_randomly_selected = no`
2. `constitutional_emperor` (立憲帝政)

**ローカライズキー**:
- `constitutional_monarchy`: "立憲君主政体"
- `constitutional_monarchy_desc`: "君主は国民の象徴として君臨するが、政治の実権は議会が握る。王室のスキャンダルが、時折国を揺るがすスパイスとなる。"

---

### 8. 直接民主制 (direct_democracy)

**色**: RGB(0, 135, 157) - シアン

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.65
- `faction_impact_on_world_tension`: なし

**外交ルール**:
```hoi4
rules = {
    can_only_justify_war_on_threat_country = yes
    can_force_government = no
    can_send_volunteers = no
    can_puppet = no
}
```

**特殊能力**:
- `can_host_government_in_exile`: yes
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    # our_own_gov: +10% 政治力, +5% 戦争支持, -5% 産業
    political_power_factor = 0.10
    war_support_factor = 0.05
    industrial_capacity_factory = -0.05
    stability_factor = 0.03

    generate_wargoal_tension = 0.85
    join_faction_tension = 0.5
    lend_lease_tension = 0.1
    send_volunteers_tension = 1
    guarantee_tension = 0.5
    annex_cost_factor = -0.4
    civilian_intel_to_others = 0.3
    army_intel_to_others = 0.5
    navy_intel_to_others = 0.5
    airforce_intel_to_others = 0.45
    justify_war_goal_when_in_major_war_time = 0.8
    drift_defence_factor = 0.75
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0.45  # +45% 貿易意見
}
```

**サブイデオロギー**:
1. `our_own_gov` (直接民主制)

**ローカライズキー**:
- `direct_democracy`: "直接民主制"
- `direct_democracy_desc`: "国民が直接投票であらゆる物事を決定する、究極の参加型政治。今日の昼食のメニューから宣戦布告まで、全ては国民投票にかけられる。"

---

### 9. 未来主義 (futurism)

**色**: RGB(62, 186, 255) - 薄い青色

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: なし
- `faction_impact_on_world_tension`: なし

**外交ルール**:
```hoi4
rules = {
    can_create_collaboration_government = yes
    can_declare_war_on_same_ideology = yes
    can_force_government = yes
    can_send_volunteers = yes
    can_puppet = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: yes
- `can_collaborate`: yes

**主要Modifiers**:
```hoi4
modifiers = {
    # despotism: +15% 研究, +5% 政治力, -10% 戦争支持
    # paradise: +5% 研究, +10% 安定度, -5% 戦争支持
    research_speed_factor = 0.15
    stability_factor = 0.08
    political_power_factor = 0.05
    war_support_factor = -0.10
    industrial_capacity_factory = 0.08

    generate_wargoal_tension = 0.1
    join_faction_tension = 0.1
    lend_lease_tension = 0.1
    send_volunteers_tension = 0.1
    guarantee_tension = 0.1
    annex_cost_factor = 0.1
    justify_war_goal_when_in_major_war_time = 0.1
    drift_defence_factor = 0.1
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0  # 貿易意見なし
}
```

**サブイデオロギー**:
1. `despotism` (専制主義)
2. `paradise` (楽園指向主義) ※ `can_be_randomly_selected = no`

**ローカライズキー**:
- `futurism`: "未来主義"
- `futurism_desc`: "過去を破壊し、機械と速度の時代を祄賛する。芸術家や思想家が国を率い、戦争すらも美しい芸術として捉える。"

---

### 10. 知識主義 (intellectualism)

**色**: RGB(62, 116, 79) - 濃い緑色

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.1
- `faction_impact_on_world_tension`: 0.1

**外交ルール**:
```hoi4
rules = {
    can_create_collaboration_government = yes
    can_force_government = yes
    can_send_volunteers = yes
    can_puppet = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    # knowledge_intensiveism: +20% 研究, -10% 戦争支持
    # knowledge_decentralization: +10% 研究, +5% 政治力, -5% 戦争支持
    # knowledge_enlightenment: +15% 研究, +5% 意見獲得, -10% 戦争支持
    research_speed_factor = 0.15
    war_support_factor = -0.08
    political_power_factor = 0.02
    opinion_gain_monthly_factor = 0.02

    generate_wargoal_tension = 0.1
    join_faction_tension = 0.1
    lend_lease_tension = 0.1
    send_volunteers_tension = 0.1
    guarantee_tension = 0.1
    annex_cost_factor = 0.1
    civilian_intel_to_others = 0.1
    army_intel_to_others = 0.1
    navy_intel_to_others = 0.1
    airforce_intel_to_others = 0.1
    justify_war_goal_when_in_major_war_time = 0.1
    drift_defence_factor = 0.1
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0.1  # +10% 貿易意見
}
```

**サブイデオロギー**:
1. `knowledge_intensiveism` (知識集約主義)
2. `knowledge_decentralization` (知識分散主義)
3. `knowledge_enlightenment` (知識啓蒙主義)

**ローカライズキー**:
- `intellectualism`: "知識主義"
- `intellectualism_desc`: "国家の最も重要な資源は知識である。図書館は要塞であり、科学者は兵士であり、ノーベル賞は戦略兵器に等しい。"

---

### 11. 神話主義 (mythologicalism)

**色**: RGB(223, 210, 141) - 黄褐色

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: なし
- `faction_impact_on_world_tension`: なし

**外交ルール**:
```hoi4
rules = {
    can_create_collaboration_government = yes
    can_declare_war_on_same_ideology = yes
    can_force_government = yes
    can_send_volunteers = yes
    can_puppet = yes
    can_only_justify_war_on_threat_country = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: yes
- `can_collaborate`: yes

**主要Modifiers**:
```hoi4
modifiers = {
    # 宗教的サブイデオロギーに基づく平均効果
    # 多くの宗教が研究ボーナス（ギリシャ哲学、イスラム黄金時代など）
    # 一部は安定度ボーナス（仏教、神道、儒教）
    # 大部分は平和主義的傾向
    research_speed_factor = 0.08
    stability_factor = 0.05
    opinion_gain_monthly_factor = 0.03
    war_support_factor = -0.05
    political_power_factor = 0.02

    join_faction_tension = 0.2
    lend_lease_tension = 0.1
    send_volunteers_tension = 0.4
    guarantee_tension = 0.4
    annex_cost_factor = 0.2
    justify_war_goal_when_in_major_war_time = 0.2
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0.6  # +60% 貿易意見
}
```

**サブイデオロギー**:
1. `greek_mythology` (ギリシア神話)
2. `shinto` (神道)
3. `islam` (イスラム主義)
4. `egyptian_mythology` (エジプト神話)
5. `cthulhu_mythology` (クトゥルフ神話)
6. `buddhism` (仏教)
7. `animism` (原始宗教)
8. `Christianity` (キリスト教)
9. `heathenism` (邪教) ※ `can_be_randomly_selected = no`
10. `new_religions` (新興宗教)
11. `confucianism` (儒教)
12. `Judaism` (ユダヤ教)
13. `Hinduism` (ヒンドゥー教)
14. `Zoroastrianism` (ゾロアスター教)
15. `manichaeism` (マニ教)
16. `kamuy` (カムイ信仰)
17. `Vodou` (ブードゥー教)

**ローカライズキー**:
- `mythologicalism`: "神話主義"
- `mythologicalism_desc`: "古代の神々や伝説の英雄への信仰が、国家の法と秩序を支配する。神託や占いが、外交政策や軍事行動を決定する。"

---

### 12. 中道右派 (rightneutrality)

**色**: RGB(168, 117, 88) - 茶色

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.3
- `faction_impact_on_world_tension`: 0.4

**外交ルール**:
```hoi4
rules = {
    can_force_government = yes
    can_puppet = yes
    can_send_volunteers = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: yes
- `can_collaborate`: yes

**主要Modifiers**:
```hoi4
modifiers = {
    # shogunate: +10% 安定度, +5% 意見獲得, -5% 戦争支持
    # Empires: +15% 産業, +5% 政治力, -5% 戦争支持
    # Kingdom: +10% 安定度, +5% 政治力, -5% 戦争支持
    stability_factor = 0.10
    industrial_capacity_factory = 0.05
    political_power_factor = 0.05
    opinion_gain_monthly_factor = 0.02
    war_support_factor = -0.05

    generate_wargoal_tension = 0.65
    join_faction_tension = 0.55
    lend_lease_tension = 0.5
    send_volunteers_tension = 0.45
    guarantee_tension = 1
    annex_cost_factor = 0.3
    civilian_intel_to_others = 0.01
    army_intel_to_others = 0.05
    navy_intel_to_others = 0.05
    airforce_intel_to_others = 0.05
    justify_war_goal_when_in_major_war_time = 0.4
    drift_defence_factor = 0.9
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0.2  # +20% 貿易意見
}
```

**サブイデオロギー**:
1. `shogunate` (将軍派) ※ `can_be_randomly_selected = no`
2. `Empires` (帝国派)
3. `Kingdom` (王国派) ※ `can_be_randomly_selected = no`

**ローカライズキー**:
- `rightneutrality`: "中道右派"
- `rightneutrality_desc`: "君主や皇帝といった伝統的権威の下で国家は統治されるべきだと考える。国際社会の騒乱からは距離を置き、国内の秩序維持を最優先する。"

---

### 13. 無政府主義 (anarchism)

**色**: RGB(80, 10, 10) - 濃い赤色

**AI挙動**: `ai_communist`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.75
- `faction_impact_on_world_tension`: 0.5

**外交ルール**:
```hoi4
rules = {
    can_force_government = no
    can_send_volunteers = no
    can_puppet = no
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    # anti_revisionism: +5% 政治力, -10% 安定度, -5% 戦争支持
    # anarchism: +5% 政治力, -10% 安定度, -10% 戦争支持
    # Anarcho_syndicalism: +10% 兵力回復, -10% 安定度, -5% 戦争支持
    political_power_factor = 0.05
    stability_factor = -0.10
    war_support_factor = -0.07
    conscription_factor = 0.03

    civilian_intel_to_others = 0
    army_intel_to_others = 0
    navy_intel_to_others = 0
    airforce_intel_to_others = 0
    hidden_modifier = {
        join_faction_tension = -0.1
    }
}
```

**陣営Modifiers**: なし

**サブイデオロギー**:
1. `anti_revisionism` (反修正主義)
2. `anarchism` (無政府主義)
3. `Anarcho_syndicalism` (アナルコ・サンディカリズム)

**ローカライズキー**:
- `anarchism`: "無政府主義"
- `anarchism_desc`: "政府や権威をすべて否定し、人々が自らの意思で秩序を築く社会を目指す。誰も命令しないので、誰も言うことを聞かない。"

---

### 14. バカ主義 (stupidism)

**色**: RGB(48, 68, 70) - 濃い灰色

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.5
- `faction_impact_on_world_tension`: 0.5

**外交ルール**:
```hoi4
rules = {
    can_create_collaboration_government = yes
    can_force_government = yes
    can_puppet = yes
    can_only_justify_war_on_threat_country = yes
    can_send_volunteers = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: yes
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    # communism_democracy: +5% 政治力, +5% 意見獲得, -5% 戦争支持
    # neoliberalism: +15% 産業, +5% 政治力, -10% 戦争支持
    # eroticism: +10% 政治力, -10% 安定度, -5% 戦争支持
    # anthropocentrism: +5% 兵力回復, -10% 研究, -5% 戦争支持
    # exclusionism: +5% 安定度, -15% 意見獲得, -10% 戦争支持
    industrial_capacity_factory = 0.03
    political_power_factor = 0.06
    war_support_factor = -0.07
    stability_factor = -0.025
    opinion_gain_monthly_factor = -0.025
    conscription_factor = 0.02
    research_speed_factor = -0.03

    generate_wargoal_tension = 0.5
    join_faction_tension = 0.5
    lend_lease_tension = 0.5
    send_volunteers_tension = 0.5
    guarantee_tension = 0.5
    annex_cost_factor = 0.5
    civilian_intel_to_others = 0.5
    army_intel_to_others = 0.5
    navy_intel_to_others = 0.5
    airforce_intel_to_others = 0.5
    justify_war_goal_when_in_major_war_time = 0.5
    drift_defence_factor = 0.5
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0.5  # +50% 貿易意見
}
```

**サブイデオロギー**:
1. `communism_democracy` (共産民主主義)
2. `neoliberalism` (新自由主義)
3. `eroticism` (性愛主義)
4. `anthropocentrism` (人間中心主義)
5. `exclusionism` (排他主義)

**ローカライズキー**:
- `stupidism`: "バカ主義"
- `stupidism_desc`: "支離滅裂で矛盾した思想を意図的に採用することで、敵を混乱させ、味方を当惑させる。予測不可能な行動こそが、最高の戦略だと信じている。"

---

### 15. 技術至上主義 (technicalism)

**色**: RGB(42, 252, 175) - ティール色

**AI挙動**: `ai_neutral`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.2
- `faction_impact_on_world_tension`: 0.2

**外交ルール**:
```hoi4
rules = {
    can_only_justify_war_on_threat_country = yes
    can_send_volunteers = no
    can_puppet = yes
    can_force_government = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    # basictechnicalism: +10% 研究, +5% 産業, -5% 安定度
    # hightechnicalism: +20% 研究, +10% 産業, -10% 安定度
    # lowtechnicalism: +5% 研究, +5% 兵力回復, -5% 産業
    research_speed_factor = 0.18
    industrial_capacity_factory = 0.05
    stability_factor = -0.05
    conscription_factor = 0.03
    political_power_factor = 0.03

    generate_wargoal_tension = 0.1
    join_faction_tension = 0.2
    lend_lease_tension = 0.2
    send_volunteers_tension = 0.1
    guarantee_tension = 0.1
    annex_cost_factor = 0.1
    civilian_intel_to_others = 0.2
    army_intel_to_others = 0.5
    navy_intel_to_others = 0.5
    airforce_intel_to_others = 0.5
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0  # 貿易意見なし
}
```

**サブイデオロギー**:
1. `basictechnicalism` (技術至上主義)
2. `hightechnicalism` (ハイテク技術至上主義) ※ `can_be_randomly_selected = no`
3. `lowtechnicalism` (ローテク技術至上主義)

**ローカライズキー**:
- `technicalism`: "技術至上主義"
- `technicalism_desc`: "国家の進歩は、その技術力によってのみ測られる。政治家はエンジニアに取って代わられ、法律はアルゴリズムによって記述される。"

---

### 16. 博愛主義 (philanthropy)

**色**: RGB(90, 20, 255) - 紫色

**AI挙動**: `ai_democratic`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.25
- `faction_impact_on_world_tension`: 0.1

**外交ルール**:
```hoi4
rules = {
    can_create_collaboration_government = no
    can_declare_war_on_same_ideology = no
    can_force_government = yes
    can_send_volunteers = no
    can_puppet = no
    can_only_justify_war_on_threat_country = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: yes
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    # neutrality_democracy: +10% 政治力, +10% 安定度, -5% 戦争支持
    # philanthropy: +10% 意見獲得, +5% 安定度, -15% 戦争支持
    # passive_pacifism: +10% 安定度, -20% 戦争支持, +5% 政治力
    # non_resistance: +10% 安定度, -25% 戦争支持, +5% 意見獲得
    # absolute_pacifism: +15% 安定度, -30% 戦争支持, +5% 意見獲得
    stability_factor = 0.12
    war_support_factor = -0.19
    political_power_factor = 0.05
    opinion_gain_monthly_factor = 0.05

    generate_wargoal_tension = 1
    join_faction_tension = 0.8
    lend_lease_tension = 0.5
    send_volunteers_tension = 0.5
    guarantee_tension = 0.25
    annex_cost_factor = 0.5
    civilian_intel_to_others = 20
    army_intel_to_others = 5
    navy_intel_to_others = 20
    airforce_intel_to_others = 5
}
```

**陣営Modifiers**:
```hoi4
faction_modifiers = {
    faction_trade_opinion_factor = 0.5  # +50% 貿易意見
}
```

**サブイデオロギー**:
1. `neutrality_democracy` (中立的民主主義)
2. `philanthropy` (博愛主義)
3. `passive_pacifism` (受動的平和主義)
4. `non_resistance` (非抵抗主義)
5. `absolute_pacifism` (絶対的平和主義)

**ローカライズキー**:
- `philanthropy`: "博愛主義"
- `philanthropy_desc`: "博愛を国家理念とし、暴力よりも対話と助け合いによって世界を良くしようとする。"

---

### 17. 変革主義 (transformationism)

**色**: RGB(230, 230, 230) - 薄い灰色

**AI挙動**: `ai_communist`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.75
- `faction_impact_on_world_tension`: 0.5

**外交ルール**:
```hoi4
rules = {
    can_force_government = no
    can_send_volunteers = yes
    can_puppet = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: yes

**主要Modifiers**:
```hoi4
modifiers = {
    # accelerationism: +20% 研究, -10% 安定度, +5% 政治力
    # artisticism: +10% 意見獲得, +5% 政治力, -5% 戦争支持
    research_speed_factor = 0.10
    stability_factor = -0.05
    political_power_factor = 0.05
    opinion_gain_monthly_factor = 0.05
    war_support_factor = -0.025

    puppet_cost_factor = -0.3
    civilian_intel_to_others = 10
    army_intel_to_others = 7.5
    navy_intel_to_others = 12.5
    airforce_intel_to_others = 7.5
    hidden_modifier = {
        join_faction_tension = -0.1
    }
}
```

**陣営Modifiers**: なし

**サブイデオロギー**:
1. `accelerationism` (加速主義)
2. `artisticism` (芸術主義)

**ローカライズキー**:
- `transformationism`: "変革主義"
- `transformationism_desc`: "既存の価値観や制度を絶えず塗り替え、新しい姿に変化し続けることこそ進歩だと信じる。"

---

### 18. 破滅主義 (ruinism)

**色**: RGB(255, 255, 255) - 白色

**AI挙動**: `ai_communist`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0
- `faction_impact_on_world_tension`: 0

**外交ルール**:
```hoi4
rules = {
    can_force_government = no
    can_send_volunteers = no
    can_puppet = no
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: yes

**主要Modifiers**:
```hoi4
modifiers = {
    # eradicationism: +15% 戦争支持, -10% 安定度, -5% 研究
    # destructiveism: +20% 戦争支持, -15% 安定度, -10% 政治力
    # primitivism: +5% 兵力回復, -10% 産業, -10% 研究
    war_support_factor = 0.13
    stability_factor = -0.12
    research_speed_factor = -0.08
    political_power_factor = -0.03
    conscription_factor = 0.02
    industrial_capacity_factory = -0.03

    puppet_cost_factor = 0
    civilian_intel_to_others = 0
    army_intel_to_others = 0
    navy_intel_to_others = 0
    airforce_intel_to_others = 0
}
```

**陣営Modifiers**: なし

**サブイデオロギー**:
1. `eradicationism` (根絶主義)
2. `destructiveism` (破壊主義)
3. `primitivism` (原始主義)

**ローカライズキー**:
- `ruinism`: "破滅主義"
- `ruinism_desc`: "文明は人類を堕落させた元凶であり、全てを破壊し原始の姿に戻ることこそが救済だと信じる。世界の終焉を積極的に推し進める。"

---

### 19. 縦長主義 (longitudinalism)

**色**: RGB(80, 110, 110) - 濃い灰色緑

**AI挙動**: `ai_communist`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0
- `faction_impact_on_world_tension`: 0

**外交ルール**:
```hoi4
rules = {
    can_force_government = yes
    can_send_volunteers = yes
    can_puppet = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    civilian_intel_to_others = 0
    army_intel_to_others = 0
    navy_intel_to_others = 0
    airforce_intel_to_others = 0
    hidden_modifier = {
        join_faction_tension = -0.1
    }
}
```

**陣営Modifiers**: なし

**サブイデオロギー**:
1. `Anarcho_longitudinalism` (無政府縦長主義)
2. `anti_horizontalism` (反横長主義)

**ローカライズキー**:
- `longitudinalism`: "縦長主義"
- `longitudinalism_desc`: "縦に長いものをこよなく愛し、国土も文化も上へ上へと伸ばすことに喜びを見いだす。"

---

### 20. 横長主義 (horizontalism)

**色**: RGB(180, 110, 10) - オレンジ茶色

**AI挙動**: `ai_communist`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 1
- `faction_impact_on_world_tension`: 1

**外交ルール**:
```hoi4
rules = {
    can_force_government = yes
    can_send_volunteers = yes
    can_puppet = yes
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    civilian_intel_to_others = 0
    army_intel_to_others = 50
    navy_intel_to_others = 50
    airforce_intel_to_others = 50
    hidden_modifier = {
        join_faction_tension = -0.1
    }
}
```

**陣営Modifiers**: なし

**サブイデオロギー**:
1. `Anarcho_horizontalism` (横長無政府主義)
2. `anti_longitudinalism` (反縦長主義)

**ローカライズキー**:
- `horizontalism`: "横長主義"
- `horizontalism_desc`: "横に広がる美しさを尊び、平たく長い形状こそ国家の理想だと主張する。"

---

### 21. ひんぬー主義 (hinnulism)

**色**: RGB(10, 80, 10) - 濃い緑色

**AI挙動**: `ai_communist`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.75
- `faction_impact_on_world_tension`: 0.5

**外交ルール**:
```hoi4
rules = {
    can_force_government = no
    can_send_volunteers = no
    can_puppet = no
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    # アニメテーマイデオロギー
    # 文化的洗練と内なる強さに焦点
    stability_factor = 0.12
    research_speed_factor = 0.08
    war_support_factor = -0.08
    opinion_gain_monthly_factor = 0.05
    political_power_factor = 0.03

    civilian_intel_to_others = 0
    army_intel_to_others = 0
    navy_intel_to_others = 0
    airforce_intel_to_others = 0
    hidden_modifier = {
        join_faction_tension = -0.1
    }
}
```

**陣営Modifiers**: なし

**サブイデオロギー**:
1. `absolutely_hinnuism` (絶対ひんぬー主義)
2. `manaitism` (まな板主義)
3. `lolism` (ろり主義)
4. `syoujyism` (少女主義)
5. `binuism` (微ぬー主義)

**ローカライズキー**:
- `hinnulism`: "ひんぬー主義"
- `hinnulism_desc`: "慎ましさと内に秘めた可能性こそが至高の価値であると考える。華美や誇張を嫌い、質素で洗練された文化を理想とする。"

---

### 22. きょぬー主義 (kyonulism)

**色**: RGB(80, 10, 10) - 濃い赤色

**AI挙動**: `ai_communist`

**世界緊張度への影響**:
- `war_impact_on_world_tension`: 0.75
- `faction_impact_on_world_tension`: 0.5

**外交ルール**:
```hoi4
rules = {
    can_force_government = no
    can_send_volunteers = no
    can_puppet = no
}
```

**特殊能力**:
- `can_host_government_in_exile`: no
- `can_collaborate`: no

**主要Modifiers**:
```hoi4
modifiers = {
    # アニメテーマイデオロギー
    # 保護、育成、圧倒的魅力に焦点
    opinion_gain_monthly_factor = 0.15
    stability_factor = 0.10
    war_support_factor = -0.05
    political_power_factor = 0.08
    conscription_factor = 0.05

    civilian_intel_to_others = 0
    army_intel_to_others = 0
    navy_intel_to_others = 0
    airforce_intel_to_others = 0
    hidden_modifier = {
        join_faction_tension = -0.1
    }
}
```

**陣営Modifiers**: なし

**サブイデオロギー**:
1. `absolutely_kyonuism` (絶対きょぬー主義)
2. `bakunuism` (ばくぬー主義)
3. `marshmallowism` (ましゅまろ主義)
4. `rocketism` (ロケット主義)
5. `loli_kyonuism` (ロリきょぬー主義)
6. `onesanism` (おねーさん主義)

**ローカライズキー**:
- `kyonulism`: "きょぬー主義"
- `kyonulism_desc`: "豊かさと包容力こそが、国家の繁栄と安定の象徴であると考える。寛大さと母性を国家理念とし、全ての国民を優しく包み込む。"

---

## サブイデオロギー詳細一覧

### 民主主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `liberalism` | 自由主義 | 個人の選択が神聖視され、国家は最高のオンラインショッピングモールを目指す。 |
| `socialism` | 社会主義 | 全員の富を平等に分かち合うが、誰かがこっそりパイを独り占めしていないか常にお互いを監視している。 |

### 共産主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `marxism` | マルクス主義 | 資本家を追い出せば理想郷が訪れると信じ、毎日理論書を読みながら革命の夢を見る。 |
| `anarchist_communism` | アナルコ共産主義 | 国家なき社会で生産手段を共同所有し、自由な協調により平等を実現しようとする。 |
| `leninism` | レーニン主義 | 少数のエリート前衛党が大衆を導き、世界革命という壮大なゴールを目指す。 |
| `stalinism` | スターリン主義 | 偉大なる指導者が全てを決定し、逆らう者はシベリアの果てで熊と語り合うことになる。 |

### ファシズム系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `nazism` | ナチズム | 特定の民族の優越性を信じ、世界から多様性を消し去ろうとする過激な思想。 |
| `fascism_ideology` | ファシズム | 国家こそが絶対であり、国民はその栄光のために全てを捧げる運命共同体。力強い指導者の下、世界を自分たちの色に塗り替えることを目指す。 |
| `gen_nazism` | ジェネリック・ナチズム | 特定の民族優越を掲げるものの、詳細な理論は曖昧なままの凡庸な極右思想。 |
| `falangism` | ファランジズム | 神と国家への忠誠を誓い、伝統的な価値観で社会を統一しようとする。 |
| `rexism` | レクシズム | カリスマ的な指導者と宗教的権威を融合させ、国家を一つの家族のようにまとめようとする。 |
| `coastisim` | 海岸主義 | 海岸主義は、国土の大半が海岸であるチリにおける、更に海岸を獲得すべきとする積極的拡大主義の一種である。 |

### 中道派系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `oligarchism` | 寡頭制 | 国の富と権力を握る一握りのエリートたちが、自分たちの利益のために国を運営する。 |
| `moderatism` | 穏健主義 | 何事もほどほどが一番と考え、過激な変化を避けて現状維持を目指す。 |
| `centrism` | 専制未来主義 | 未来の安定のために強権的指導を容認し、極端を避けつつも独裁的手法を好む。 |
| `boarderisum` | 長国境主義 | 長国境主義は、国土が長く面積に比して国境線が長いチリにおける、更に国境線を長くし世界に広く存在を知らしめようとする思想である。 |

### 市民主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `urban_civicism` | 都市市民主義 | 高層ビルとネオンサインこそが文明の証であり、国の発展は都市の発展と同一だと考える。 |
| `peasantism` | 農民主義 | 大地こそが全ての力の源泉であり、農民の汗と土の匂いが国家の魂だと信じる。 |
| `comp_civilism` | 山民主義 | 都市の技術と農村の魂を融合させ、究極のハイブリッド国家を目指す。 |

### 保守的民主主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `Conservatism` | 保守主義 | 変化とはすなわち腐敗の始まりであり、先祖から受け継いだものを守り抜くことが使命である。 |

### 立憲君主政体系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `constitutional_royal_government` | 立憲王政 | 国王は国民の父として敬愛され、その権威が国家の安定を支える。 |
| `constitutional_emperor` | 立憲帝政 | 皇帝の神聖な血統が国家の正当性の源泉であり、その存在が国民を一つにまとめる。 |

### 直接民主制系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `our_own_gov` | 直接民主制 | すべての政策を自分たちの手で決めることを誇りとし、常に投票と討論が繰り返される。 |

### 未来主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `despotism` | 専制主義 | 未来の栄光のためには一人の独裁者にすべてを委ねるべきだとする思想。 |
| `paradise` | 楽園指向主義 | 全ての労働は機械に任せ、人間は芸術と快楽を追求することに専念する理想郷。 |

### 知識主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `knowledge_intensiveism` | 知識集約主義 | 国家の全ての力を研究開発に注ぎ込み、究極のテクノロジーを手に入れようとする。 |
| `knowledge_decentralization` | 知識分散主義 | 知識は独占されるべきでなく、全ての国民がアクセスできることで国家は強くなると信じる。 |
| `knowledge_enlightenment` | 知識啓蒙主義 | 無知こそが悪の根源であり、教育と啓蒙活動によって世界をより良い場所へと導こうとする。 |

### 神話主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `greek_mythology` | ギリシア神話 | オリンポスの神々を敬い、彼らの物語を国家指導の指針とする。 |
| `shinto` | 神道 | 八百万の神への信仰を国の基盤とし、自然と調和する社会を理想とする。 |
| `islam` | イスラム主義 | コーランの教えを政治と日常に貫き、共同体の結束を重んじる。 |
| `egyptian_mythology` | エジプト神話 | ラーやオシリスといった古代神を崇拝し、その秩序を現代に再現しようとする。 |
| `cthulhu_mythology` | クトゥルフ神話 | 古きものへの狂信が国家を支配し、正気を代償に未知なる力を求める。 |
| `buddhism` | 仏教 | 悟りと慈悲を政治に持ち込み、煩悩のない社会を目指す。 |
| `animism` | 原始宗教 | 森羅万象に霊が宿ると信じ、自然崇拝を通じて調和を図る。 |
| `Christianity` | キリスト教 | キリストの教えを基礎に愛と赦しの国を築こうとする。 |
| `heathenism` | 邪教 | 公認宗教を持たず、異端の儀式や信仰が混在する雑多な信心。 |
| `new_religions` | 新興宗教 | 既存宗教に飽き足らず、新たな啓示や教義を創出して社会に広める。 |
| `confucianism` | 儒教 | 儒教の徳目を国家統治の根幹とし、礼と秩序を重んじる。 |
| `Judaism` | ユダヤ教 | 唯一神への信仰と律法の遵守を国家生活の基盤とする。 |
| `Hinduism` | ヒンドゥー教 | 多神教的世界観と輪廻の思想が社会制度を形作る。 |
| `Zoroastrianism` | ゾロアスター教 | 善と悪の二元論に基づき、光明の力で世界を浄化しようとする。 |
| `manichaeism` | マニ教 | 光と闇の永遠の戦いを説き、禁欲によって魂を救おうとする。 |
| `kamuy` | カムイ信仰 | アイヌの神々カムイへの敬意を国家の精神とし、自然との共生を目指す。 |
| `Vodou` | ブードゥー教 | 祖霊と精霊に祈りを捧げ、呪術と信仰が政治に入り混じる。 |

### 中道右派系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `shogunate` | 将軍派 | 将軍の権威の下で武家が統治し、厳格な身分制を維持する。 |
| `Empires` | 帝国派 | 皇帝の支配による統一を重んじ、強大な帝国を理想とする。 |
| `Kingdom` | 王国派 | 王の血統こそ国家の正統性と考え、王国の繁栄を目指す。 |

### 無政府主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `anti_revisionism` | 反修正主義 | 正統派の理論から一歩でも逸れることを許さず、妥協を裏切りとして糾弾する過激派。 |
| `anarchism` | 無政府主義 | 政府や権威をすべて否定し、人々が自らの意思で秩序を築く社会を目指す。誰も命令しないので、誰も言うことを聞かない。 |
| `Anarcho_syndicalism` | アナルコ・サンディカリズム | 労働組合が社会の基盤となり、現場労働者の連帯によって国家なき社会を築こうとする。 |

### バカ主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `communism_democracy` | 共産民主主義 | 共産主義的平等を掲げつつ、民主的選挙で指導部を選ぶ折衷体制。 |
| `neoliberalism` | 新自由主義 | 市場の自由を最優先し、国家の介入を極力排除しようとする。 |
| `eroticism` | 性愛主義 | 快楽と性を解放し、官能を政治の中心に据える過激な思想。 |
| `anthropocentrism` | 人間中心主義 | 人間こそが世界の主であり、自然や他生物は従属すべきと考える。 |
| `exclusionism` | 排他主義 | 外部の影響を徹底的に拒み、純粋な共同体の維持を目指す。 |

### 技術至上主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `basictechnicalism` | 技術至上主義 | あらゆる政策は技術的合理性に従うべきだと信じる。 |
| `hightechnicalism` | ハイテク技術至上主義 | 最先端技術の追求こそ国家の至上命題であるとする。 |
| `lowtechnicalism` | ローテク技術至上主義 | 素朴な技術と手仕事を尊び、過度な機械化を拒む。 |

### 博愛主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `neutrality_democracy` | 中立的民主主義 | いずれの陣営にも与せず、徹底した中立を保ちながら民主的手続きだけは守り続ける政治体制。 |
| `philanthropy` | 博愛主義 | 博愛を国家理念とし、暴力よりも対話と助け合いによって世界を良くしようとする。 |
| `passive_pacifism` | 受動的平和主義 | 自らは決して攻めず、攻撃された時にのみ抵抗するという消極的な平和観を掲げる。 |
| `non_resistance` | 非抵抗主義 | 暴力に対して一切の抵抗を行わず、受け入れることで争いを終わらせようとする徹底した非暴力主義。 |
| `absolute_pacifism` | 絶対的平和主義 | いかなる状況でも戦争を否定し、武力行使を完全に放棄する理想主義的立場。 |

### 変革主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `accelerationism` | 加速主義 | 社会変革は加速こそが鍵だと信じ、技術と混乱で既存秩序を突き破ろうとする。 |
| `artisticism` | 芸術主義 | 芸術的価値を最上位に置き、国家運営さえも壮大なアートプロジェクトとして捉える。 |

### 破滅主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `eradicationism` | 根絶主義 | 敵対する価値や文化を根こそぎ消し去ることで新秩序を築こうとする。 |
| `destructiveism` | 破壊主義 | 破壊そのものに価値を見いだし、創造よりも崩壊を選ぶ。 |
| `primitivism` | 原始主義 | 文明を捨て原始的生活へ回帰することで人間の本質を取り戻そうとする。 |

### 縦長主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `Anarcho_longitudinalism` | 無政府縦長主義 | 縦長こそ至高とする思想と無政府主義が融合し、上下へ伸びる自由な社会を夢見る。 |
| `anti_horizontalism` | 反横長主義 | 横への広がりを忌み嫌い、全てを縦へと再配置しようとする過激な縦長信奉者。 |

### 横長主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `Anarcho_horizontalism` | 横長無政府主義 | 横長への愛と無政府主義を掛け合わせ、自由に広がる平坦な世界を目指す。 |
| `anti_longitudinalism` | 反縦長主義 | 縦へ伸びるものを許さず、全てを平たく押し広げようとする横長至上主義者。 |

### ひんぬー主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `absolutely_hinnuism` | 絶対ひんぬー主義 | あらゆる豊満さを悪とみなし、その根絶を目指す過激派。 |
| `manaitism` | まな板主義 | 完全な平坦さこそが究極の美であり、国家の理想像であると考える。 |
| `lolism` | ろり主義 | 幼さと小柄さを理想とし、未成熟を美徳とする極端な価値観。 |
| `syoujyism` | 少女主義 | 少女の純真さを国家理念に据え、清らかで柔らかな社会を求める。 |
| `binuism` | 微ぬー主義 | ほとんど存在しないほどの慎ましさを称え、控えめな美を追求する。 |

### きょぬー主義系

| サブイデオロギーID | 名前 | 説明 |
|------------------|------|------|
| `absolutely_kyonuism` | 絶対きょぬー主義 | 大きければ大きいほど良いという思想に基づき、国家のあらゆるものを巨大化させようとする。 |
| `bakunuism` | ばくぬー主義 | 豊かさが持つ破壊的なまでの魅力を信奉し、他国をその魅力で圧倒しようとする。 |
| `marshmallowism` | ましゅまろ主義 | 柔らかさと包容力を美徳とし、ふんわりとした豊かさを追い求める。 |
| `rocketism` | ロケット主義 | 天へ向かう推進力を至上とし、すべてを上昇志向に染め上げる。 |
| `loli_kyonuism` | ロリきょぬー主義 | 幼さと豊満さを両立させた究極の矛盾を理想とする。 |
| `onesanism` | おねーさん主義 | 包容力ある年長女性を理想化し、成熟した優しさで社会を導こうとする。 |

---

## イデオロギードリフト (Ideology Drift)

### 概要

イデオロギードリフトは、国家の政策、指導者、アイデア、イベントなどを通じて、特定のイデオロギーの支持率を日々変化させるシステムです。

### ドリフトModifierの基本形式

```hoi4
[ideology_name]_ideology_drift = 0.05
```

**例**:
```hoi4
communism_ideology_drift = 0.05   # 共産主義支持率が日々+0.05%上昇
democratic_ideology_drift = 0.03  # 民主主義支持率が日々+0.03%上昇
fascism_ideology_drift = 0.10     # ファシズム支持率が日々+0.10%上昇
neutrality_ideology_drift = 0.07  # 中道派支持率が日々+0.07%上昇
```

### ドリフトの使用例

#### アイデアでの使用

```hoi4
political_advisor_ideology_drift = {
    cost = 150
    advisor_slot = political_advisor
    allowed = {
        has_government = democracy
    }
    modifiers = {
        communism_ideology_drift = -0.05
        democratic_ideology_drift = 0.02
        fascism_ideology_drift = -0.05
        neutrality_ideology_drift = 0.03
    }
}
```

#### 国家指導者特性での使用

```hoi4
communist_revolutionary = {
    cost = 150
    advisor_slot = political_advisor
    modifiers = {
        communism_ideology_drift = 0.10
        political_power_gain = 0.10
    }
}
```

#### 国家方針での使用

```hoi4
focus_drift_communism = {
    icon = GFX_goal_generic_political_unity
    completion_reward = {
        add_political_power = 150
        country_event = {
            id = communism_event.1
        }
    }
    on_activate = {
        add_ideas = {
            temporary_communist_drift_boost
        }
    }
}

# temporary_communist_drift_boost アイデア定義
temporary_communist_drift_boost = {
    communism_ideology_drift = 0.15
}
```

### ドリフトの計算

**基本計算式**:
```
日々のドリフト量 = Σ(全てのイデオロギードリフトModifier)
```

**注意点**:
1. ドリフトは0-100%の範囲内でクリップされます
2. 負の値はそのイデオロギーの支持率を減少させます
3. 全てのイデオロギーのドリフトの合計が0になるように、自動的に調整されます
4. ドリフトは毎日更新されます

### 独自イデオロギーへのドリフト

BSMmodの独自イデオロギー（civilism, technicalismなど）へのドリフトは、以下の形式で指定します：

```hoi4
civilism_ideology_drift = 0.05
technicalism_ideology_drift = 0.03
philanthropy_ideology_drift = 0.07
```

---

## ローカライズキー一覧

### メインイデオロギー

| イデオロギーID | ローカライズキー | 日本語名 |
|--------------|----------------|---------|
| `democratic_ideology` | `democratic_ideology` | 民主主義 |
| `communism_ideology` | `communism_ideology` | 共産主義 |
| `fascism_ideology` | `fascism_ideology` | ファシズム |
| `neutrality_ideology` | `neutrality_ideology` | 中道派 |
| `civilism` | `civilism` | 市民主義 |
| `conservative_democracy` | `conservative_democracy` | 保守的民主主義 |
| `constitutional_monarchy` | `constitutional_monarchy` | 立憲君主政体 |
| `direct_democracy` | `direct_democracy` | 直接民主制 |
| `futurism` | `futurism` | 未来主義 |
| `intellectualism` | `intellectualism` | 知識主義 |
| `mythologicalism` | `mythologicalism` | 神話主義 |
| `rightneutrality` | `rightneutrality` | 中道右派 |
| `anarchism` | `anarchism` | 無政府主義 |
| `stupidism` | `stupidism` | バカ主義 |
| `technicalism` | `technicalism` | 技術至上主義 |
| `philanthropy` | `philanthropy` | 博愛主義 |
| `transformationism` | `transformationism` | 変革主義 |
| `ruinism` | `ruinism` | 破滅主義 |
| `longitudinalism` | `longitudinalism` | 縦長主義 |
| `horizontalism` | `horizontalism` | 横長主義 |
| `hinnulism` | `hinnulism` | ひんぬー主義 |
| `kyonulism` | `kyonulism` | きょぬー主義 |

### 国名の動的変換

HOI4では、イデオロギーに応じて国名が動的に変化します。ローカライズキーの形式は以下の通りです：

```
[TAG]_[ideology_key]:0 "国家名"
[TAG]_[ideology_key]_DEF:0 "定形的国家名"
[TAG]_[ideology_key]_ADJ:0 "形容詞形"
```

**例**:
```
USA_democratic_ideology:0 "アメリカ合衆国"
USA_democratic_ideology_DEF:0 "アメリカ合衆国"
USA_democratic_ideology_ADJ:0 "アメリカ"

USA_fascism_ideology:0 "アメリカ帝国"
USA_fascism_ideology_DEF:0 "アメリカ帝国"
USA_fascism_ideology_ADJ:0 "アメリカ帝国"

USA_communism_ideology:0 "アメリカ社会主義共和国"
USA_communism_ideology_DEF:0 "アメリカ社会主義共和国"
USA_communism_ideology_ADJ:0 "アメリカ社会主義共和国"
```

### サブイデオロギーの説明キー

サブイデオロギーの説明は、以下の形式でローカライズされます：

```
[sub_ideology_key]_desc:0 "説明テキスト"
```

**例**:
```
liberalism_desc:0 "個人の選択が神聖視され、国家は最高のオンラインショッピングモールを目指す。"
marxism_desc:0 "資本家を追い出せば理想郷が訪れると信じ、毎日理論書を読みながら革命の夢を見る。"
```

---

## 国別使用例

### 日本 (JPN)

**定義ファイル**: `bakasekai/history/countries/JPN - Japan.txt`

**従属国の設定例**:
```hoi4
CTO = {
    set_politics = {
        ruling_party = constitutional_monarchy
        last_election = "1936.1.1"
        election_frequency = 48
        elections_allowed = yes
    }
    set_popularities = {
        democratic_ideology = 30
        constitutional_monarchy = 40
        neutrality_ideology = 30
    }
}
```

**解説**:
- 統治政党: `constitutional_monarchy` (立憲君主政体)
- 最終選挙: 1936年1月1日
- 選挙頻度: 48ヶ月
- 選挙許可: yes
- 人気度: 民主主義30%、立憲君主政体40%、中道派30%

### アメリカ (USA)

**定義ファイル**: `bakasekai/history/countries/USA - USA.txt`

**設定例**:
```hoi4
set_politics = {
    ruling_party = democratic_ideology
    last_election = "1932.11.8"
    election_frequency = 48
    elections_allowed = yes
}

set_popularities = {
    democratic_ideology = 99
    communism_ideology = 1
}
```

**解説**:
- 統治政党: `democratic_ideology` (民主主義)
- 最終選挙: 1932年11月8日
- 選挙頻度: 48ヶ月
- 選挙許可: yes
- 人気度: 民主主義99%、共産主義1%

---

## イデオロギー関連ファイル構成

### 主要ファイル

| ファイルパス | 役割 |
|-------------|------|
| `bakasekai/common/ideologies/00_ideologies.txt` | イデオロギー定義ファイル |
| `bakasekai/localisation/japanese/replace/bakasekai/bakasekai_l_japanese.yml` | 日本語ローカライズ |
| `bakasekai/localisation/english/` | 英語ローカライズファイル群 |
| `bakasekai/history/countries/*.txt` | 国別イデオロギー設定 |
| `bakasekai/common/ideas/*.txt` | イデオロギードリフトを持つアイデア定義 |

### 関連ドキュメント

| ドキュメントパス | 説明 |
|---------------|------|
| `documents/97_ideologies.md` | イデオロギー一覧（簡易版） |
| `documents/README_systems.md` | システム全体の索引 |

---

## 注意事項

### 1. サブイデオロギーのランダム選択

一部のサブイデオロギーは、イベントや国家方針でのみ選択可能で、ランダム選択から除外されています：

| サブイデオロギーID | 理由 |
|------------------|------|
| `coastisim` | チリ固有の特殊イデオロギー |
| `boarderisum` | チリ固有の特殊イデオロギー |
| `paradise` | 未来主義の特殊な実現形態 |
| `constitutional_royal_government` | 特定の状況でのみ出現 |
| `hightechnicalism` | 高度な技術達成後に解放 |
| `Kingdom` | 特定の歴史的文脈でのみ出現 |
| `shogunate` | 日本固有の特殊イデオロギー |
| `heathenism` | 特定の宗教的状況でのみ出現 |

### 2. インテリジェンス共有

イデオロギーによって、陣営内でのインテリジェンス共有率が異なります。一部のイデオロギーはインテリジェンス共有を完全に拒否しています：

**インテリジェンス共有なし**:
- `anarchism` (無政府主義)
- `ruinism` (破滅主義)
- `longitudinalism` (縦長主義)
- `hinnulism` (ひんぬー主義)
- `kyonulism` (きょぬー主義)

### 3. AI挙動の分類

AI挙動は以下の4つのカテゴリに分類されます：

| AI挙動 | イデオロギー |
|---------|------------|
| `ai_democratic` | democratic_ideology, philanthropy |
| `ai_communist` | communism_ideology, anarchism, transformationism, ruinism, longitudinalism, horizontalism, hinnulism, kyonulism |
| `ai_fascist` | fascism_ideology |
| `ai_neutral` | neutrality_ideology, civilism, conservative_democracy, constitutional_monarchy, direct_democracy, futurism, intellectualism, mythologicalism, rightneutrality, stupidism, technicalism |

### 4. 動的陣営名のローカライズ

動的陣営名のローカライズキーは、日本語版では実装されていない可能性があります。必要な場合は、以下の形式でローカライズファイルに追加してください：

```
FACTION_NAME_COMMUNIST_1:0 "共产国际"
FACTION_NAME_COMMUNIST_2:0 "人民联盟"
FACTION_NAME_FASCIST_1:0 "新秩序"
FACTION_NAME_FASCIST_2:0 "轴心国"
FACTION_NAME_NONALIGNED_1:0 "互不侵犯条约"
FACTION_NAME_NONALIGNED_2:0 "防御协定"
```

### 5. イデオロギー変更の制限

一部の外交ルールは、イデオロギーによって以下の制限があります：

| ルール | 説明 |
|-------|------|
| `can_declare_war_on_same_ideology = no` | 同じイデオロギーの国に対して宣戦布告できない |
| `can_only_justify_war_on_threat_country = yes` | 威脛国に対してのみ宣戦の理由を正当化できる |
| `can_create_collaboration_government` | 協力政府を作成できるかどうか |
| `can_host_government_in_exile` | 亡命政府を受け入れられるかどうか |

### 6. 世界緊張度への影響

イデオロギーによって、戦争や陣営形成が世界緊張度に与える影響が大きく異なります：

**高い影響**:
- `fascism_ideology`: 戦争1.0、陣営1.0
- `horizontalism`: 戦争1.0、陣営1.0

**中程度の影響**:
- `communism_ideology`: 戦争0.75、陣営0.5
- `anarchism`: 戦争0.75、陣営0.5
- `transformationism`: 戦争0.75、陣営0.5
- `hinnulism`: 戦争0.75、陣営0.5
- `kyonulism`: 戦争0.75、陣営0.5

**低い影響**:
- `democratic_ideology`: 戦争0.25、陣営0.1
- `neutrality_ideology`: 戦争0.25、陣営0.1
- `philanthropy`: 戦争0.25、陣営0.1

**影響なし**:
- `ruinism`: 戦争0、陣営0
- `longitudinalism`: 戦争0、陣営0
- `futurism`: 戦争なし、陣営なし

---

## 更新履歴

- 2026-04-10: 初版作成

---

## 関連情報

### システム間の連携

イデオロギーシステムは、以下のシステムと連携しています：

1. **ステラリス要素システム**: イデオロギーによって特性や伝統の取得に影響
2. **国家統合力システム**: イデオロギーの安定度が統合力に影響
3. **統一通貨システム**: イデオロギーの安定度と産業力が統一通貨獲得に影響
4. **経済同盟システム**: イデオロギーによって経済同盟への参加に制限がある場合あり

### 参考資料

- `AGENTS.md`: エージェント向けの開発ガイドライン
- `CLAUDE.md`: AI向け全体ガイド
- `.github/copilot-instructions.md`: コーディング規約と構造
- `.github/CONTRIBUTING.md`: 開発/検証フロー
- `documents/onboarding_guide.md`: 新規参加者向け案内
