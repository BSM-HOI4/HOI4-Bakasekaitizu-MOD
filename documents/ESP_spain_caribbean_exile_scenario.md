# スペイン（カリブ亡命）シナリオ案

タグは `ESP`。1936年1月1日開始。`common/national_focus/spain.txt` は事実上の空ファイルで、方針樹・企業・設計局・国民精神・登録キャラクターはまだ存在しない。この文書は実装仕様ではなく、既存の領有・傀儡関係・MODシステムに合わせた案である。

## 地図

本土は失われている。ESP が所有するのはカリブ・ベネズエラ側の五州だけである。

| 州 | ファイル名 | 備考 |
| --- | --- | --- |
| 307 | Venezuela（注記 Miranda） | 首都。人口約133万、油41・石炭20、民需5・軍需1、航空基地2、海軍基地3＋2、VP5、州変数 `gold_mine = 1` |
| 488 | Bolivar | 内陸 pastoral、人口約14.6万 |
| 489 | Monagas | town、人口約158万、油35・石炭18、民需2、海軍基地5 |
| 695 | Curacao | rural、人口約7.6万、油35・石炭18、燃料庫、海軍基地1、沿岸要塞2、VP1 |
| 971 | Bolivar | pastoral、人口約10万 |

傀儡は二つ。`CEU`（セウタ、州1101。人口1811、海軍基地3、航空基地1、VP5）と `PML`（メリリャ、州1098。人口7.4万、海軍基地3、航空基地3、VP2、化粧タグ `PML_esp`）で、いずれもジブラルタル海峡の向こう側に残る地中海の爪である。

イベリア半島はすべて `FRA` 所有である。マドリード（州41）を含むスペイン本土各州には `FRA` と `ESP` の両方のコアが既に付いており、ESP 側は「コアはあるが地がない」状態である。例外はバレアレス（州177）とカナリア（州178）で、こちらは `FRA` コアのみで ESP コアがない。リスボン（州112）は `PAL` 所有で `PAL`・`ESP` 二重コア、アンドラ（州925）は `ADR`・`ESP`・`FRA` 三重コアである。

カリブ側の隣接地として、`PRT`（ポルトガル）がギアナ諸州（309・310・687・972）を持っており、ESP のボリバル・モナガスとは陸で接している。PRT の首都はアゾレス（州698）で、ポルトガル本土は `PAL` が持つ。ESP・PRT・PAL の三者関係は南米北岸で続く。

## 開幕

正式名称は「スペイン」、化粧タグは `ESP_republic`（スペイン共和国）。通貨トークンは `nc_NSI` 系の自動定義にある `nc_ESP` で、表示はスペイン・クローネ（kr）。政権は `democratic_ideology` で始まり、最終選挙1933年2月、周期36か月である。登録キャラクターのファイルは存在せず、開幕の指導者・顧問・将軍はすべて新設が要る。

軍事は `ESP_1936` で歩兵師団を中心とした18個師団と、Man the Guns 時の `ESP_1936_naval`（軽巡 Libertad、駆逐艦4、潜水艦2、母港はプロビンス1944）、By Blood Alone 時の `ESP_1936_air` がある。亡命したのに艦隊が残っている、という形である。輸送船150、安定0.5。

## 政治

本土失陥後の亡命政権なので、政治列は「どの正統でスペインを名乗るか」を深くする。各ルートは末端まで4〜7段を基本とする。

史実人物は1936年時点の位置が書けるものに限る。共和国側はこのMOD内で本土を既に失った設定なので、ニセト・アルカラ＝サモラ（1936年4月まで大統領）、マヌエル・アサーニャ（1936年5月から大統領）、インダレシオ・プリエト、ラルゴ・カバリェロ、フアン・ネグリン、ディエゴ・マルティネス・バリオらが亡命側にいる、という処理を案とする。実際の大量亡命は史実では1939年以降であり、時系列のずれは文面で「この世界線の設定」と明記する。王党派はローマにいたアルフォンソ十三世（1941年死去）とフアン・デ・ボルボン、カルリスタはマヌエル・ファル・コンデとハビエル・デ・ボルボン＝パルマ。ファランヘはホセ・アントニオ・プリモ・デ・リベラが1936年に獄中である点を踏まえ、生死不明枠か後継者枠で扱い、確定は実装時にする。共産側はドローレス・イバルリとホセ・ディアス。軍人はホセ・ミアハ、ビセンテ・ロホ、ミゲル・ブイサ（共和国艦隊司令）を亡命艦隊に当てる。

