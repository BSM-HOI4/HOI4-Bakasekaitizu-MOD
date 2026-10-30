# フランス（イベリア併合・共同君主）シナリオ案

タグは `FRA`。1936年1月1日開始。`common/national_focus/france.txt` は事実上の空ファイルで、方針樹はゼロから設計する。既存の領有・キャラクター・MIO・PAL との関係はそのまま使う。この文書は実装仕様ではなく案である。

## 地図

フランスは大陸欧州とイベリアの両方を持つ。所有州は合計51で、内訳はフランス本土、イベリア全域、サヴォワ（州735）、ドーバー（州835）、モナコ（州927）、コモロ（州708）、サンピエール（州730）である。

イベリア側はマドリード（州41）をはじめカタルーニャ（165）、ガリシア（171）、ナバラ（172）、グラナダ（173）、レオン（174）、シウダー・レアル（175）、ブルゴス（176）、バレアレス（177）、カナリア（178）、エストレマドゥーラ（170）、サラマンカ（788）、コルドバ（789）、アストゥリアス（790）、バリャドリド（791）、バスク（792）、グアダラハラ（793）、東アラゴン（794）、フランス領バスク（806）、カタルーニャ（165）、アラゴン西部（166）、バレンシア（167）、ムルシア（168）、セビリア（169）がすべて `FRA` 所有である。これらの州には `FRA` コアと `ESP` コアが共存しており、バレアレス・カナリアだけが `FRA` コア単独である。亡命スペイン（ESP）にとっての「失われた地図」は、こちらにとっては「持っているが火種の多い地図」である。

州の下には自治の名が残っている。カタルーニャに `CAT`、ガリシアに `GLC`、ナバラ・バスク・仏領バスクに `NAV`、セビリア・グラナダ・コルドバに `ADU`、アンドラ（925）に `ADR`、オクシタニア系の南部各州とサヴォワに `OCC`、コルシカに `COR`、ブルターニュに `BRI`、アルザス（州28）に `RAL`、モナコに `MCO`、コモロに `MAD` のコアが付く。ドーバーには `GBR` と `FRA` の二重コアがあり、イギリス海峡の向こう側に自国領の橋頭堡を持つ格好である。

`PAL`（パリ）はポルトガル本土を治める。首都はリスボン（州112、海軍基地8、タングステン50、`PAL`・`ESP` 二重コア）、ほかポルト（180）、グアルダ（181）、ベジャ（179）、サンタレン（795）、マデイラ（697）。そしてイル＝ド＝フランス（州16）には `FRA` と `PAL` の両方のコアがある。「パリ」という名の国家がポルトガルを治め、その故地はフランスの首都州、という二重構造がこの世界線の前提である。

## 開幕

正式名称は「フランス」、化粧タグは `FRA_republic`（フランス共和国）。`political_set_M` により `constitutional_monarchy` が与党で、選挙周期は12か月、人気は憲政君主64・共産20・中道12・民主3・ファシズム1である。開幕指導者は `FRA_napoleon_VI`（サブイデオロギー `constitutional_emperor`）。通貨トークンは `nc_FRA` が `synchronized_dynamic_tokens` に未登録のため、表示の要否は実装時に決める。

登録済みキャラクターは60近くあり、政治の顔としてはラヴァル（`liberalism`）、ダラディエ（`socialism`）、ナポレオン六世（`constitutional_emperor`）、ギョーマ（`centrism`）、トレーズ（`stalinism`）、ニコ（`marxism`）が country_leader 枠にいる。軍人・顧問はペタン、ド・ゴール、ガムラン、ウェイガン、ダルラン、ビュイヤマン、ブリュム、モーラス、ビュカール、デュクロらが既に recruit 済みである。追加の人物は原則作らない。

軍事は DLC で `FRA_1936` / `FRA_1936_nsb` に切り替わるOOB、Man the Guns 時の海軍OOB、BBA 時の航空OOBがあり、陸・空・海とも欧州級の開幕技術を持つ。輸送船300、コマンドパワー+20。

## 政治

