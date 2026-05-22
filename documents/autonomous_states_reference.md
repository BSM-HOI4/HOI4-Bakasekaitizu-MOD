# BSM Mod — 傀儡国・自律国種別一覧

自由度 `0.00`(完全支配) → `1.00`(完全独立) の順で並べています。  
記号: **✓** = yes / **✗** = no / **—** = 未定義(HOI4デフォルト適用)

---

## 目次

- [📦 バニラ](#バニラ) — HOI4標準の自律度タイプ。DLC不要。 (10件)
- [📦 バニラDLC](#バニラdlc) — Together for Victory / WtT / MtG / NSB / LaR / AaT 等DLC付属タイプ。 (9件)
- [🔧 BSM汎用](#bsm汎用) — BSM mod独自の汎用タイプ（国タグ非依存）。 (53件)
- [🏳️ 国別(BSM)](#国別(bsm)) — GER / JAP / SOV / GBR / CHI / IND / USA / FSA 等専用タイプ。 (27件)
- [🌍 MD系(BSM)](#md系(bsm)) — Modern Dayシナリオ由来の現代的タイプ群。 (54件)
- [⚔️ EU4系(BSM)](#eu4系(bsm)) — EU4の主従属区分をHOI4に移植した5段階システム。 (5件)
- [🏯 日本系(BSM)](#日本系(bsm)) — 幕府体制(4段階)・都道府県制(3段階)・令制国の計8タイプ。 (8件)

---


## 📦 バニラ

> HOI4標準の自律度タイプ。DLC不要。

| 自由度 | ID | 日本語名 | 傀儡 | 兵力共有 | 人力倍率 | CIC移転 | MIC移転 | 貿易移転 | 宣戦不可 | 徴兵拒否可 | スパイ可 | 出兵義務 | 解放条件 |
|-------:|:---|:---------|:----:|:--------:|:--------:|:-------:|:-------:|:--------:|:--------:|:----------:|:--------:|:--------:|:---------|
| 0 | `Territorium` | テリトリウム | ✓ | 1.00 | 1 | 0.75 | 0.75 | 1.00 | ✓ | ✗ | ✗ | ✓ | — |
| 0.1 | `autonomy_psonal_union` | 人的同君連合国 | ✗ | 1.00 | 0.4 | — | — | 0.50 | — | ✓ | — | — | — |
| 0.2 | `autonomy_integrated_puppet` | 統合傀儡国 | ✓ | 1.00 | 1.0 | 0.25 | 0.75 | 1.00 | ✓ | ✗ | ✗ | ✓ | DLC:Together for V |
| 0.2 | `autonomy_reichskommissariat` | 国家弁務官区 | ✓ | 0.90 | 0.9 | 0.25 | 0.65 | 1.00 | ✓ | ✗ | ✗ | ✓ | 宗主:JPN/MAN DLC:Death or Disho |
| 0.4 | `autonomy_puppet` | 傀儡国 | ✓ | 0.90 | 0.9 | — | — | 1.00 | ✓ | ✗ | ✗ | — | — |
| 0.5 | `autonomy_reichsprotectorate` | 国家保護領 | ✓ | 0.70 | 0.7 | 0.25 | — | 0.60 | ✓ | ✗ | ✗ | — | 宗主:JPN/MAN DLC:Death or Disho |
| 0.60 | `autonomy_colony` | 植民地 | ✓ | 0.70 | 0.7 | — | — | 0.50 | ✓ | ✗ | ✗ | — | DLC:Together for V |
| 0.75 | `autonomy_supervised_state` | 監督国 | ✗ | 0.00 | 0.2 | — | — | 0.25 | ✓ | ✗ | ✗ | — | DLC:Man the Guns |
| 0.8 | `autonomy_dominion` | 自治領 | ✗ | 0.00 | 0.2 | — | — | 0.25 | ✓ | ✗ | ✓ | — | DLC:Together for V |
| 0.80 | `autonomy_satellite` | 衛星国 | ✗ | 0.40 | 0.5 | — | — | 0.40 | ✓ | ✗ | ✗ | — | 宗主:JPN/MAN DLC:Death or Disho |

## 📦 バニラDLC

> Together for Victory / WtT / MtG / NSB / LaR / AaT 等DLC付属タイプ。

| 自由度 | ID | 日本語名 | 傀儡 | 兵力共有 | 人力倍率 | CIC移転 | MIC移転 | 貿易移転 | 宣戦不可 | 徴兵拒否可 | スパイ可 | 出兵義務 | 解放条件 |
|-------:|:---|:---------|:----:|:--------:|:--------:|:-------:|:-------:|:--------:|:--------:|:----------:|:--------:|:--------:|:---------|
| 0.0 | `autonomy_aat_defense_council_member` | 防衛評議会構成国 | ✓ | 1.00 | 0 | 0.35 | 0.65 | 1.00 | ✓ | ✗ | ✗ | ✓ | 宗主:SWE DLC:Arms Against T |
| 0.0 | `autonomy_collaboration_government` | 協力政府 | ✓ | 1.00 | 1.0 | 0.75 | 0.75 | 1.00 | ✓ | ✗ | ✗ | ✓ | DLC:La Resistance |
| 0.0 | `autonomy_eu_member` | EU加盟国 | ✓ | 0.50 | 0.5 | — | — | 0.50 | ✓ | ✗ | ✓ | — | 宗主:BEL DLC:Gotterdammerun |
| 0.0 | `autonomy_personal_union` | 人的同君連合国 | ✓ | 0.00 | 1.0 | — | — | 0.50 | ✓ | ✗ | ✗ | ✗ | DLC:No Step Back |
| 0.2 | `autonomy_austro_hungarian_subject` | オーストリア＝ハンガリー臣民国 | ✓ | 0.90 | 0.9 | — | — | 1.00 | ✓ | ✗ | ✗ | — | 宗主:AUS DLC:Gotterdammerun |
| 0.2 | `autonomy_volkskommissariat` | 人民委員区 | ✓ | 0.90 | 0.9 | 0.50 | 0.50 | 1.00 | ✓ | ✗ | ✗ | ✓ | 宗主:DEU DLC:Gotterdammerun |
| 0.2 | `autonomy_wtt_imperial_protectorate` | 帝国保護領 | ✓ | 0.90 | 0.9 | 0.25 | 0.65 | 1.00 | ✓ | ✗ | ✗ | ✓ | 宗主:JPN/MAN DLC:Waking the Tig |
| 0.7 | `autonomy_wtt_imperial_associate` | 帝国提携国 | ✓ | 0.70 | 0.7 | 0.25 | — | 0.60 | ✓ | ✗ | ✓ | — | 宗主:JPN/MAN DLC:Waking the Tig |
| 0.8 | `autonomy_wtt_imperial_subject` | 帝国構成国 | ✗ | 0.50 | 0.5 | 0.10 | 0.25 | 0.25 | ✗ | ✓ | ✗ | ✗ | 宗主:JPN DLC:Waking the Tig |

## 🔧 BSM汎用

> BSM mod独自の汎用タイプ（国タグ非依存）。

| 自由度 | ID | 日本語名 | 傀儡 | 兵力共有 | 人力倍率 | CIC移転 | MIC移転 | 貿易移転 | 宣戦不可 | 徴兵拒否可 | スパイ可 | 出兵義務 | 解放条件 |
|-------:|:---|:---------|:----:|:--------:|:--------:|:-------:|:-------:|:--------:|:--------:|:----------:|:--------:|:--------:|:---------|
| 0.0 | `autonomy_antarctic_territory` | 南極地域 | ✗ | — | 0 | — | — | — | ✓ | ✗ | — | — | 条件あり |
| 0.0 | `autonomy_eu_member` | EU加盟国 | ✓ | 0.50 | 0.5 | — | — | 0.50 | ✓ | ✗ | ✓ | — | (常時不可) |
| 0.0 | `autonomy_italy_governate` | イタリア総督府 | ✗ | 0.70 | 0 | — | — | 1.00 | — | — | — | — | 条件あり |
| 0.0 | `autonomy_military_district` | 軍政区 | ✓ | 1.00 | 0 | — | — | 1.00 | — | — | — | — | 条件あり |
| 0.0 | `autonomy_military_government` | 軍政府 | ✓ | 1.00 | 0 | — | — | 1.00 | — | — | — | — | 制限なし |
| 0.0 | `autonomy_occupied_territory` | 占領地 | ✓ | — | 0 | — | — | 0.60 | — | — | — | — | 条件あり |
| 0.0 | `crown_dependency` | 王冠属領 | ✗ | 0.80 | 1.0 | 0.50 | 0.50 | 0.80 | ✓ | ✗ | — | ✗ | FLAG:monarchy_state_flag |
| 0.0 | `integrated_puppet_government` | 統合傀儡政府 | ✗ | 0.80 | 1.0 | 0.50 | 0.50 | 0.80 | ✓ | ✗ | — | ✗ | 宗主:GER |
| 0.1 | `captaincy_general` | 総督領 | ✗ | 0.80 | 1.0 | 0.45 | 0.45 | 0.80 | ✓ | ✗ | — | ✗ | 宗主:POR |
| 0.1 | `constituent_autonomous_province` | 構成自治州 | ✗ | 0.80 | 1.0 | 0.45 | 0.45 | 0.80 | ✓ | ✗ | — | ✗ | — |
| 0.1 | `mandated_territory_C` | C式委任統治領 | ✗ | 0.80 | 1.0 | 0.45 | 0.45 | 0.80 | ✓ | ✗ | — | ✗ | — |
| 0.1 | `overseas_territory` | 海外領土 | ✗ | 0.80 | 1.0 | 0.45 | 0.45 | 0.80 | ✓ | ✗ | — | ✗ | — |
| 0.1 | `viceroyalty` | 副王領 | ✗ | 0.80 | 1.0 | 0.45 | 0.45 | 0.80 | ✓ | ✗ | — | ✗ | FLAG:monarchy_state_flag |
| 0.2 | `autonomy_austro_hungarian_subject` | オーストリア＝ハンガリー臣民国 | ✓ | 0.90 | 0.9 | — | — | 1.00 | ✓ | ✗ | ✗ | — | (常時不可) |
| 0.2 | `autonomy_reichsprotektorat` | 国家保護領 | ✓ | 0.60 | 0 | 0.30 | — | 0.80 | — | — | — | — | 条件あり |
| 0.2 | `autonomy_volkskommissariat` | 人民委員区 | ✓ | 0.90 | 0.9 | 0.50 | 0.50 | 1.00 | ✓ | ✗ | ✗ | ✓ | (常時不可) |
| 0.25 | `autonomy_ibrgovernate` | イベリア総督府 | ✓ | 0.90 | 0 | — | — | 1.00 | — | — | — | — | 条件あり |
| 0.25 | `autonomy_liberated_government` | 解放政府 | ✗ | 0.90 | 0 | — | — | 1.00 | — | — | — | — | 条件あり |
| 0.3 | `colonies_federation` | 植民地連邦 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | FLAG:federal_dependent_territory_flag |
| 0.3 | `colony` | 植民地 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | FLAG:unitary_dependent_territory_flag |
| 0.3 | `colony_and_protected_territory` | 植民地及び保護領 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | FLAG:protected_dependent_territory_flag |
| 0.3 | `condominium` | 共同統治領 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | — |
| 0.3 | `constituent_state` | 構成国 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | — |
| 0.3 | `mandated_territory_B` | B式委任統治領 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | — |
| 0.3 | `occupied_puppet_government` | 占領傀儡政府 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | 宗主:GER |
| 0.3 | `personal_union_colony` | 同君連合植民地 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | FLAG:monarchy_state_flag |
| 0.3 | `personal_union_protected_territory` | 同君連合保護領 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | FLAG:monarchy_state_flag |
| 0.3 | `protected_territory` | 保護領 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | — |
| 0.3 | `real_union` | 物的同君連合国 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | FLAG:monarchy_state_flag |
| 0.4 | `autonomy_integrated_reichskommissariat` | 国家弁務官統合区 | ✓ | — | 0 | — | — | 0.60 | — | — | — | — | 条件あり |
| 0.40 | `autonomy_italy_antiimperialist` | 反帝国主義提携国 | ✗ | 0.00 | 0 | 0.00 | — | 0.00 | — | — | — | — | 条件あり |
| 0.40 | `autonomy_italy_hefty_influence` | 強影響下自治国 | ✗ | 0.20 | 0 | — | — | 0.80 | — | — | — | — | 制限なし |
| 0.40 | `autonomy_italy_reliant` | 依存国 | ✗ | 0.10 | 0 | — | — | -0.80 | — | — | — | — | 制限なし |
| 0.5 | `autonomy_sea_integrated_warlord_subject` | 東南アジア統合軍閥臣民 | ✓ | 0.90 | 0.9 | — | — | 1.00 | ✓ | ✗ | ✗ | — | (常時不可) |
| 0.5 | `leased_territory` | 租借地 | ✗ | 0.60 | 1.0 | 0.25 | 0.25 | 0.60 | ✓ | ✗ | — | ✗ | — |
| 0.6 | `autonomous_puppet_state` | 自治的傀儡国 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | 宗主:GER |
| 0.6 | `autonomous_state` | 自治国 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | 宗主:ENG |
| 0.6 | `autonomy_autonomous_reichskommissariat` | 国家弁務官自治区 | ✓ | — | 0 | — | — | 0.60 | — | — | — | — | 条件あり |
| 0.6 | `autonomy_sea_warlord_subject` | 東南アジア軍閥臣民 | ✓ | 0.50 | 0.9 | — | — | 0.50 | ✓ | ✗ | ✗ | — | (常時不可) |
| 0.6 | `mandated_territory_A` | A式委任統治領 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | — |
| 0.6 | `personal_union` | 人的同君連合国 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | FLAG:monarchy_state_flag |
| 0.6 | `protected_state` | 保護国 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | — |
| 0.6 | `tributary_state` | 朝貢国 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | — |
| 0.6 | `trust_territory` | 信託統治領 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | — |
| 0.6 | `vassal_state` | 附庸国 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | — |
| 0.75 | `autonomy_client_state` | 依存国 | ✗ | 0.00 | 0 | — | — | 0.25 | — | — | — | — | 制限なし |
| 0.8 | `associated_state` | 提携国 | ✗ | 0.10 | 0.0 | 0.10 | 0.10 | 0.10 | ✗ | ✓ | — | ✗ | — |
| 0.80 | `autonomy_italy_associate` | イタリア提携国 | ✗ | 0.00 | 0 | — | — | -0.10 | — | — | — | — | 制限なし |
| 0.80 | `autonomy_transnistria_governate` | トランスニストリア統治区 | ✗ | 0.00 | 0 | — | — | 0.00 | — | — | — | — | 条件あり |
| 0.80 | `autonomy_ulster_breakaway_state` | アルスター分離国 | ✗ | 0.00 | 0 | — | — | 0.00 | — | — | — | — | 条件あり |
| 0.8 | `joint_special_economic_zone` | 共同経済特区 | ✗ | 0.60 | 1.0 | — | — | 0.60 | ✓ | ✗ | — | ✗ | — |
| 0.8 | `nominal_puppet_state` | 名目的傀儡国 | ✗ | 0.10 | 0.0 | 0.10 | 0.10 | 0.10 | ✗ | ✓ | — | ✗ | 宗主:GER |
| 0.9 | `release_leased_territory` | 租借地返還 | ✗ | — | 0.0 | — | — | — | — | — | — | — | — |

## 🏳️ 国別(BSM)

> GER / JAP / SOV / GBR / CHI / IND / USA / FSA 等専用タイプ。

| 自由度 | ID | 日本語名 | 傀儡 | 兵力共有 | 人力倍率 | CIC移転 | MIC移転 | 貿易移転 | 宣戦不可 | 徴兵拒否可 | スパイ可 | 出兵義務 | 解放条件 |
|-------:|:---|:---------|:----:|:--------:|:--------:|:-------:|:-------:|:--------:|:--------:|:----------:|:--------:|:--------:|:---------|
| 0.0 | `USA_territory` | 準州 | ✗ | 0.90 | 1.0 | 0.50 | 0.50 | 0.90 | ✓ | ✗ | — | ✗ | 宗主:ALF |
| 0.0 | `autonomy_SSR` | ソビエト社会主義共和国 | ✓ | 0.90 | 0.9 | 0.25 | 0.50 | 1.00 | ✓ | ✗ | ✗ | ✓ | 宗主:SOV DLC:Together for V |
| 0.0 | `reichsland` | 国家直轄地 | ✗ | 0.90 | 1.0 | 0.50 | 0.50 | 0.90 | ✓ | ✗ | — | ✗ | 宗主:GER |
| 0.1 | `CHI_autonomous_province` | 中華自治省 | ✗ | 0.80 | 1.0 | 0.45 | 0.45 | 0.80 | ✓ | ✗ | — | ✗ | 宗主:CHI |
| 0.1 | `SOV_constituent_autonomous_republic` | 構成自治共和国 | ✗ | 0.80 | 1.0 | 0.45 | 0.45 | 0.80 | ✓ | ✗ | — | ✗ | 宗主:SOV |
| 0.1 | `imperial_overseas_territory` | 外地 | ✗ | 0.80 | 1.0 | 0.45 | 0.45 | 0.80 | ✓ | ✗ | — | ✗ | 宗主:JAP |
| 0.1 | `reichsgeneralgovernorate` | 国家総督領 | ✗ | 0.80 | 1.0 | 0.45 | 0.45 | 0.80 | ✓ | ✗ | — | ✗ | 宗主:GER |
| 0.1 | `reichsprotectorate` | 国家保護領 | ✗ | 0.80 | 1.0 | 0.45 | 0.45 | 0.80 | ✓ | ✗ | — | ✗ | 宗主:GER |
| 0.25 | `FSA_government_general` | 総督府 | ✓ | — | 0.9 | — | — | — | — | — | — | — | 宗主条件あり |
| 0.3 | `CHI_autonomous_military_clique` | 中華自治軍閥 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | 宗主:CHI |
| 0.3 | `IND_princely_state` | インド藩王国 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | 宗主:IND |
| 0.3 | `SOV_constituent_federative_republic` | 構成連邦共和国 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | 宗主:SOV |
| 0.3 | `SOV_constituent_republic` | 構成共和国 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | 宗主:SOV |
| 0.3 | `commonwealth_administered_territory` | 連邦管理地域 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | 宗主:ENG |
| 0.3 | `imperial_constituent_state` | 帝国構成国 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | 宗主:JAP |
| 0.3 | `reichskolonie` | 国家植民地 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | 宗主:GER |
| 0.3 | `reichskommissariat` | 国家弁務官区 | ✗ | 0.70 | 1.0 | 0.35 | 0.35 | 0.70 | ✓ | ✗ | — | ✗ | 宗主:GER |
| 0.6 | `SOV_satellite_state` | 衛星国 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | 宗主:SOV |
| 0.6 | `USA_commonwealth` | 米国自治連邦区 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | 宗主:ALF |
| 0.6 | `autonomy_Soviet_Supervised_State` | ソビエト監督国 | ✓ | 0.70 | 0.7 | 0.25 | — | 0.60 | ✓ | ✗ | ✗ | — | 宗主:SOV DLC:Together for V |
| 0.6 | `dominion` | 自治領 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | 宗主:ENG |
| 0.6 | `imperial_associated_state` | 帝国提携国 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | 宗主:JAP |
| 0.6 | `reichssatellitestate` | 衛星国 | ✗ | 0.20 | 0.0 | 0.20 | 0.20 | 0.20 | ✗ | ✓ | — | ✗ | 宗主:GER |
| 0.75 | `autonomy_Soviet_Sattelite_State` | ソビエト衛星国 | ✓ | 0.50 | 0.5 | 0.10 | 0.20 | 0.25 | ✗ | ✓ | ✗ | ✗ | 宗主:SOV DLC:Together for V |
| 0.80 | `autonomy_china_warlord_regime` | 中国軍閥政権 | ✗ | — | 0 | — | — | — | — | — | — | — | 条件あり |
| 0.8 | `commonwealth_realm` | 連邦王国 | ✗ | 0.10 | 0.0 | 0.10 | 0.10 | 0.10 | ✗ | ✓ | — | ✗ | 宗主:ENG |
| 0.8 | `imperial_protected_state` | 帝国保護国 | ✗ | 0.10 | 0.0 | 0.10 | 0.10 | 0.10 | ✗ | ✓ | — | ✗ | 宗主:JAP |

## 🌍 MD系(BSM)

> Modern Dayシナリオ由来の現代的タイプ群。

| 自由度 | ID | 日本語名 | 傀儡 | 兵力共有 | 人力倍率 | CIC移転 | MIC移転 | 貿易移転 | 宣戦不可 | 徴兵拒否可 | スパイ可 | 出兵義務 | 解放条件 |
|-------:|:---|:---------|:----:|:--------:|:--------:|:-------:|:-------:|:--------:|:--------:|:----------:|:--------:|:--------:|:---------|
| 0.0 | `autonomy_armenia_state` | アルメニア国 | ✗ | 0.10 | 0.1 | 0.00 | 0.15 | 0.20 | ✓ | ✗ | — | ✓ | 宗主:ARM |
| 0.0 | `autonomy_authority_of_palestine` | パレスチナ自治区 | ✗ | 0.10 | 0.1 | 0.75 | 0.00 | 0.80 | ✗ | ✓ | — | ✗ | 宗主:ISR |
| 0.0 | `autonomy_authority_of_palestine_1` | パレスチナ自治区（過渡期） | ✗ | 0.05 | 0.1 | 0.45 | 0.00 | 0.50 | ✗ | ✓ | — | ✗ | 宗主:ISR |
| 0.0 | `autonomy_authority_of_palestine_2` | パレスチナ自治区（拡大） | ✗ | 0.03 | 0.1 | 0.25 | 0.00 | 0.30 | ✗ | ✓ | — | ✗ | 宗主:ISR |
| 0.0 | `autonomy_autonomous_province` | セルビア自治区 | ✗ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:SER |
| 0.0 | `autonomy_autonomous_province1` | 連邦構成主体 | ✗ | 1.00 | 0.1 | 0.00 | 0.00 | 0.20 | ✓ | ✗ | — | ✓ | 宗主:SER |
| 0.0 | `autonomy_autonomous_state` | 自治区 | ✓ | 0.10 | 0.1 | 0.75 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | FLAG:formed_neo_baathist_uar |
| 0.0 | `autonomy_autonomous_state_colored` | 自治区 | ✓ | 0.10 | 0.1 | 0.75 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | FLAG:formed_neo_baathist_uar |
| 0.0 | `autonomy_balkan_federation` | バルカン連邦構成主体 | ✗ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:SER |
| 0.0 | `autonomy_cuban_confederation` | アンティル連合構成主体 | ✗ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:CUB |
| 0.0 | `autonomy_governorate_rf` | 行政区 | ✗ | 0.40 | 0.1 | 0.45 | 0.75 | 0.70 | ✓ | ✗ | — | ✓ | 宗主:SOV |
| 0.0 | `autonomy_korean_federation` | 高麗連邦国 | ✗ | 0.10 | 0.0 | 0.25 | 0.25 | 0.80 | ✗ | ✗ | — | ✗ | 宗主:NKO |
| 0.0 | `autonomy_kray_rf` | 地方 | ✗ | 0.20 | 0.1 | 0.25 | 0.55 | 0.50 | ✓ | ✗ | — | ✓ | 宗主:SOV |
| 0.0 | `autonomy_marz_arm` | 事実上のマーズ | ✗ | 0.30 | 0.1 | 0.35 | 0.65 | 0.60 | ✓ | ✗ | — | ✓ | 宗主:ARM |
| 0.0 | `autonomy_oblast_rf` | 州 | ✗ | 0.30 | 0.1 | 0.35 | 0.65 | 0.60 | ✓ | ✗ | — | ✓ | 宗主:SOV |
| 0.0 | `autonomy_okrug_rf` | 自治管区 | ✗ | 0.40 | 0.1 | 0.45 | 0.75 | 0.70 | ✓ | ✗ | — | ✓ | 宗主:SOV |
| 0.0 | `autonomy_pmc_wagner` | 民間軍事会社ワグネル | ✓ | 1.00 | 0.1 | 1.00 | 1.00 | 0.70 | ✓ | ✗ | — | ✗ | 宗主:SOV |
| 0.0 | `autonomy_provisional_security_of_gaza` | ガザ暫定安全保障区 | ✗ | 0.10 | 0.1 | 0.75 | 0.00 | 0.80 | ✗ | ✓ | — | ✗ | 宗主:PAL |
| 0.0 | `autonomy_republic_khm` | 連邦構成主体 | ✗ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:KHM |
| 0.0 | `autonomy_republic_rf` | 国民共和国 | ✗ | 0.10 | 0.1 | 0.00 | 0.45 | 0.40 | ✓ | ✗ | — | ✓ | 宗主:SOV |
| 0.0 | `autonomy_republic_ukr` | 連邦構成主体 | ✗ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:UKR |
| 0.0 | `autonomy_special_administrative_region_ETK` | 特別行政区 | ✓ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:CHI |
| 0.0 | `autonomy_special_administrative_region_HKG` | 特別行政区 | ✓ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:CHI |
| 0.0 | `autonomy_special_administrative_region_MAC` | 特別行政区 | ✓ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:CHI |
| 0.0 | `autonomy_special_administrative_region_MON` | 特別行政区 | ✓ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:CHI |
| 0.0 | `autonomy_special_administrative_region_TAI` | 特別行政区 | ✓ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:CHI |
| 0.0 | `autonomy_special_administrative_region_TIB` | 特別行政区 | ✓ | 0.10 | 0.1 | 0.00 | 0.75 | 0.80 | ✓ | ✗ | — | ✓ | 宗主:CHI |
| 0.0 | `autonomy_state_cis` | CIS連合加盟国 | ✗ | 0.10 | 0.1 | 0.00 | 0.15 | 0.20 | ✓ | ✗ | — | ✓ | 宗主:SOV |
| 0.0 | `autonomy_state_rf` | 連邦国 | ✗ | 0.10 | 0.1 | 0.00 | 0.15 | 0.20 | ✓ | ✗ | — | ✓ | 宗主:SOV |
| 0.0 | `autonomy_terrorist_mintaqah` | ミンタカ | ✓ | 1.00 | 1.0 | 0.75 | 0.75 | — | ✓ | ✗ | — | ✓ | 宗主条件あり |
| 0 | `autonomy_uar_regional_command` | 地域司令部 | ✓ | 1.00 | 0.7 | 0.75 | 0.75 | 0.75 | ✓ | ✓ | ✗ | ✗ | FLAG:formed_baathist_uar |
| 0.0 | `autonomy_warsaw` | ワルシャワ条約機構加盟国 | ✗ | 0.00 | 1.0 | — | — | 0.00 | ✓ | ✗ | — | — | 宗主:SOV |
| 0.20 | `autonomy_federal_state_iran` | イラン連邦国 | ✗ | 1.00 | 0.3 | 1.00 | 1.00 | 0.70 | ✓ | ✓ | ✗ | ✗ | 宗主条件あり |
| 0.20 | `autonomy_irn_province` | イラン連合構成国 | ✗ | 1.00 | 0.3 | 0.50 | 0.50 | 0.40 | ✓ | ✓ | ✗ | ✗ | FLAG:iranic_confederation_member |
| 0.20 | `autonomy_islamic_republic` | イスラム共和国 | ✗ | 1.00 | 0.3 | 0.50 | 0.50 | 0.40 | ✓ | ✓ | ✗ | ✗ | FLAG:PER_decentralized_nation |
| 0.20 | `autonomy_socialist_union` | 社会主義連合 | ✗ | 1.00 | 0.3 | 0.50 | 0.50 | 0.40 | ✓ | ✓ | ✗ | ✗ | 宗主条件あり |
| 0.20 | `autonomy_uar_province` | 州 | ✓ | 1.00 | 0.3 | 0.25 | 0.25 | 0.40 | ✓ | ✓ | ✗ | ✗ | FLAG:formed_baathist_uar |
| 0.25 | `autonomy_puppet_state` | 傀儡国 | ✓ | 0.40 | 0.4 | 0.50 | 0.50 | 0.60 | ✓ | ✗ | — | ✗ | FLAG:formed_neo_baathist_uar |
| 0.25 | `autonomy_puppet_state_colored` | 傀儡国 | ✓ | 0.40 | 0.4 | 0.50 | 0.50 | 0.60 | ✓ | ✗ | — | ✗ | FLAG:formed_neo_baathist_uar |
| 0.30 | `autonomy_terrorist_wilayah` | ウィラーヤ | ✓ | 1.00 | 1.0 | 0.50 | 0.50 | — | ✓ | ✗ | — | ✓ | 宗主条件あり |
| 0.50 | `autonomy_satellite_state` | 衛星国 | ✗ | 0.70 | 0.5 | 0.25 | 0.25 | 0.40 | ✓ | ✓ | — | ✗ | FLAG:formed_neo_baathist_uar |
| 0.50 | `autonomy_satellite_state_colored` | 衛星国 | ✗ | 0.70 | 0.5 | 0.25 | 0.25 | 0.40 | ✓ | ✓ | — | ✗ | FLAG:formed_neo_baathist_uar |
| 0.60 | `autonomy_terrorist_branch` | 支部 | ✓ | 1.00 | 1.0 | 0.25 | 0.25 | — | ✗ | ✓ | — | ✗ | 宗主条件あり |
| 0.60 | `autonomy_uar_state` | 邦 | ✗ | 1.00 | 0 | 0.00 | 0.00 | 0.20 | ✗ | ✓ | ✓ | ✗ | FLAG:formed_baathist_uar |
| 0.75 | `autonomy_associated_state` | 自由連合 | ✗ | 1.00 | 1.0 | 0.00 | 0.00 | 0.20 | ✗ | ✓ | — | ✗ | FLAG:formed_neo_baathist_uar |
| 0.75 | `autonomy_associated_state_colored` | 自由連合 | ✗ | 1.00 | 1.0 | 0.00 | 0.00 | 0.20 | ✗ | ✓ | — | ✗ | FLAG:formed_neo_baathist_uar |
| 0.85 | `HOL_personal_union` | オランダ同君連合国 | ✓ | 1.00 | 0.3 | — | — | 1.00 | ✗ | ✗ | — | ✗ | FLAG:HOL_personal_union_agreed |
| 0.85 | `TAJ_autonomy_administrative_region` | タジク自治行政区 | ✗ | 0.10 | 0.3 | 0.25 | 0.40 | 0.25 | ✓ | ✓ | — | — | 宗主:TAJ |
| 0.85 | `TUR_eyalet_province` | エヤレト | ✗ | 0.10 | 0.3 | 0.85 | 0.40 | 0.25 | ✓ | ✓ | — | — | 宗主:TUR |
| 0.85 | `autonomy_fifty_first_state_iraq` | 米国第51州（イラク） | ✗ | 0.10 | 0.3 | 0.25 | 0.40 | 0.25 | ✓ | ✓ | — | — | 宗主:USA |
| 0.85 | `autonomy_fifty_second_state_afghanistan` | 米国第52州（アフガニスタン） | ✗ | 0.10 | 0.3 | 0.00 | 0.40 | 0.25 | ✓ | ✓ | — | — | 宗主:USA |
| 0.85 | `autonomy_occupation_zone_IRQ` | 占領地域 | ✗ | 0.10 | 0.3 | 1.00 | 1.00 | 0.25 | ✓ | ✗ | — | — | 宗主:POL |
| 0.85 | `autonomy_union_state` | 連合国家 | ✗ | 0.00 | 0.3 | 0.00 | 0.00 | 0.00 | ✗ | ✓ | — | ✗ | 宗主:SOV |
| 0.85 | `danish_crown_holding` | デンマーク王室保有 | ✗ | 0.00 | 0.3 | 0.00 | 0.00 | 0.00 | ✗ | ✓ | — | ✗ | 宗主:DEN |

## ⚔️ EU4系(BSM)

> EU4の主従属区分をHOI4に移植した5段階システム。

| 自由度 | ID | 日本語名 | 傀儡 | 兵力共有 | 人力倍率 | CIC移転 | MIC移転 | 貿易移転 | 宣戦不可 | 徴兵拒否可 | スパイ可 | 出兵義務 | 解放条件 |
|-------:|:---|:---------|:----:|:--------:|:--------:|:-------:|:-------:|:--------:|:--------:|:----------:|:--------:|:--------:|:---------|
| 0.40 | `bsm_eu4_vassal` | 封臣国 | ✓ | 0.80 | 0.8 | 0.20 | 0.30 | 0.60 | ✓ | ✗ | ✗ | — | — |
| 0.50 | `bsm_eu4_march` | 辺境国 | ✓ | 1.00 | 1.0 | 0.00 | 0.10 | 0.20 | ✓ | ✗ | ✗ | — | — |
| 0.65 | `bsm_eu4_protectorate` | 保護国（EU4式） | ✗ | 0.40 | 0.4 | 0.10 | 0.00 | 0.30 | ✓ | ✓ | ✓ | — | — |
| 0.80 | `bsm_eu4_real_union` | 同君連合国（EU4式） | ✗ | 0.20 | 0.2 | 0.00 | 0.00 | 0.20 | ✓ | ✗ | ✓ | — | — |
| 0.85 | `bsm_eu4_tributary` | 朝貢国（EU4式） | ✗ | 0.10 | 0.1 | 0.05 | — | 0.25 | ✗ | ✓ | ✓ | — | — |

## 🏯 日本系(BSM)

> 幕府体制(4段階)・都道府県制(3段階)・令制国の計8タイプ。

| 自由度 | ID | 日本語名 | 傀儡 | 兵力共有 | 人力倍率 | CIC移転 | MIC移転 | 貿易移転 | 宣戦不可 | 徴兵拒否可 | スパイ可 | 出兵義務 | 解放条件 |
|-------:|:---|:---------|:----:|:--------:|:--------:|:-------:|:-------:|:--------:|:--------:|:----------:|:--------:|:--------:|:---------|
| 0.02 | `bsm_jpn_tokubetsu_ku` | 特別区 | ✓ | 1.00 | 1.0 | 0.70 | 0.70 | 1.00 | ✓ | ✗ | ✗ | ✓ | FLAG:bsm_jpn_modern_flag |
| 0.04 | `bsm_jpn_tokubetsu_shi` | 特別自治市 | ✓ | 1.00 | 1.0 | 0.60 | 0.60 | 0.95 | ✓ | ✗ | ✗ | ✓ | FLAG:bsm_jpn_modern_flag |
| 0.08 | `bsm_jpn_prefecture` | 都道府県 | ✓ | 1.00 | 1.0 | 0.50 | 0.50 | 0.90 | ✓ | ✗ | ✗ | ✓ | FLAG:bsm_jpn_modern_flag |
| 0.10 | `bsm_jpn_tenryo` | 天領 | ✓ | 1.00 | 1.0 | 0.40 | 0.40 | 0.80 | ✓ | ✗ | ✗ | ✓ | FLAG:bsm_jpn_bakufu_flag |
| 0.25 | `bsm_jpn_ryoseikoku` | 令制国 | ✓ | 0.80 | 0.8 | 0.30 | 0.30 | 0.60 | ✓ | ✗ | ✗ | ✓ | FLAG:bsm_jpn_bakufu_flag |
| 0.30 | `bsm_jpn_fudai` | 譜代大名 | ✓ | 0.90 | 0.9 | 0.25 | 0.30 | 0.50 | ✓ | ✗ | ✓ | ✗ | FLAG:bsm_jpn_bakufu_flag |
| 0.50 | `bsm_jpn_han` | 藩 | ✓ | 0.60 | 0.6 | 0.15 | 0.15 | 0.35 | ✓ | ✗ | ✗ | ✗ | FLAG:bsm_jpn_bakufu_flag |
| 0.70 | `bsm_jpn_tozama` | 外様大名 | ✓ | 0.30 | 0.3 | 0.05 | 0.05 | 0.15 | ✓ | ✓ | ✗ | ✗ | FLAG:bsm_jpn_bakufu_flag |

---

*総計 166 種別 / 自動生成*