現地側は、1935–41年にベネズエラ大統領だったエレアサール・ロペス・コントレラスと、陸海軍相イサイアス・メディナ・アンガリータを「宿主」の顔に据える案。カタルーニャのリュイス・コンパニス、バスクのホセ・アントニオ・アギーレ、ガリシアのカステラオは、亡命先に集まる自治派として枝分かれに使う。

### 共和国再編

亡命憲章を続け、アサーニャを戴く正統路線。プリエトの穏健連立で安定を稼ぎ、在外選挙で正統の証を上げる。化粧タグは `ESP_republic` のまま残る。

### 王政復古

ローマのアルフォンソ十三世かフアン王子を迎える。カルリスタを別分岐にし、二人の王を一つの玉座に重ねる和解で終えるか、正統派一本に絞るかを選ばせる。`neutrality_ideology` 系か既存の `constitutional_monarchy` のどちらに乗せるかは、政党群の実装を見て決める。

### ファランヘ

亡命先で「イスパニダー」を唱える列。国民シンジカリスモをカリブの労働者に訳して持ち込む説明にし、本土より先に新大陸で体制を作る皮肉を効かせる。`fascism_ideology`。

### 人民戦線・共産

イバルリとホセ・ディアスの列。亡命民兵を組織し、メキシコとの連携で物資を回す。`communism_ideology`。

### カリブ連邦・「地図上のスペイン」

復帰を捨てて新世界に根付く列。ロペス・コントレラスとの協定でミランダの統治を確定させ、アンティル諸島との連邦を目指す。末端で復帰列を封じ、国名を「地図上のスペイン」に格下げする仮称ルートにする案。コアと傀儡は残したまま、名だけが失われる結末である。

## 固有メカニクス：帰還の四証

NTS の「机」とは別の軸として、ESP では**四つの証**を数える。国変数 `ESP_proof_fleet`・`ESP_proof_bridgehead`・`ESP_proof_legitimacy`・`ESP_proof_recognition`（各0〜3）に、方針と決定で段を積む。復帰列の終盤は、艦隊の証（亡命艦隊を大西洋横断できるまで仕立てる）、橋頭堡の証（CEU/PML を要塞化し内側から使える状態にする）、正統の証（選んだ政権が国内に受け入れられる名を持つ）、承認の証（列強の黙認か支援を得る）の四点を同時に満たすことを要求する。どれか一つでも欠けると上陸方針は選べない、という門番にする。実装は4変数＋方針の `available` で足り、GUI は要らない。

## 産業

**オリノコの油。** 州489と695の油は既に35ずつある。精製側をキュラソーに寄せる設計にし、史実のキュラソー製油所（1918年操業のイスラ製油所、原油はベネズエラ産）を史実の核に据える。艦隊の燃料証にも直結させる。

**亡命造船。** 海軍基地5のモナガスを母港に、亡命艦隊の改修と新造を回す。工場数は小さいので、造船所建設の即時報酬より既存設備の拡張方向にする。

**亡命知識人。** スペイン語の大学・印刷・医学をカラカスに移す列。文明度と研究速度を小さく足し、「国は地図にないが蔵書はある」説明にする。

**ボリバルの金。** 州307の `gold_mine` 変数は既にあるので、`nc_ESP` の担保として説明だけ付け、産出イベントは小さく。

## 軍事

**亡命艦隊。** 軽巡1・駆逐4・潜水2が現存する。ブイサを旗頭に据え、キュラソーとモナガスを二母港にする。艦隊の証はこの列を通る。