政治列は「ナポレオン家の憲政をどう終わらせるか、あるいは続けるか」を軸に、五方向へ深く分ける。各列は末端まで5〜9段である。

**帝政の継続。** ナポレオン六世の憲政君主を維持し、12か月周期の選挙を戴冠の儀式に変えていく列。ボナパルティズムの国民投票を重ね、最終的に「西方の皇帝」へ進む。`constitutional_monarchy` のまま動かす。

**共和国への揺り戻し。** ダラディエ（社会）かブリュムで共和を復帰させる列。化粧タグ `FRA_republic` は既に共和国名を示しており、名の回収は早い。`democratic_ideology`。

**王党・国家主義。** モーラスの系譜とビュカール、ペタンの摂政で「国家の再統合」を唱える列。イベリアの自治コアを抑える方向に効果を寄せる。`fascism_ideology`。

**共産。** トレーズ（スターリン系）とニコ（マルクス系）の二系統を残したまま、人民戦線→人民委員会へ進む列。イベリア側の地下組織（ESP 側の `ESP_iberian_uprising` と同じ火種）を味方に回す説明が要る。`communism_ideology`。

**中道・技術官僚。** ギョーマ（`centrism`）の列で、政党を休ませて計画官僚に統治を渡す。短めの列にし、どの政治ルートの末端とも接続しない独立枝とする。`neutrality_ideology` 系に寄せるか既存 centrism のまま扱うかは実装時に決める。

## 固有メカニクス：二つの王冠（王冠の配分）

「机」や「証」の代わりに、フランスでは**王冠の座**を数える。国変数 `FRA_crown_seat`（-100〜+100）を「玉座の重心」として扱い、負側はパリ宮廷（ナポレオン家）、正側はリスボン宮廷（PAL＝パリ議会が預かる側）を意味する。方針と決定で振り、閾値で次を開く。

- 座がパリ側に振り切ると、イル＝ド＝フランスの PAL コアを「棚上げ」または「請求整理」する道が開き、PAL は同君連合の下座になる。
- 座がリスボン側に振り切ると、二重戴冠が進み、PAL を吸収した西イベリア王冠の成立案が出る。
- 中央に留めたままだと、現状の「保護する王冠と預かる王冠」が維持され、保障関係だけが強くなる。

変数は `FRA_crown_seat` 一つに留め、PAL 側には `PAL_crown_consent` を併置する案。PAL が国家として存在しない場合の分岐保険は実装時に書く。

## PALとの関係

現状の確定事実は、州16の `FRA`・`PAL` 二重コアと、`FRA` が `PAL` に `give_guarantee` している点だけである。そこから「共同君主／二重王冠」の説明を組む。

PAL の指導者は `PALIS`（表示「パリ議会」、`philanthropy` 与党、サブイデオロギー `non_resistance`、選挙なし）で、国王ではなく議会が王冠を預かっている格好である。案として、パリ議会は「パリの冠を失った宮廷」であり、リスボンに座しながらイル＝ド＝フランスのコアを権利書として持ち続ける、という読みを置く。FRA 側の保障は、議会が持つ権利書を皇帝が認めた証と説明できる。

列の末端は三つに分ける。

1. **王冠統合。** パリ議会の同意を得て PAL を併合し、ポルトガル本土を直接統治する。座がリスボン側に十分振れた場合のみ。
2. **二重戴冠。** 併合せず、PAL を同君連合の相手に据える。`autonomy_psonal_union` 系か既存の同君系自治を使うかは辞書照合。
3. **王冠分離。** PAL がパリのコアを権利書として手放す交換に、FRA の保障を相互防衛に格上げし、ポルトガル側の工業方針を共有する。州16の PAL コア除去はこの選択式効果に限定し、開幕は変えない。

## 産業

**イベリア鉱山。** アストゥリアスの石炭、バスクの鋼、リオ・ティント系の鉱山を FRA の民需・軍需へ組み込む列。史実の鉱山名は使うが、会社名は無名枠に留める。

**ピレネー鉄道。** フランス側とイベリア側の規格差を題材に、「軌間を揃える」建設列にする。インフラと州間接続の説明に使う。

