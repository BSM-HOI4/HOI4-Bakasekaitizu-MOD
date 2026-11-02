# フランス（イベリア併合・共同君主）シナリオ案

タグは `FRA`。1936年1月1日開始。既存の国家方針ファイルは空であり、方針樹はゼロから設計する。領有、キャラクター、MIO、PAL との関係は既存のゲームデータをそのまま継承する。

## 地図

フランスは大陸欧州の故地とイベリア半島の全域を併せ持つ。総領有州数は51州に達し、フランス本土、イベリア全域、サヴォワ（州735）、ドーバー（州835）、モナコ（州927）、インド洋のコモロ（州708）、北米沖のサンピエール（州730）で構成される。

イベリア地域は首都マドリード（州41）をはじめ、カタルーニャ（州165）、アラゴン西部（州166）、バレンシア（州167）、ムルシア（州168）、セビリア（州169）、エストレマドゥーラ（州170）、ガリシア（州171）、ナバラ（州172）、グラナダ（州173）、レオン（州174）、シウダー・レアル（州175）、ブルゴス（州176）、バレアレス（州177）、カナリア（州178）、サラマンカ（州788）、コルドバ（州789）、アストゥリアス（州790）、バリャドリド（州791）、バスク（州792）、グアダラハラ（州793）、東アラゴン（州794）、フランス領バスク（州806）のすべてを `FRA` が保有する。これらのうちバレアレスとカナリアを除く各州には `FRA` と `ESP` のコアが重複して付与されている。亡命スペイン（ESP）にとっての失われた地図は、フランスにとっては領有しながらも無数の火種を抱え込んだ重荷である。

各州には地方自治や分離派の潜在的コアが残存する。カタルーニャに `CAT`、ガリシアに `GLC`、ナバラ・バスク・仏領バスクに `NAV`、セビリア・グラナダ・コルドバに `ADU`、アンドラ（州925）に `ADR`、オクシタニア南部およびサヴォワに `OCC`、コルシカに `COR`、ブルターニュに `BRI`、アルザス（州28）に `RAL`、モナコに `MCO`、コモロに `MAD` が設定されている。さらにイギリス海峡を挟んだドーバーには `GBR` と `FRA` の二重コアが存在し、海峡対岸に自国領の橋頭堡を確保している。

ポルトガル本土は `PAL`（パリ）が統治する。首都リスボン（州112、海軍基地8、タングステン50、`PAL`・`ESP` 二重コア）を中心に、ポルト（州180）、グアルダ（州181）、ベジャ（州179）、サンタレン（州795）、マデイラ（州697）を領有する。そしてフランスの首都州であるイル＝ド＝フランス（州16）には `FRA` と `PAL` の二重コアが存在する。「パリ」を名乗る国家がポルトガルを治め、その原初の中枢がフランスの首都州と重なり合うという二重構造が、この世界線の前提である。

## 開幕

正式名称は「フランス」、化粧タグは `FRA_republic`（フランス共和国）。`political_set_M` により立憲君主制（`constitutional_monarchy`）が与党に就いており、選挙周期は12か月、支持率は憲政君主64%、共産20%、中道12%、民主3%、ファシズム1%である。開幕の元首はボナパルト家の `FRA_napoleon_VI`（ナポレオン六世、サブイデオロギー `constitutional_emperor`）。通貨トークン `nc_FRA` は未登録のため、表示の扱いは実装時に決める。

登録済みキャラクターは約60名を数える。指導者枠にはピエール・ラヴァル（`liberalism`）、エドゥアール・ダラディエ（`socialism`）、ナポレオン六世（`constitutional_emperor`）、ギョーマ（`centrism`）、モーリス・トレーズ（`stalinism`）、ニコ（`marxism`）が揃う。軍司令官および顧問にはペタン、ド・ゴール、ガムラン、ウェイガン、ダルラン、ビュイヤマン、ブリュム、モーラス、ビュカール、デュクロらが既に登用済みであり、新規キャラクターの追加は原則として行わない。

軍事は DLC 環境に応じて `FRA_1936` または `FRA_1936_nsb` の陸軍OOB、Man the Guns の海軍OOB、By Blood Alone の航空OOBが読み込まれ、主要国水準の初期技術を完備する。輸送船は300隻、コマンドパワー補正+20。

## 政治