**上陸ドクトリン。** 目的地は地中海である。海兵・上陸・上陸用装備の研究ボーナスを積み、陸軍の量は増やさない方向。

**外人部隊の残党。** スペイン外人部隊は史実でモロッコ側の兵である。CEU/PML が傀儡で残っている以上、部隊の名を傀儡側に残し、宗主が師団テンプレとして受け取る枝を置く。

**セウタ要塞。** 傀儡州の要塞化は宗主側の建設か傀儡方針で扱い、橋頭堡の証を上げる。

**航空。** 開幕の `ESP_1936_air` を前提に、カリブ哨戒と本土往還を分ける小さい列に留める。

## 企業

`common/ideas` の designer として置く。数値方向のみ固定。

| ID | 種別 | 史実の核 | 解禁 | 効果の方向 |
| --- | --- | --- | --- | --- |
| `ESP_isla_refinery` | industrial_concern | キュラソーのイスラ製油所（1918–） | キュラソー精製の方針 | 燃料、油の通商 |
| `ESP_orinoco_petroleum` | industrial_concern | オリノコ方面の石油開発。社名は無名枠と明記 | オリノコ油田の方針 | 燃料、産出 |
| `ESP_banco_exterior` | industrial_concern | 国外業務のスペイン銀行（史実のBanco Exterior相当） | 開幕から | 政治力、通商収入 |
| `ESP_astilleros_caribe` | naval_manufacturer | 亡命後にモナガスへ寄せた艤装職人 | 亡命造船の方針 | 艦艇研究・改修 |
| `ESP_imprenta_exilio` | industrial_concern | 亡命先のスペイン語印刷・出版 | 亡命知識人の方針 | 研究速度、安定 |
| `ESP_ceuta_arsenal` | materiel_manufacturer | セウタの要塞工廠 | 橋頭堡方針 | 歩兵装備・要塞 |
| `ESP_tabaco_habana` | industrial_concern | スペイン系タバコ交易 | カリブ連邦列 | 消費財、通商 |
| `ESP_aviacion_caribe` | aircraft_manufacturer | モナガス航空基地の改修枠 | 航空列 | 航空機研究 |

開幕から見せるのは `ESP_banco_exterior` と `ESP_isla_refinery`（精製所は史実が動いている）の二つ、残りは方針報酬で解禁する案。

## 設計局

**モナガス艤装所** `ESP_monagas_yard_organization`

- 装備は軽巡以下の改修と輸送船。
- 初期特性「亡命先の埠頭」：改修コストを下げ、新造速度を下げる。
- 特性「大西洋往還」は艦隊の証二段目で開く。

**カラカス兵器廠** `ESP_caracas_arsenal_organization`

- 装備は歩兵火器・支援装備。
- 初期特性「別の言葉の図面」：信頼性微減、生産コスト微減。

**セウタ要塞工兵** `ESP_ceuta_engineers_organization`

- 装備は砲と要塞資材。
- 初期特性「海峡の幅を知る」：対艦・対地砲の命中方向に微増。
- 解禁は橋頭堡方針。傀儡側MIOではなく宗主側に置く。

**亡命航空工房** `ESP_exile_air_organization`

- 装備は既存の哨戒機系。
- 初期特性「図面だけが届いた」：生産コスト増、研究ボーナス微増。

## 国民精神

カテゴリは `country`。数値は実装時に調整し、方向だけ固定する。

**亡命政権** `ESP_government_in_exile`（開幕から）

- 政治力微増、安定微減。本土を持たない政府であることを説明。
- 帰還完了かカリブ連邦確定で置き換える。

**二つの祖国** `ESP_two_homelands`（開幕から）

- 徴兵と工場のわずかな二律背反。地に根付くほどスペインの主張が薄れる説明。

**クローネの担保** `ESP_krone_backing`（開幕から）

- `Unified_Currency_gain_factor` 微増。ボリバルの金の説明にする。

**艦隊の証** `ESP_proof_fleet_idea`（復帰列）

- 海軍経験と艦隊出力の加算。段に応じて置き換える。