**マドリード工廠。** 州41の既存工場を FRA 側の生産計画へ編入する。`CAT`・`NAV`・`ADU` のコア州では建設効果を落とし、コアの残る州は統治列と連動させる。

**リスボン船渠。** PAL 列と共有する合弁枠。PAL 側の海軍基地8を FRA の大西洋艦隊の修理拠点として使う説明。

**植民地と外地。** コモロ・サンピエールは小さいので、輸送船と海軍経験の小枝に留める。

## 軍事

**陸軍。** ガムラン系の既存師団運用と、ド・ゴール系の装甲集中を排他分岐にする。ピレネー線とアルプス線を別枠の要塞列にし、マジノ延長と分ける。

**海軍。** ダルランを旗頭に、大西洋（ブレスト＋ドーバー＋リスボン寄港）と地中海の二艦隊構想に分ける。ドーバー州を持つ以上、海峡支配は海軍列の看板にする。

**航空。** ビュイヤマンの既存航空OOBを前提に、戦略爆撃と防空の二択を置く。

**外地軍。** イベリア側の鎮守部隊をテンプレとして用意し、自治列の抵抗抑制と連動させる。

## 企業

`common/ideas` の designer として置く。MIO とは別枠で、数値方向のみ固定。

| ID | 種別 | 史実の核 | 解禁 | 効果の方向 |
| --- | --- | --- | --- | --- |
| `FRA_renault_concern` | materiel_manufacturer | ルノー | 開幕から | 装甲・車両研究 |
| `FRA_hotchkiss_concern` | materiel_manufacturer | オチキス | 開幕から | 機関銃・軽装甲 |
| `FRA_schneider_exports` | materiel_manufacturer | シュナイダー | 開幕から | 砲・輸出方向 |
| `FRA_banque_deux_couronnes` | industrial_concern | パリとリスボンを繋ぐ宮廷銀行（架空名） | PAL列 | PP・通商 |
| `FRA_compagnie_iberienne` | industrial_concern | イベリア鉄道・鉱山の仏系資本 | ピレネー鉄道 | インフラ・建設 |
| `FRA_asturias_coal_concern` | industrial_concern | アストゥリアス炭田 | イベリア鉱山 | 資源産出 |
| `FRA_basque_steel_concern` | industrial_concern | ビルバオ製鉄 | イベリア鉱山 | 鋼・軍需 |
| `FRA_lisbon_dock_concern` | naval_manufacturer | リスボン海軍基地の合弁 | PAL 二重戴冠列 | 艦艇改修 |
| `FRA_channel_ferries` | naval_manufacturer | ドーバー海峡の定期航路 | ドーバー列 | 輸送・上陸支援 |
| `FRA_grandes_ecoles` | industrial_concern | 高等専門学校系の官学 | 中道技術官僚列 | 研究速度 |

開幕から見せるのはルノー・オチキス・シュナイダーの三社、残りは方針報酬。

## 設計局

既存 MIO（`FRA_organization.txt`）はルノー・オチキス・APX（戦車系）、FCM・AEB・ACL・ACF（艦艇系）、モラーヌ・ブロック・アミオ・ルヴァスール・SNCAC（航空系）、パナール・ソミュア・MAS・シュナイダー（装備系）で、すべて残す。追加案はイベリア絡みに限る。

**アストゥリアス兵器** `FRA_asturias_arms_organization`

- 装備は歩兵火器・砲。
- 初期特性「二つの言葉の刻印」：生産コスト微減、信頼性微減。
- 解禁はイベリア鉱山列。

**リスボン合同船渠** `FRA_lisbon_yard_organization`

- 装備は軽艦艇と輸送船。
- 初期特性「もう一つの王冠の港」：航続微増。
- 解禁は PAL 二重戴冠か王冠統合。

**ピレネー兵站廠** `FRA_pyrenees_depot_organization`

- 装備は支援・輜重系。
- 初期特性「軌間の違う荷車」：補給方向に微増。

## 国民精神