政治列は「ナポレオン家の立憲帝政をいかに完遂し、あるいは終わらせるか」を焦点に、五方向へ深く分岐させる。各列は5〜9段の深度を持つ。

帝政の継続。ナポレオン六世の君主制を堅持し、12か月ごとに訪れる議会選挙を実質的な信任の儀礼へと変質させていく。ボナパルティズムに基づく国民投票を重ね、最終的に「西方の皇帝」としての戴冠を目指す。イデオロギーは立憲君主制（`constitutional_monarchy`）を維持する。

共和国への揺り戻し。ダラディエやレオン・ブリュムを擁立し、共和政への復帰を図る。化粧タグは初期状態で既に `FRA_republic` を保持しているため、国名と政体の乖離を解消する道となる。

王党・国家主義。シャルル・モーラスのアクシオン・フランセーズ運動やマルセル・ビュカール、フィリップ・ペタンの摂政体制を通じて「国家の再統合」を推し進める。イベリアの自治要求を強権的に抑え込む方向へ舵を切る。

共産。モスクワ寄りのトレーズとマルクス主義系のニコの二系統を軸に、人民戦線から人民委員会へと移行する。イベリア半島に潜伏する地下組織を懐柔・統合し、連邦体制を模索する。

中道・技術官僚。ギョーマ将軍を中心に政党政治を停止させ、実務官僚による統治体制を構築する。他系統の終点とは交わらない独立した短縮分岐として扱う。

## 固有メカニクス：二つの王冠（王冠の配分）

フランスでは議会支配や個別の証拠ではなく、玉座の重心を数える。

国変数 `FRA_crown_seat`（-100〜+100）を用い、負の領域をパリ宮廷（ボナパルト家）、正の領域をリスボン宮廷（PAL＝パリ議会）の優位として定義する。各種方針や決定の採択によって数値を変動させ、到達した閾値に応じて国家の帰趨を開く。

座がパリ側に極端に傾いた場合、イル＝ド＝フランスにおける PAL コアを無効化または請求整理する選択肢が現れ、PAL はフランスの従属国として組み込まれる。
座がリスボン側に極端に傾いた場合、二重戴冠の儀礼が進展し、PAL を形式上対等な共同君主として吸収した「西イベリア王冠」の成立へ至る。
変数を中央付近に留めた場合、現状の「パリが軍事的に保護し、リスボンが正統性を預かる」曖昧な共存関係が維持され、相互の安全保障体制のみが強化される。

管理変数は `FRA_crown_seat` を主軸とし、PAL 側には受容度を示す `PAL_crown_consent` を連携させる。

## PALとの関係

確定しているゲーム上の事実は、州16（イル＝ド＝フランス）における `FRA` と `PAL` の二重コア設定、および `FRA` から `PAL` への独立保障（`give_guarantee`）である。この特異な配置を「二重王冠／共同君主」の物語として解釈する。

PAL の国家指導者は `PALIS`（パリ議会、与党 `philanthropy`、サブイデオロギー `non_resistance`、選挙なし）であり、君主個人ではなく議会組織が王冠を預かっている。パリ議会とは「本来の都であるパリの座を失ったままリスボンに逃れた宮廷」であり、イル＝ド＝フランスのコアは彼らが保持し続ける正統性の権利書にほかならない。フランス帝国が PAL へ与えている独立保障は、皇帝がその権利書の有効性を公認している証拠と位置付ける。

関係性の結末は三つに大別される。

王冠統合。パリ議会の合意を取り付けて PAL を完全に併合し、ポルトガル本土をフランスの直轄領として統合する。王冠の重心がリスボン側へ十分に傾いている場合のみ選択を許す。

二重戴冠。併合の道を選ばず、PAL を対等な同君連合の同盟者として固定化する。既存の従属形態を活用し、両国の主権を並立させる。

王冠分離。PAL がイル＝ド＝フランスのコア権利書を正式に破棄する代償として、フランスの独立保障を攻守同盟へと格上げし、イベリア半島の産業基盤を共有する。州16からの PAL コア除去は、この選択的な合意イベントの効果としてのみ発生させ、開幕時の配置は変更しない。

## 産業

**イベリア鉱山。** アストゥリアスの石炭、バスクの鋼、リオ・ティント系の鉱山を FRA の民需・軍需へ組み込む列。史実の鉱山名は使うが、会社名は無名枠に留める。