**地中海の爪** `ESP_mediterranean_claws`（橋頭堡列）

- CEU/PML の従属度と傀儡師団強化の説明。

**マドリードは地図にある** `ESP_madrid_on_the_map`（正統の証三段目）

- 戦争支持微増、本土諸州の抵抗減少方向。

**地図上のスペイン** `ESP_map_spain`（カリブ連邦末端）

- 安定と消費財の改善、本土回帰系を封じる説明。名称変更イベントと対になる。

## このMODの国家idea

**文明度。** 亡命知識人の列で `base_Cultural_Degree` を小さく足す方向。「スペインの蔵書は船で来た」説明。カリブ連邦列では現地への移行として足さない。

**国家統合力。** 開幕は低めに据え、正統の証を上げるごとに `National_Unity_Power_gain_factor` を足す。「地図上のスペイン」ルートは統合力を捨てて安定へ振り替える。

**統一通貨。** `nc_ESP` の「スペイン・クローネ」は残す。亡命政府が発行する実体の薄い通貨、という説明にし、ボリバルの金と銀行の二本で係数を支える。カリブ連邦確定時に表示名の整理を検討する（実装時調整）。

**宗教。** 新しい宗教法は作らず、既存の宗教法からカトリック系を選ぶ方向。王政路線で宗教の係数を明示的に使う案は実装時に辞書と照合する。

**従属体系。** CEU/PML の `puppet` は通常傀儡のまま残す。橋頭堡列で `autonomy_ibrgovernate`（イベリア総督府）への格上げを検討するが、その `allowed` の `is_iberian_nation` は `original_tag = SPR/POR/SPA/CAT` を見ており `ESP` を含まない点に注意が要る。配線は実装時に該当トリガの修正範囲として切り分ける。

## 外交

- `FRA`：イベリア全域を持つ相手。承認の証は FRA の黙認か FRA との戦争の二択にし、亡命政権を FRA が認める平和ルート（飛び地自治での引き渡し）も末端に一本置く。
- `PAL`：リスボンの ESP コアが外交火種になる。リスボン問題の方針で PAL と敵対するか、イベリア回収の際にコアを棚上げするかを選ばせる。PAL 側は FRA が `give_guarantee` している点を文面に織り込む。
- `PRT`：ギアナ国境だけが接する小国同士。国境確定・貿易・アゾレス寄港の小列に留め、PRT のコアは触らない。
- `USA`・`MEX`：史実の亡命先はメキシコだった。メキシコ列を承認と物資の供給元として使う。タグの実在は実装時に確認する。
- `CEU`・`PML`：傀儡のまま残すか、橋頭堡列で吸収して直接要塞州にするかを分岐にする。吸収は傀儡解消（annex）＋州コア取得で処理し、タグ自体は残す案。

## 方針樹

接頭辞は `ESP_`。幹を中央、政治の複数列を左、産業・軍事を右、外交・復帰を下部に置く。合計80本規模の長ルート設計で、効果の方向のみ固定する。

### 幹（6本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_exile_government` | — | — | 起点。`ESP_government_in_exile` 確認、PP |
| `ESP_caracas_charter` | `ESP_exile_government` | — | 亡命憲章。正統の証+1 |
| `ESP_the_lost_map` | `ESP_caracas_charter` | — | 本土喪失の確認イベント。本土諸州コアの一覧表示 |
| `ESP_spanish_registry` | `ESP_the_lost_map` | — | 亡命者名簿。顧問枠の人材決定 |
| `ESP_four_proofs` | `ESP_spanish_registry` | — | 四証の変数起動 |
| `ESP_two_homelands_focus` | `ESP_four_proofs` | — | 政治列と連邦列の分岐開放 |