カテゴリは `country`。数値は実装時に調整し、方向だけ固定する。

**二つの王冠** `FRA_two_crowns`（開幕から）

- 安定微増、PAL への保障を説明する文面。王冠の配分の説明を兼ねる。

**イベリアの重荷** `FRA_iberian_burden`（開幕から）

- 駐留と抵抗の説明。占領・抵抗関連の微ペナルティ方向。自治列か直轄列で軽減する。

**ドーバーの崖** `FRA_dover_cliff`（開幕から）

- 対英関係の火種。海軍経験微増、GBR との外交に影を落とす説明。

**ナポレオン法典の西** `FRA_code_west`（帝政列）

- イベリア側の抵抗減少、統治効果方向。

**王冠の配分** `FRA_crown_scales`（PAL列）

- `FRA_crown_seat` の現在値に応じた方向の微補正。動的にするか段階ideaにするかは実装時調整。

**共和国の復活** `FRA_republic_returned`（共和列）

- 民主受諾・安定方向。

**人民の皇帝** `FRA_peoples_emperor`（共産列の皮肉な末端）

- 共産化後に王冠の名を残す選択をした場合の精神。選ばない場合は作らない。

## このMODの国家idea

**文明度。** 開幕から高めに据え、イベリア統治列では現地側の文化を「併合か寛容か」で係数を分ける。強制同化（直轄）は文明度を微減、自治寛容は微増方向。

**国家統合力。** 二重王冠の構造上、統合力は PAL 側との共有として説明し、王冠統合時に一度だけ大きく足す。分離を選んだ場合は足さない。

**統一通貨。** `nc_FRA` トークンが未定義なので、実装時に `_bsm_nc_tokens` へ登録するか、登録済みの共通通貨系に乗せるかを決める。フラン建ての説明にする案。

**宗教。** 新設せず、既存のカトリック系を使う。イベリア側は同じ宗教法でよい。

**自治体系。** `autonomy_ibrgovernate`（イベリア総督府）は既に定義済みだが、その `allowed` は `is_iberian_nation`（`original_tag = SPR/POR/SPA/CAT`）を要求しており、`FRA` 自身にも `ESP` にも掛からない。総督府を FRA の属領形態として使うなら、解放タグ（`CAT`/`GLC`/`NAV`/`ADU`/`SPA` 系）に自治を付ける設計か、`is_iberian_nation` の拡張が要る。どちらにするかは実装時に別枠で決め、ここでは現行定義を書き換えない。

## 外交

- `PAL`：専用列を参照。保障・二重コア・王冠の配分の三点で動かす。
- `ESP`：イベリア全コアを持つ亡命政府。監視・封じ込め・カリブへの遠征（承認列の終盤）の三段に分ける。ESP の復帰列と表裏の関係にする。
- `GBR`：ドーバー問題。海峡の共同管理か、ドーバーを返して対独協調を取るかの分岐。
- `GER`：アルザスの `RAL` コアとライン地帯。対独強硬か宥和か。
- `ITA`：サヴォワと `OCC` コアの問題。タグ名は実装時に確認。
- `PRT`：ギアナ領とアゾレスの小国。PAL を統合した場合の残存ポルトガル問題として軽く触れる。

## 方針樹

接頭辞は `FRA_`。幹を中央、政治の五列を左、イベリア統治・産業を右上、軍事を右下、PAL・外交を下部に置く。合計96本の長ルート設計。効果の方向のみ固定。

### 幹（6本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_two_capitals` | — | — | 起点。パリとリスボンの説明、`FRA_two_crowns` 確認 |
| `FRA_crown_parliament` | `FRA_two_capitals` | — | 憲政議会。`FRA_crown_seat` 変数起動 |
| `FRA_iberian_patrimony` | `FRA_crown_parliament` | — | イベリア領有の確認。`FRA_iberian_burden` |
| `FRA_imperial_review` | `FRA_iberian_patrimony` | — | 観兵。陸海空経験 |
| `FRA_empire_question` | `FRA_imperial_review` | — | 政治五列の分岐開放 |
| `FRA_crown_scales_focus` | `FRA_empire_question` | — | 王冠の配分の説明。PAL列開放 |