**ピレネー鉄道。** フランス側とイベリア側の規格差を題材に、「軌間を揃える」建設列にする。インフラと州間接続の説明に使う。

**マドリード工廠。** 州41の既存工場を FRA 側の生産計画へ編入する。`CAT`・`NAV`・`ADU` のコア州では建設効果を落とし、コアの残る州は統治列と連動させる。

**リスボン船渠。** PAL 列と共有する合弁枠。PAL 側の海軍基地8を FRA の大西洋艦隊の修理拠点として使う説明。

**植民地と外地。** コモロ・サンピエールは小さいので、輸送船と海軍経験の小枝に留める。

**対ESP産業。** オリノコ油とのバーター／キュラソー合弁は友好側、亡命油の禁輸とイベリア自給は敵対側。`ESP_FRA_rapport` の産業層。

## 軍事

**陸軍。** ガムラン系の既存師団運用と、ド・ゴール系の装甲集中を排他分岐にする。ピレネー線とアルプス線を別枠の要塞列にし、マジノ延長と分ける。

**海軍。** ダルランを旗頭に、大西洋（ブレスト＋ドーバー＋リスボン寄港）と地中海の二艦隊構想に分ける。ドーバー州を持つ以上、海峡支配は海軍列の看板にする。

**航空。** ビュイヤマンの既存航空OOBを前提に、戦略爆撃と防空の二択を置く。

**外地軍。** イベリア側の鎮守部隊をテンプレとして用意し、自治列の抵抗抑制と連動させる。

**対ESP軍事。** アンティル共同哨戒と海峡共同監視は友好側、対潜競争と封鎖計画は敵対側。上陸ドクトリンは共有しない。

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

## 固有メカニクス：スペイン問題（対 ESP）

イベリア全コアを持つ亡命政府 `ESP` との関係は、監視と遠征だけでは足りない。**仲良くするか、冷ややかに共存するか、敵にするか**を、外交・軍事・産業の三層で同じ変数に載せる。

国変数は ESP 側の `ESP_FRA_rapport`（-100〜+100）を正本とし、FRA 方針・決定からも同じ値を動かす。閾値の目安は +60（友好確定）、0付近（冷たい共存）、-60（敵対確定）。ESP の「大西洋の関係」列と相互参照し、片方だけ友好を取っても相手が敵対なら中央へ引き戻す事件を挟む。

| 層 | 友好側（rapport 高） | 敵対側（rapport 低） |
| --- | --- | --- |
| 外交 | カラカス亡命政権の黙認、領事、イベリア共同憲章、アンドラ共治 | 監視強化、最後通牒、カリブ遠征、復帰戦争への備え |
| 軍事 | カリブ共同哨戒、セウタ海峡の共同管理、顧問交換（上陸ドクトリンは共有しない） | 対潜競争、アンティル封鎖準備、橋頭堡への牽制 |
| 産業 | オリノコ油と仏製機械のバーター、キュラソー合弁、研究ライセンス | 禁輸・拿捕、イベリア軍需の独自化、油依存の遮断 |

友好確定でもイベリアの `ESP` コアは消さない。平和末端は「自治枠を残して帰還戦争を封じる」か「カリブと飛び地だけをスペイン領として認める」。敵対確定は `FRA_caribbean_expedition` と ESP 復帰列の表裏になる。

## アンドラ（ADR）

州925は `FRA` 所有、`wasteland`、人的1532、インフラ1、資源なし。コアは `ADR`・`ESP`・`FRA` の三重。開幕に独立国家としての `ADR` はなく、化粧タグ `ADR_co-principality` と司教系キャラクターだけが定義されている。史実の共治（フランス元首＋ウルヘル司教）を、「イベリアを持つフランス」と「亡命スペイン」の接点に読み替える。

アンドラは `ESP_FRA_rapport` の測り棒でもある。友好側では共治公国を緩衝として立て、敵対側ではピレネーの監視砦にし、中立では三重コアのまま直轄放置する。領有変更は方針・事件の結果でのみ行い、開幕は動かさない。

**皇帝の共治権。** FRA はフランス側共治者として州925の法的説明を持つ。帝政列ではナポレオン六世の名で、共和列では大統領権の継承名で処理する。

**渓谷の解放。** rapport 高かつ ESP が共治交渉を取ったとき、同意イベントで州925を `ADR` 解放し、双方保証の中立小国にする。コアは三重のまま。拒否すれば交渉決裂で rapport を下げる。