### 政治：共和国再編列（6本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_second_republic` | `ESP_two_homelands_focus` | `ESP_royalist_emissaries`, `ESP_falange_exiles`, `ESP_passion_flower` | 共和国継続宣言。democratic |
| `ESP_azana_presidency` | `ESP_second_republic` | — | アサーニャを指導者に |
| `ESP_moderate_coalition` | `ESP_azana_presidency` | `ESP_united_front_again` | プリエトの穏健連立。安定 |
| `ESP_united_front_again` | `ESP_azana_presidency` | `ESP_moderate_coalition` | 左派との合同。共産列への橋 |
| `ESP_constitution_in_exile` | `ESP_moderate_coalition` or `ESP_united_front_again` | — | 亡命憲法。正統の証+1 |
| `ESP_elections_abroad` | `ESP_constitution_in_exile` | — | 在外選挙イベント。正統の証+1 |

### 政治：王政復古列（7本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_royalist_emissaries` | `ESP_two_homelands_focus` | `ESP_second_republic` 系 | 王党派の使者。neutrality/monarchy系 |
| `ESP_alfonso_in_rome` | `ESP_royalist_emissaries` | `ESP_carlist_compact` | アルフォンソ十三世の支持 |
| `ESP_carlist_compact` | `ESP_royalist_emissaries` | `ESP_alfonso_in_rome` | ファル・コンデのカルリスタ協約 |
| `ESP_infante_juan` | `ESP_alfonso_in_rome` | — | フアン王子への継承整理 |
| `ESP_two_crowns` | `ESP_carlist_compact` | — | 二王の和解イベント |
| `ESP_crown_over_sea` | `ESP_infante_juan` or `ESP_two_crowns` | — | 海を越えた戴冠。正統の証+2 |
| `ESP_regency_atlantic` | `ESP_crown_over_sea` | — | 摂政評議会。安定、復帰列解禁 |

### 政治：ファランヘ列（6本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_falange_exiles` | `ESP_two_homelands_focus` | `ESP_second_republic` 系 | ファランヘ亡命者。fascism |
| `ESP_jons_legacy` | `ESP_falange_exiles` | — | JONS系の継承 |
| `ESP_primo_rivera_shadow` | `ESP_jons_legacy` | — | プリモ・デ・リベラの生死不明扱い事件 |
| `ESP_national_syndicate` | `ESP_primo_rivera_shadow` | — | 国民シンジカリスモ。工場方向 |
| `ESP_hispanidad` | `ESP_national_syndicate` | — | イスパニダー。カリブ・中南米関係 |
| `ESP_caudillo_candidate` | `ESP_hispanidad` | — | 総統候補の指導者交代 |

### 政治：人民戦線・共産列（6本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_passion_flower` | `ESP_two_homelands_focus` | `ESP_second_republic` 系 | イバルリ。communism |
| `ESP_jose_diaz_line` | `ESP_passion_flower` | — | ホセ・ディアスの党再建 |
| `ESP_militia_fleets` | `ESP_jose_diaz_line` | — | 民兵と船団。徴兵方向 |
| `ESP_union_of_exiles` | `ESP_militia_fleets` | — | 亡命組合連合 |
| `ESP_red_spain_america` | `ESP_union_of_exiles` | — | 赤いスペイン・アメリカ支部。承認の証の別経路 |
| `ESP_pozas_rearguard` | `ESP_red_spain_america` | — | ポサス系将軍の後衛配置 |