### 帝政継続列（9本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_bonaparte_charter` | `FRA_empire_question` | `FRA_republican_opposition`, `FRA_maurras_circle`, `FRA_thorez_party` | ボナパルト憲章。帝政継続 |
| `FRA_napoleon_court` | `FRA_bonaparte_charter` | — | 宮廷整理。PP |
| `FRA_plebiscite_1937` | `FRA_napoleon_court` | — | 国民投票イベント |
| `FRA_imperial_decrees` | `FRA_plebiscite_1937` | — | 勅令統治。安定 |
| `FRA_order_of_crown` | `FRA_imperial_decrees` | — | 王冠勲章。将官方向 |
| `FRA_court_parties` | `FRA_order_of_crown` | — | 宮廷党派の調停 |
| `FRA_second_empire_style` | `FRA_court_parties` | — | 第二帝政風。消費財・安定 |
| `FRA_emperor_two_seas` | `FRA_second_empire_style` | — | 二つの海の皇帝。海軍方向 |
| `FRA_bonapartist_supreme` | `FRA_emperor_two_seas` | — | 帝政確定。正統・統合力方向 |

### 共和列（7本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_republican_opposition` | `FRA_empire_question` | 帝政列 | 共和野党。democratic |
| `FRA_daladier_path` | `FRA_republican_opposition` | `FRA_blum_coalition` | ダラディエ政権 |
| `FRA_blum_coalition` | `FRA_republican_opposition` | `FRA_daladier_path` | ブリュム連立 |
| `FRA_third_republic_return` | どちらか | — | 第三共和制復帰 |
| `FRA_social_republic` | `FRA_third_republic_return` | — | 社会改革。消費財・安定 |
| `FRA_auriol_presidency` | `FRA_social_republic` | — | オリオル大統領 |
| `FRA_republic_confirmed` | `FRA_auriol_presidency` | — | 共和確定。正統方向 |

### 王党・国家主義列（7本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_action_francaise` | `FRA_empire_question` | 帝政列・共和列・共産列 | アクション・フランセーズ系 |
| `FRA_maurras_circle` | `FRA_action_francaise` | — | モーラスの系譜 |
| `FRA_bucard_shirts` | `FRA_maurras_circle` | — | ビュカールの民兵 |
| `FRA_petain_regency` | `FRA_bucard_shirts` | — | ペタン摂政 |
| `FRA_national_integral` | `FRA_petain_regency` | — | 国民統合。イベリア自治抑圧方向 |
| `FRA_coup_de_paris` | `FRA_national_integral` | — | パリのクーデタ事件 |
| `FRA_french_state_new` | `FRA_coup_de_paris` | — | 新国家体制。fascism 確定 |

### 共産列（7本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_cgt_underground` | `FRA_empire_question` | 帝政列・王党列・共和列 | CGT系地下組織。communism |
| `FRA_thorez_party` | `FRA_cgt_underground` | `FRA_nicod_marxists` | トレーズ系 |
| `FRA_nicod_marxists` | `FRA_cgt_underground` | `FRA_thorez_party` | ニコ系 |
| `FRA_popular_front` | どちらか | — | 人民戦線 |
| `FRA_peoples_commissariats` | `FRA_popular_front` | — | 人民委員会 |
| `FRA_red_iberia_link` | `FRA_peoples_commissariats` | — | イベリア地下組織との連携 |
| `FRA_paris_commune_new` | `FRA_red_iberia_link` | — | 新コミューン。確定 |

### 中道技術官僚列（5本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_guillaumat_technocrats` | `FRA_empire_question` | 四列いずれかの確定後 | ギョーマの技術官僚 |
| `FRA_merit_council` | `FRA_guillaumat_technocrats` | — | 能力評議会 |
| `FRA_planification` | `FRA_merit_council` | — | 計画局。工業方向 |
| `FRA_apolitical_state` | `FRA_planification` | — | 非政治国家 |
| `FRA_experts_charter` | `FRA_apolitical_state` | — | 専門家憲章。確定 |