**ピレネー監視。** 敵対側では要塞・諜報拠点化し、ESP のピレネー連絡を妨害する。州カテゴリや資源は増やさない。

## 外交

- `PAL`：専用列を参照。保障・二重コア・王冠の配分の三点で動かす。
- `ESP`：**スペイン問題**列が本筋。監視・封じ込め・カリブ遠征に加え、友好・産業・軍事の三層とアンドラ共治を置く。ESP の復帰列・大西洋列と表裏。
- `ADR`：上記アンドラ列。タグ解放は友好末端の同意イベントのみ。
- `GBR`：ドーバー問題。海峡の共同管理か、ドーバーを返して対独協調を取るかの分岐。
- `GER`：アルザスの `RAL` コアとライン地帯。対独強硬か宥和か。
- `ITA`：サヴォワと `OCC` コアの問題。タグ名は実装時に確認。
- `PRT`：ギアナ領とアゾレスの小国。PAL を統合した場合の残存ポルトガル問題として軽く触れる。

## 方針樹

接頭辞は `FRA_`。幹を中央、政治の五列を左、イベリア統治・産業を右上、軍事を右下、PAL・対ESP・アンドラ・外交を下部に置く。合計 **約117本** の長ルート設計。効果の方向のみ固定する。

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

### 産業列（10本）＋対ESP産業枝（4本）

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
| `FRA_machine_for_orinoco` | `FRA_spain_handshake` | `FRA_embargo_exile_oil` | 機械⇔オリノコ油。rapport+、民需 |
| `FRA_curacao_joint_slot` | `FRA_machine_for_orinoco` | — | キュラソー合弁枠。燃料共有、rapport+ |
| `FRA_embargo_exile_oil` | `FRA_spain_cold_file` | `FRA_machine_for_orinoco` | 亡命油の禁輸。rapport- |
| `FRA_iberian_autarky` | `FRA_embargo_exile_oil` | — | イベリア自給軍需。消費財悪化、軍需方向 |

### 軍事列（12本）＋対ESP軍事枝（4本）

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
| `FRA_joint_antilles_patrol` | `FRA_spain_handshake` | `FRA_exile_asw_race` | アンティル共同哨戒。rapport+ |
| `FRA_strait_shared_watch` | `FRA_joint_antilles_patrol` | — | セウタ海峡共同監視。友好版 |
| `FRA_exile_asw_race` | `FRA_spain_cold_file` | `FRA_joint_antilles_patrol` | 対亡命対潜競争。rapport- |
| `FRA_antilles_blockade_plan` | `FRA_exile_asw_race` | — | アンティル封鎖計画。遠征列へ接続 |

### 対ESP関係列（8本）

旧 `FRA_exile_spain_watch` / `FRA_caribbean_expedition` を拡張する。

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_spain_question` | `FRA_iberian_administration` | — | スペイン問題の説明。rapport 参照開始 |
| `FRA_spain_handshake` | `FRA_spain_question` | `FRA_spain_cold_file` | 対ESP握手。rapport+、領事 |
| `FRA_spain_cold_file` | `FRA_spain_question` | `FRA_spain_handshake` | 冷たいファイル。監視・諜報、rapport- |
| `FRA_caracas_recognition` | `FRA_spain_handshake` | — | カラカス黙認。ESP の承認の証を平和で満たす側 |
| `FRA_iberian_joint_charter_fra` | `FRA_caracas_recognition` | — | イベリア共同憲章（FRA側）。友好確定、ESP復帰戦争を封じる同意 |
| `FRA_exile_spain_watch` | `FRA_spain_cold_file` | — | 亡命監視の本格化 |
| `FRA_caribbean_expedition` | `FRA_exile_spain_watch` | — | 対ESP遠征準備。敵対確定への滑走路 |
| `FRA_atlantic_entente_fra` | `FRA_iberian_joint_charter_fra` かつ産業・軍事友好枝の末端 | — | 大西洋協商（FRA側）。アンドラ共治の前提 |

### アンドラ列（7本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_andorra_valley` | `FRA_iberian_administration` or `FRA_spain_question` | — | 渓谷の現状。三重コアの説明 |
| `FRA_imperial_coprince` | `FRA_andorra_valley` | — | 皇帝／大統領の共治権の法的確認 |
| `FRA_coprincipality_offer` | `FRA_imperial_coprince` かつ `FRA_spain_handshake` | `FRA_andorra_fort` | 共治提案。ESP 同意事件、rapport+ |
| `FRA_release_adr` | `FRA_coprincipality_offer` かつ ESP 側 `ESP_restore_adr` 相当 | — | 州925を `ADR` 解放、双方保証、`ADR_co-principality` |
| `FRA_andorra_fort` | `FRA_imperial_coprince` かつ `FRA_spain_cold_file` | `FRA_coprincipality_offer` | 渓谷要塞化。ピレネー監視、rapport- |
| `FRA_pyrenees_listen_post` | `FRA_andorra_fort` | — | 傍受所。ESP ピレネー連絡の妨害 |
| `FRA_valley_customs` | `FRA_release_adr` or（中立のまま `FRA_andorra_valley`） | — | 渓谷関税。小さな通商 |