### 政治：カリブ連邦列（6本）＋末端仮称

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_caribbean_assembly` | `ESP_two_homelands_focus` | 復帰列の終盤と排他 | アンティル議会構想 |
| `ESP_lopez_pact` | `ESP_caribbean_assembly` | — | ロペス・コントレラス協定。安定 |
| `ESP_spanish_venezuela` | `ESP_lopez_pact` | — | ミランダ統治の確定。消費財方向 |
| `ESP_antilles_league` | `ESP_spanish_venezuela` | — | 周辺島嶼との連邦交渉 |
| `ESP_new_carthage` | `ESP_antilles_league` | — | 新カルタゴ構想。艦隊の証を経済に振替 |
| `ESP_map_spain` | `ESP_new_carthage` | `ESP_operation_return` 系 | 「地図上のスペイン」へ名称格下げ。復帰列を封じる |

### 産業列（11本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_orinoco_derricks` | 幹 | — | 州489の油増産 |
| `ESP_isla_refinery_focus` | `ESP_orinoco_derricks` | — | キュラソー精製。燃料、`ESP_isla_refinery` |
| `ESP_fuel_for_fleet` | `ESP_isla_refinery_focus` | — | 燃料備蓄。艦隊の証+1 |
| `ESP_caracas_workshops` | 幹 | — | 州307の民需増設 |
| `ESP_exile_shipwrights` | `ESP_caracas_workshops` | — | 造船所と `ESP_astilleros_caribe` |
| `ESP_university_in_exile` | 幹 | — | 亡命大学。研究スロット方向 |
| `ESP_imprenta_madrid` | `ESP_university_in_exile` | — | 印刷。`ESP_imprenta_exilio` |
| `ESP_bolivar_gold` | 幹 | — | 金鉱。`nc_ESP` 係数 |
| `ESP_convoy_flag` | `ESP_caracas_workshops` | — | 輸送船団。通商方向 |
| `ESP_krone_standard` | `ESP_bolivar_gold` | — | クローネ安定。通商・PP |
| `ESP_antilles_market` | `ESP_antilles_league` | — | 連邦市場。消費財・民需 |

### 軍事列（14本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_fleet_review` | 幹 | — | 亡命艦隊の点検。海軍経験 |
| `ESP_buiza_flag` | `ESP_fleet_review` | — | ブイサ提督の旗。艦隊の証+1 |
| `ESP_curacao_squadron` | `ESP_buiza_flag` | — | キュラソー分艦隊 |
| `ESP_refitted_libertad` | `ESP_curacao_squadron` | — | リベルタ改修 |
| `ESP_submarine_wolves` | `ESP_buiza_flag` | — | 潜水狼群。艦隊の証+1 |
| `ESP_miaja_staff` | 幹 | — | ミアハ参謀。陸軍経験 |
| `ESP_rojo_academy` | `ESP_miaja_staff` | — | ロホの軍学校。将官 |
| `ESP_legion_in_exile` | `ESP_miaja_staff` | — | 外人部隊残党の再編 |
| `ESP_amphibious_doctrine` | `ESP_rojo_academy` | — | 上陸ドクトリン研究 |
| `ESP_landing_battalions` | `ESP_amphibious_doctrine` | — | 海兵大隊テンプレ |
| `ESP_air_exile_wings` | 幹 | — | 亡命航空団 |
| `ESP_caribbean_patrol` | `ESP_air_exile_wings` | — | カリブ哨戒 |
| `ESP_long_range_ferry` | `ESP_caribbean_patrol` | — | 航続延長。艦隊の証の補助 |
| `ESP_generalstaff_return` | `ESP_landing_battalions` | — | 帰還参謀本部。復帰列の軍前提 |

### 橋頭堡列（7本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_mediterranean_claws` | 幹 | — | CEU/PML の現状確認 |
| `ESP_ceuta_arsenal_focus` | `ESP_mediterranean_claws` | — | セウタ工廠。傀儡建設 |
| `ESP_melilla_watch` | `ESP_ceuta_arsenal_focus` | — | メリリャ監視網。航空基地拡張 |
| `ESP_strait_fortress` | `ESP_melilla_watch` | — | 海峡要塞化。橋頭堡の証+1 |
| `ESP_puppet_staffs` | `ESP_strait_fortress` | — | 傀儡参謀統合 |
| `ESP_absorb_the_claws` | `ESP_puppet_staffs` | `ESP_keep_the_claws` | CEU/PML 吸収案。州コア取得 |
| `ESP_keep_the_claws` | `ESP_puppet_staffs` | `ESP_absorb_the_claws` | 傀儡維持。従属深化 |