### イベリア統治列（10本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_iberian_administration` | `FRA_iberian_patrimony` | — | イベリア行政庁 |
| `FRA_madrid_palace` | `FRA_iberian_administration` | — | マドリード行宮 |
| `FRA_direct_departements` | `FRA_madrid_palace` | `FRA_autonomy_charter` | 直轄県化。抵抗抑圧方向 |
| `FRA_autonomy_charter` | `FRA_madrid_palace` | `FRA_direct_departements` | 自治憲章。寛容方向 |
| `FRA_iberian_governate` | `FRA_autonomy_charter` | — | イベリア総督府。解放タグに `autonomy_ibrgovernate` を付ける案 |
| `FRA_catalan_autonomy` | `FRA_autonomy_charter` | — | `CAT` 自治 |
| `FRA_basque_statute` | `FRA_autonomy_charter` | — | `NAV` 自治 |
| `FRA_galician_cortes` | `FRA_autonomy_charter` | — | `GLC` 自治 |
| `FRA_andalusian_question` | `FRA_direct_departements` | — | `ADU` コアの扱い |
| `FRA_iberia_integrated` | 直轄・自治いずれかの末端 | — | イベリア統合完了。重荷の軽減 |

### PAL連携列（9本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_paris_two_crowns` | `FRA_crown_scales_focus` | — | パリの二冠説明。`FRA_crown_seat` 初期値設定 |
| `FRA_lisbon_cortes` | `FRA_paris_two_crowns` | — | リスボン議会との定期会議 |
| `FRA_palis_envoy` | `FRA_lisbon_cortes` | — | パリ議会への特使 |
| `FRA_crown_in_lisbon` | `FRA_palis_envoy` | — | 座をリスボン側へ。変数加算 |
| `FRA_madeira_station` | `FRA_crown_in_lisbon` | — | マデイラ寄港協定 |
| `FRA_dual_coronation` | `FRA_crown_in_lisbon` | `FRA_pal_separation` | 二重戴冠。同君連合化 |
| `FRA_union_of_crowns` | `FRA_dual_coronation` | — | 王冠統合。PAL 併合案（同意イベント必須） |
| `FRA_pal_separation` | `FRA_palis_envoy` | `FRA_dual_coronation` | 王冠分離。PAL の州16コア放棄と相互防衛 |
| `FRA_lisbon_joint_fleet` | `FRA_dual_coronation` or `FRA_pal_separation` | — | リスボン合同艦隊 |

### 産業列（10本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_iberian_mines` | `FRA_iberian_administration` | — | 鉱山調査 |
| `FRA_rio_tinto_concessions` | `FRA_iberian_mines` | — | 鉱山利権 |
| `FRA_asturias_coal` | `FRA_iberian_mines` | — | アストゥリアス炭田 |
| `FRA_basque_steel` | `FRA_asturias_coal` | — | バスク製鉄 |
| `FRA_pyrennees_rail` | `FRA_iberian_administration` | — | ピレネー鉄道。軌間統一 |
| `FRA_madrid_workshops` | `FRA_pyrennees_rail` | — | マドリード工廠 |
| `FRA_renault_contracts` | `FRA_madrid_workshops` | — | ルノー請負 |
| `FRA_colonial_ports` | 幹 | — | 外地港。輸送船 |
| `FRA_five_year_plan` | `FRA_renault_contracts` | — | 五年計画 |
| `FRA_channel_trade` | `FRA_dover_question` | — | 海峡通商 |