### 外交列（7本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_dover_question` | `FRA_imperial_review` | — | ドーバー問題。`FRA_dover_cliff` |
| `FRA_channel_entente` | `FRA_dover_question` | `FRA_channel_rivalry` | 対英協調 |
| `FRA_channel_rivalry` | `FRA_dover_question` | `FRA_channel_entente` | 海峡競争 |
| `FRA_rhineland_watch` | `FRA_imperial_review` | — | ライン監視。対独 |
| `FRA_alsace_memory` | `FRA_rhineland_watch` | — | アルザスの `RAL` コア |
| `FRA_italian_border` | `FRA_rhineland_watch` | — | サヴォワ・OCC 国境 |
| `FRA_monaco_status` | `FRA_imperial_review` | — | モナコ地位協定 |

### 終局列（5本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `FRA_empire_of_west` | 政治列の確定 | — | 西方帝国宣言 |
| `FRA_iberian_coronation` | `FRA_iberia_integrated` | — | イベリア戴冠 |
| `FRA_twin_thrones_final` | `FRA_union_of_crowns` or `FRA_dual_coronation` | — | 双玉座の確定 |
| `FRA_continent_master` | `FRA_iberian_coronation` | — | 大陸統治の完成 |
| `FRA_new_charlemagne` | `FRA_continent_master` | — | 終端。シャルルマーニュ継承名 |

合計: 6+9+7+7+7+5+10+9+14+16+8+7+7+5 = **約117本**。実装時に95〜105本へ絞ってよいが、PAL連携・イベリア統治・対ESP三層・アンドラ列は削らない。

## 実装時に残すもの

- 州16の `FRA`・`PAL` 二重コア、`give_guarantee = PAL`。コア放棄は `FRA_pal_separation` の選択効果に限定し、開幕は変えない。
- 全イベリア州の `FRA`・`ESP` 共存コア、自治系コア（`CAT`/`GLC`/`NAV`/`ADU`/`OCC`/`COR`/`BRI`/`RAL`/`MCO`/`MAD`/`ADR`/`GBR` on 835）。
- 州925の `FRA` 所有と `ADR`/`ESP`/`FRA` 三重コア。`ADR_co-principality` と既存 ADR キャラクター。解放は `FRA_release_adr` と ESP 側同意の両方が揃ったときのみ。
- 既存の全キャラクター定義と recruit 行、既存 MIO 全定義、装備バリアント、OOB 三系。
- `political_set_M`、政党値、`FRA_republic` 化粧タグ、輸送船300・CP+20・安定0.5。
- `autonomy_ibrgovernate` と `is_iberian_nation` の現行定義。拡張する場合は別タスクとして切り分ける。
- `PAL` の国史・指導者・領有。PAL 側の実装はこの文書の範囲外。
- `PRT` のアゾレス・ギアナ領有とコア。
- ESP の復帰列・大西洋列との整合。ESP が復帰戦争を仕掛けた場合は `FRA_spain_cold_file` 系で対応し、友好確定時は戦争目標を封じる。ESP 側の計画を破壊しない。

要調査の残件：`PAL` の自治ステータス（独立か従属かの現在値）、`GBR` タグの実名、ドーバー州の実プロビンス構成、`nc_FRA` トークン新設の可否、帝政列の `constitutional_emperor` と `constitutional_monarchy` の政党対応表、ADR 解放時の Default_oob 差し替え要否。