### 外交列（7本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_league_petition` | `ESP_four_proofs` | — | 国際連盟への訴え。承認の証+1 |
| `ESP_mexican_hand` | `ESP_league_petition` | — | メキシコ供給線 |
| `ESP_washington_briefing` | `ESP_mexican_hand` | — | 米国説得 |
| `ESP_guiana_border` | `ESP_four_proofs` | — | PRT とのギアナ国境確定 |
| `ESP_caribbean_recognition` | `ESP_washington_briefing` | — | 米州承認。承認の証+1 |
| `ESP_fra_containment` | 幹 | `ESP_fra_approach` | 対仏牽制。諜報方向 |
| `ESP_fra_approach` | 幹 | `ESP_fra_containment` | 対仏交渉。承認の証の別経路 |

### 復帰列（12本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_reconquista_plan` | `ESP_generalstaff_return` | `ESP_map_spain` | レコンキスタ計画。四証を要求する門 |
| `ESP_maquis_network` | `ESP_reconquista_plan` | — | 本土地下組織。抵抗支援 |
| `ESP_pyrenees_line` | `ESP_maquis_network` | — | ピレネー越えの連絡線 |
| `ESP_iberian_uprising` | `ESP_pyrenees_line` | — | イベリア蜂起イベント |
| `ESP_balearic_stepping` | `ESP_iberian_uprising` | — | バレアレス主張。州177へ ESP コア追加案 |
| `ESP_canary_anchor` | `ESP_balearic_stepping` | — | カナリア中継。州178へ ESP コア追加案 |
| `ESP_andorra_post` | `ESP_pyrenees_line` | — | アンドラ連絡所 |
| `ESP_lisbon_question` | `ESP_iberian_uprising` | — | リスボンの ESP コアの扱い。PAL との交渉か併呑 |
| `ESP_french_gate` | `ESP_lisbon_question` | — | FRA への最後通牒 or 交渉 |
| `ESP_operation_return` | 四証すべて閾値以上 | `ESP_map_spain` | 帰還作戦。FRA への戦争目標 |
| `ESP_madrid_or_nothing` | `ESP_operation_return` | — | マドリード奪還後の再建。本土州への統治効果 |
| `ESP_iberia_restored` | `ESP_madrid_or_nothing` | — | 終端。イベリア再統合と国民精神の更新 |

合計: 6+6+7+6+6+6+11+14+7+7+12 = **88本**。実装時に70本前後へ削ってもよいが、列の末端まで切らない。

## 国境・復帰計画

この計画が通るまで州は動かさない。

- 本土各州の `ESP` コアは既に付いているので追加しない。動くのは州177・178への ESP コア追加（`ESP_balearic_stepping`・`ESP_canary_anchor`）だけである。
- リスボン（州112）は `PAL`・`ESP` 二重コアのまま維持し、`ESP_lisbon_question` で PAL との交渉事件にする。PAL のコアを消さない。
- CEU/PML は傀儡のままか吸収かを分岐にし、いずれの場合も州1101・1098 の `CEU`/`PML` コアは残す。
- マドリードを含む全本土州の `FRA` コアは残す。ESP のコアと FRA のコアが共存する状態が前提の世界線である。
- 復帰戦争の戦争目標は `ESP_operation_return` で発行し、占領後のコア化は和平結果に置く。開幕に州を動かさない。

## 実装時に残すもの

- 州307・488・489・695・971 の所有とコア、資源値、`gold_mine` 変数。
- `ESP_republic` 化粧タグ。王政・ファランヘ等では別化粧タグか既存名で処理するかを実装時に決める。
- 傀儡 `CEU`・`PML`、PML の化粧タグ `PML_esp`。
- 開幕 OOB・艦隊・航空 OOB の名前と編成。
- `nc_ESP`「スペイン・クローネ」の表示。
- 本土諸州の `ESP`/`FRA` 共存コア、リスボンの `PAL`/`ESP` 共存コア。
- `autonomy_ibrgovernate` と `is_iberian_nation` の現行定義。ESP を対象に含めるかは別タスクで判断し、ここでは書き換えない。
- `PRT` のギアナ領有とコア。

要調査の残件：州488・489・971 の `add_core_of` 有無（実装前に確認する）、PRT と接する州境界の実プロビンス、ブイサ・ロペス・コントレラスの肖像有無、メキシコ・米国タグの命名。