### 軍事列（12本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_grand_armee_review` | `FRA_imperial_review` | — | 陸軍点検 |
| `FRA_gamelin_doctrine` | `FRA_grand_armee_review` | `FRA_degaulle_armor` | ガムラン系ドクトリン |
| `FRA_degaulle_armor` | `FRA_grand_armee_review` | `FRA_gamelin_doctrine` | ド・ゴール装甲 |
| `FRA_maginot_extension` | `FRA_gamelin_doctrine` | — | マジノ延長 |
| `FRA_pyrenees_line` | `FRA_maginot_extension` | — | ピレネー要塞線 |
| `FRA_alpine_forts` | `FRA_pyrenees_line` | — | アルプス要塞 |
| `FRA_colonial_army` | `FRA_grand_armee_review` | — | 外地軍テンプレ |
| `FRA_darlan_fleet` | 幹 | — | ダルラン艦隊 |
| `FRA_atlantic_squadron` | `FRA_darlan_fleet` | — | 大西洋艦隊。ドーバー・リスボン |
| `FRA_mediterranean_squadron` | `FRA_darlan_fleet` | — | 地中海艦隊 |
| `FRA_vuillemin_air` | 幹 | — | ビュイヤマン航空 |
| `FRA_air_reserve` | `FRA_vuillemin_air` | — | 航空予備 |

### 外交列（9本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_dover_question` | `FRA_imperial_review` | — | ドーバー問題。`FRA_dover_cliff` |
| `FRA_channel_entente` | `FRA_dover_question` | `FRA_channel_rivalry` | 対英協調 |
| `FRA_channel_rivalry` | `FRA_dover_question` | `FRA_channel_entente` | 海峡競争 |
| `FRA_rhineland_watch` | `FRA_imperial_review` | — | ライン監視。対独 |
| `FRA_alsace_memory` | `FRA_rhineland_watch` | — | アルザスの `RAL` コア |
| `FRA_italian_border` | `FRA_rhineland_watch` | — | サヴォワ・OCC 国境 |
| `FRA_exile_spain_watch` | `FRA_iberian_administration` | — | ESP 亡命監視。諜報 |
| `FRA_caribbean_expedition` | `FRA_exile_spain_watch` | — | 対ESP 遠征準備。承認列の対案 |
| `FRA_monaco_status` | `FRA_imperial_review` | — | モナコ地位協定 |

### 終局列（5本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_empire_of_west` | 政治列の確定 | — | 西方帝国宣言 |
| `FRA_iberian_coronation` | `FRA_iberia_integrated` | — | イベリア戴冠 |
| `FRA_twin_thrones_final` | `FRA_union_of_crowns` or `FRA_dual_coronation` | — | 双玉座の確定 |
| `FRA_continent_master` | `FRA_iberian_coronation` | — | 大陸統治の完成 |
| `FRA_new_charlemagne` | `FRA_continent_master` | — | 終端。シャルルマーニュ継承名 |

合計: 6+9+7+7+7+5+10+9+10+12+9+5 = **96本**。実装時に80〜90本へ絞ってよいが、PAL連携列とイベリア統治列は削らない。

## 実装時に残すもの

- 州16の `FRA`・`PAL` 二重コア、`give_guarantee = PAL`。コア放棄は `FRA_pal_separation` の選択効果に限定し、開幕は変えない。
- 全イベリア州の `FRA`・`ESP` 共存コア、自治系コア（`CAT`/`GLC`/`NAV`/`ADU`/`OCC`/`COR`/`BRI`/`RAL`/`MCO`/`MAD`/`ADR`/`GBR` on 835）。
- 既存の全キャラクター定義と recruit 行、既存 MIO 全定義、装備バリアント、OOB 三系。
- `political_set_M`、政党値、`FRA_republic` 化粧タグ、輸送船300・CP+20・安定0.5。
- `autonomy_ibrgovernate` と `is_iberian_nation` の現行定義。拡張する場合は別タスクとして切り分ける。
- `PAL` の国史・指導者・領有。PAL 側の実装はこの文書の範囲外。
- `PRT` のアゾレス・ギアナ領有とコア。
- ESP の復帰列との整合。ESP が復帰戦争を仕掛けた場合、FRA 側は `FRA_exile_spain_watch` 系で対応する設計とし、ESP 側の計画を破壊しない。

要調査の残件：`PAL` の自治ステータス（独立か従属かの現在値）、`GBR` タグの実名、ドーバー州の実プロビンス構成、`nc_FRA` トークン新設の可否、帝政列の `constitutional_emperor` と `constitutional_monarchy` の政党対応表。
