# スペイン（カリブ亡命）シナリオ案

タグは `ESP`。1936年1月1日開始。国家方針樹、企業、設計局、国民精神、登録キャラクターは未作成である。この案は既存の領有、傀儡関係、MODシステムに合わせた導入案である。

## 地図

本土は失われている。ESP が保持するのはカリブ海および南米ベネズエラ沿岸の五州に限られる。

首都は州307（Venezuela、ファイル注記 Miranda）。人口約133万、石油41・石炭20を産出し、民需5・軍需1、航空基地2、海軍基地5（3＋2）、VP5を擁する。州変数 `gold_mine = 1` が付く。残る保有州は、内陸放牧地の州488（Bolivar、人口約14.6万）、石油35・石炭18と民需2、海軍基地5を持つ都市州489（Monagas、人口約158万）、沖合の島嶼で石油35・石炭18、燃料庫、海軍基地1、沿岸要塞2を備える州695（Curacao、人口約7.6万、VP1）、そして内陸放牧地の州971（Bolivar、人口約10万）である。

地中海側には二つの飛び地傀儡を維持している。ジブラルタル海峡南岸の `CEU`（セウタ、州1101、人口1811、海軍基地3、航空基地1、VP5）と、`PML`（メリリャ、州1098、人口7.4万、海軍基地3、航空基地3、VP2、化粧タグ `PML_esp`）である。いずれもアフリカ北岸に残された旧帝国の爪痕である。

イベリア半島本土はすべて `FRA` の所有である。マドリード（州41）をはじめとする半島各州には `FRA` と `ESP` の両方のコアが既に付与されており、ESP は「コアを持ちながら領土を追われた亡命政権」の立場にある。ただしバレアレス（州177）とカナリア（州178）の二州だけは `FRA` 単独コアであり、ESP コアを持たない。リスボン（州112）は `PAL` 所有下で `PAL`・`ESP` の二重コア、ピレネー山中のアンドラ（州925）は `ADR`・`ESP`・`FRA` の三重コアである。

カリブ沿岸の隣接勢力としては、ギアナ諸州（309・310・687・972）を領有する `PRT`（ポルトガル）があり、ボリバルおよびモナガスと陸上で接している。PRT の首都はアゾレス（州698）に置かれ、ポルトガル本土は `PAL` が治める。新大陸北岸において ESP・PRT・PAL の複雑な力学が交錯する。

## 開幕

正式名称は「スペイン」、化粧タグは `ESP_republic`（スペイン共和国）。通貨トークンは `nc_ESP`、表示単位はスペイン・クローネ（kr）である。政権は民主主義（`democratic_ideology`）から始まり、最終選挙は1933年2月、選挙周期は36か月に設定されている。登録キャラクターの定義ファイルは存在せず、指導者、閣僚、将軍はすべて新設が必要である。

軍事は `ESP_1936` に基づき、歩兵を基幹とする18個師団を新大陸に展開する。Man the Guns 環境下では軽巡 Libertad、駆逐艦4隻、潜水艦2隻からなる亡命艦隊（`ESP_1936_naval`、母港プロビンス1944）を保有し、By Blood Alone 環境下では航空部隊（`ESP_1936_air`）も備える。本国を失いながらも一定の艦隊戦力を保っている点が特徴である。輸送船150隻、初期安定度は0.5。

## 政治

本土を失った亡命政権として、政治路線は「どの正統性を掲げてスペインの再建を期すか」という一点を軸に深く分岐させる。各ルートは4〜7段の規模を基本とする。

亡命政府の首脳陣は、1936年時点で史実の位置付けが整合する人物に絞る。共和国派では大統領経験者のニセト・アルカラ＝サモラやマヌエル・アサーニャ、指導層のインダレシオ・プリエト、ラルゴ・カバリェロ、フアン・ネグリン、ディエゴ・マルティネス・バリオらを亡命政権の中枢に据える。王党派はローマに滞在中のアルフォンソ十三世とフアン・デ・ボルボン、カルリスタはマヌエル・ファル・コンデとハビエル・デ・ボルボン＝パルマを擁立候補とする。獄中にあるファランヘのホセ・アントニオ・プリモ・デ・リベラは消息不明枠または後継者体制として扱い、共産党はドローレス・イバルリとホセ・ディアス、軍司令官にはホセ・ミアハ、ビセンテ・ロホ、艦隊司令官ミゲル・ブイサを配置する。

新大陸の現地側としては、ベネズエラ大統領エレアサール・ロペス・コントレラスと陸海軍相イサイアス・メディナ・アンガリータを宿主側の権力者として位置付ける。さらに亡命地に身を寄せるカタルーニャのリュイス・コンパニス、バスクのホセ・アントニオ・アギーレ、ガリシアのカステラオら地方自治派が各分岐で発言力を持つ。

共和国再編。亡命憲章を堅持し、アサーニャを擁して法的な正統性を保つ道である。プリエトの穏健路線で連立をまとめ、在外選挙を実施して正統性を固める。化粧タグは `ESP_republic` を維持する。

王政復古。旧国王アルフォンソ十三世あるいはフアン王子を迎え、君主制の復活を図る。カルリスタ派との合意によって二重の王統を統合するか、正統派ボルボン家の一本化を貫くかを選択する。

ファランヘ。新大陸の地で「イスパニダー」の理念を掲げ、国民シンジカリズムを現地の労働者層へ浸透させる急進路線である。本土奪還に先んじてカリブ海に新たな国家体制を打ち立てる。

人民戦線・共産。イバルリとディアスを中心に亡命民兵を組織し、メキシコ等との連帯を通じて物資と兵力を確保する。

カリブ連邦・「地図上のスペイン」。半島奪還を断念し、新世界に永住の基盤を築く選択肢である。ロペス・コントレラスとの協定を結んでミランダ周辺の統治権を確立し、アンティル諸島を取り込んだ連邦結成へ進む。欧州帰還の方針を恒久的に封鎖し、国名を「地図上のスペイン」へと改称する。領有権主張や飛び地傀儡は維持されるものの、欧州国家としてのスペインは地図上から消滅する。

## 固有メカニクス：帰還の四証

NTS の「机」とは別の軸として、ESP では**四つの証**を数える。国変数 `ESP_proof_fleet`・`ESP_proof_bridgehead`・`ESP_proof_legitimacy`・`ESP_proof_recognition`（各0〜3）に、方針と決定で段を積む。復帰列の終盤は、艦隊の証（亡命艦隊を大西洋横断できるまで仕立てる）、橋頭堡の証（CEU/PML を要塞化し内側から使える状態にする）、正統の証（選んだ政権が国内に受け入れられる名を持つ）、承認の証（列強の黙認か支援を得る）の四点を同時に満たすことを要求する。どれか一つでも欠けると上陸方針は選べない、という門番にする。実装は4変数＋方針の `available` で足り、GUI は要らない。

## 産業

**オリノコの油。** 州489と695の油は既に35ずつある。精製側をキュラソーに寄せる設計にし、史実のキュラソー製油所（1918年操業のイスラ製油所、原油はベネズエラ産）を史実の核に据える。艦隊の燃料証にも直結させる。

**亡命造船。** 海軍基地5のモナガスを母港に、亡命艦隊の改修と新造を回す。工場数は小さいので、造船所建設の即時報酬より既存設備の拡張方向にする。

**亡命知識人。** スペイン語の大学・印刷・医学をカラカスに移す列。文明度と研究速度を小さく足し、「国は地図にないが蔵書はある」説明にする。

**ボリバルの金。** 州307の `gold_mine` 変数は既にあるので、`nc_ESP` の担保として説明だけ付け、産出イベントは小さく。

**対仏産業。** 油と仏製機械のバーター／キュラソー合弁は友好側、禁輸と軍需転換は敵対側。`ESP_FRA_rapport` の産業層として方針樹の対仏枝に載せる。

## 軍事

**亡命艦隊。** 軽巡1・駆逐4・潜水2が現存する。ブイサを旗頭に据え、キュラソーとモナガスを二母港にする。艦隊の証はこの列を通る。

**上陸ドクトリン。** 目的地は地中海である。海兵・上陸・上陸用装備の研究ボーナスを積み、陸軍の量は増やさない方向。

**外人部隊の残党。** スペイン外人部隊は史実でモロッコ側の兵である。CEU/PML が傀儡で残っている以上、部隊の名を傀儡側に残し、宗主が師団テンプレとして受け取る枝を置く。

**セウタ要塞。** 傀儡州の要塞化は宗主側の建設か傀儡方針で扱い、橋頭堡の証を上げる。

**航空。** 開幕の `ESP_1936_air` を前提に、カリブ哨戒と本土往還を分ける小さい列に留める。

**対仏軍事。** カリブ共同哨戒とセウタ海峡共同管理は友好側、対潜競争と橋頭堡牽制は敵対側。上陸ドクトリン自体は友好でも共有しない。

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

## 固有メカニクス：大西洋の関係（対 FRA）

ESP と FRA の関係は、復帰戦争の有無だけでは足りない。**仲良くするか、冷ややかに共存するか、敵にするか**を、外交・軍事・産業の三層で同じ変数に載せる。

国変数 `ESP_FRA_rapport`（-100〜+100、開幕 0）。正は和解・提携、負は敵対・報復。FRA 側は同一値を `FRA` の国変数として同期するか、`set_variable` で相手国へ写す（実装時に片側正本を決める）。閾値の目安は +60（友好確定）、0付近（冷たい共存）、-60（敵対確定）。

三層の中身:

| 層 | 友好側（rapport 高） | 敵対側（rapport 低） |
| --- | --- | --- |
| 外交 | 亡命政権の黙認、領事交換、イベリア自治憲章の共同署名、承認の証を平和で満たす | 大使館閉鎖相当の事件、諜報妨害、最後通牒、承認の証を戦争で満たす |
| 軍事 | カリブ共同哨戒、セウタ海峡の共同管理、演習・顧問交換、上陸ドクトリンの共有はしないが沿岸警備は協調 | 対潜競争、橋頭堡への牽制配備、カリブ遠征への備え、復帰戦争の門番を開く |
| 産業 | オリノコ油と仏製機械のバーター、キュラソー精製の合弁、クローネ／フラン決済枠、研究ライセンス | 禁輸・拿捕事件、軍需転換、独自製油の強制、燃料を艦隊だけに回す |

友好確定でも本土コアは消さない。平和末端は「FRA がイベリアに自治枠を残し、ESP が帰還戦争を封じる」か「飛び地とカリブだけをスペイン領として承認する」の二本。敵対確定は既存の復帰列へ接続する。カリブ連邦末端を取った場合、友好側は「地図上のスペイン」として FRA と通商条約だけ結び、敵対側はカリブ防衛戦争に振る。

FRA 側の同名列（`FRA_spain_question` 系）と **相互に相手の選択を見る**。片方だけ友好を取っても相手が敵対なら rapport は中央へ引き戻す事件を挟む。

## アンドラ（ADR）

州925は `FRA` 所有、`wasteland`、人的1532、インフラ1、資源なし。コアは `ADR`・`ESP`・`FRA` の三重。開幕に独立国家としての `ADR` は存在せず、化粧タグ `ADR_co-principality`（共治公国）と司教系キャラクター（`ADR_Justi_Guitart_i_Vilardebo`、`ADR_Ramon_Iglesias_i_Navarri`）だけが定義されている。史実の共治（フランス元首＋ウルヘル司教）を、この世界線では「イベリアを持つフランス」と「コアだけ残した亡命スペイン」の接点に読み替える。

アンドラは領土としては取るに足りないが、`ESP_FRA_rapport` の測り棒である。友好側では共治公国を緩衝として立て、敵対側ではピレネーの監視砦にし、中立では三重コアのまま放置する。既存の `ESP_andorra_post` は連絡所に留めず、専用列へ拡張する。領有変更は方針・事件の結果でのみ行い、開幕配置は動かさない。

**共治復活。** rapport が高友好のとき、FRA 同意イベントを経て州925を `ADR` として解放する。従属はどちらにも付けず、双方から保証される中立小国（または形式上の共治）にする。コアは三重のまま残す。化粧タグ `ADR_co-principality` をそのまま使う。

**ウルヘルの席。** ESP は亡命政権として司教側共治者の名を借り、正統の証を小さく足す。キャラクターは既存 ADR 定義を `recruit` するだけで足り、新規肖像は要らない。

**ピレネーの釘。** rapport が敵対のとき、アンドラを要塞・諜報拠点化し、橋頭堡の証の補助にする。州カテゴリや資源は増やさず、要塞とレーダー程度に留める。復帰列のピレネー連絡と接続する。

## 外交

- `FRA`：**大西洋の関係**列が本筋。承認の証は (1) 友好で FRA が亡命政権を認める、(2) 冷たい共存で列強の黙認だけ取る、(3) 敵対で戦争、の三択。平和ルート（飛び地自治での引き渡し／共同憲章／共治アンドラ）は友好末端に置く。
- `ADR`：上記アンドラ列。タグ解放は友好末端のみ。敵対時は州925を FRA 領のまま要塞化するだけ。
- `PAL`：リスボンの ESP コアが外交火種になる。リスボン問題の方針で PAL と敵対するか、イベリア回収の際にコアを棚上げするかを選ばせる。友好対 FRA を取っている場合、PAL 交渉は FRA 保証の枠内に縛る。
- `PRT`：ギアナ国境だけが接する小国同士。国境確定・貿易・アゾレス寄港の小列に留め、PRT のコアは触らない。
- `USA`・`MEX`：史実の亡命先はメキシコだった。メキシコ列を承認と物資の供給元として使う。タグの実在は実装時に確認する。
- `CEU`・`PML`：傀儡のまま残すか、橋頭堡列で吸収して直接要塞州にするかを分岐にする。吸収は傀儡解消（annex）＋州コア取得で処理し、タグ自体は残す案。友好対 FRA 時は海峡共同管理で傀儡を残しやすい。

## 方針樹

接頭辞は `ESP_`。幹を中央、政治の複数列を左、産業・軍事を右、対仏・アンドラ・復帰を下部に置く。合計 **約110本** の長ルート設計で、効果の方向のみ固定する。

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

### 産業列（11本）＋対仏産業枝（4本）

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
| `ESP_orinoco_for_machine` | `ESP_fra_handshake` | `ESP_oil_embargo_fra` | 対仏バーター。油⇔機械。rapport+、民需方向 |
| `ESP_curacao_joint_refine` | `ESP_orinoco_for_machine` | — | キュラソー合弁精製。燃料共有、rapport+ |
| `ESP_oil_embargo_fra` | `ESP_fra_cold_war` | `ESP_orinoco_for_machine` | 対仏禁輸。燃料を自艦隊へ、rapport- |
| `ESP_war_refinery` | `ESP_oil_embargo_fra` | — | 軍需転換製油。艦隊の証+1、消費財悪化 |

### 軍事列（14本）＋対仏軍事枝（4本）

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
| `ESP_joint_caribbean_patrol` | `ESP_fra_handshake` | `ESP_anti_fra_asw` | カリブ共同哨戒。海軍経験、rapport+ |
| `ESP_strait_condominium` | `ESP_joint_caribbean_patrol` | — | セウタ海峡共同管理。橋頭堡の証を平和版で+1 |
| `ESP_anti_fra_asw` | `ESP_fra_cold_war` | `ESP_joint_caribbean_patrol` | 対仏対潜競争。rapport-、潜水研究 |
| `ESP_bridgehead_deterrence` | `ESP_anti_fra_asw` | — | 橋頭堡牽制配備。復帰列の軍前提を早める |

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

### 外交列（5本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_league_petition` | `ESP_four_proofs` | — | 国際連盟への訴え。承認の証+1 |
| `ESP_mexican_hand` | `ESP_league_petition` | — | メキシコ供給線 |
| `ESP_washington_briefing` | `ESP_mexican_hand` | — | 米国説得 |
| `ESP_guiana_border` | `ESP_four_proofs` | — | PRT とのギアナ国境確定 |
| `ESP_caribbean_recognition` | `ESP_washington_briefing` | — | 米州承認。承認の証+1 |

### 対仏関係列（8本）

旧 `ESP_fra_containment` / `ESP_fra_approach` の二本を拡張する。産業・軍事の対仏枝はここの分岐を前提にする。

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_atlantic_temperature` | `ESP_four_proofs` | — | 温度の説明。`ESP_FRA_rapport` 初期化 |
| `ESP_fra_handshake` | `ESP_atlantic_temperature` | `ESP_fra_cold_war` | 対仏握手。rapport+、領事事件 |
| `ESP_fra_cold_war` | `ESP_atlantic_temperature` | `ESP_fra_handshake` | 冷たい共存〜敵対の入口。rapport-、諜報 |
| `ESP_paris_consulate` | `ESP_fra_handshake` | — | パリ領事。承認の証+1（平和版） |
| `ESP_iberian_joint_charter` | `ESP_paris_consulate` | — | イベリア共同憲章。友好確定、復帰戦争を封じる選択 |
| `ESP_caracas_ultimatum` | `ESP_fra_cold_war` | — | カラカス最後通牒。rapport大減 |
| `ESP_recognition_by_war` | `ESP_caracas_ultimatum` | — | 戦争で承認の証を満たす門。復帰列へ接続 |
| `ESP_atlantic_entente` | `ESP_iberian_joint_charter` かつ産業・軍事友好枝の末端 | — | 大西洋協商。通商・哨戒・アンドラ共治の前提 |

### アンドラ列（7本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_andorra_post` | `ESP_pyrenees_line` or `ESP_atlantic_temperature` | — | アンドラ連絡所。三重コアの説明 |
| `ESP_urgell_seat` | `ESP_andorra_post` | — | ウルヘルの席。司教側共治の名。正統の証+1 |
| `ESP_coprincipality_talks` | `ESP_urgell_seat` かつ `ESP_fra_handshake` | `ESP_andorra_nail` | 共治交渉。FRA 同意事件、rapport+ |
| `ESP_restore_adr` | `ESP_coprincipality_talks` | — | 州925を `ADR` 解放、`ADR_co-principality`、双方保証 |
| `ESP_andorra_nail` | `ESP_urgell_seat` かつ `ESP_fra_cold_war` | `ESP_coprincipality_talks` | ピレネーの釘。要塞・諜報、rapport- |
| `ESP_pyrenees_listening` | `ESP_andorra_nail` | — | 傍受網。橋頭堡の証補助、復帰列と接続 |
| `ESP_valley_market` | `ESP_restore_adr` or（中立のまま `ESP_andorra_post`） | — | 渓谷市場。小さな通商・消費財。ADR 非解放でも可 |

### 復帰列（11本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `ESP_reconquista_plan` | `ESP_generalstaff_return` | `ESP_map_spain` | レコンキスタ計画。四証を要求する門 |
| `ESP_maquis_network` | `ESP_reconquista_plan` | — | 本土地下組織。抵抗支援 |
| `ESP_pyrenees_line` | `ESP_maquis_network` | — | ピレネー越えの連絡線。アンドラ列の入口 |
| `ESP_iberian_uprising` | `ESP_pyrenees_line` | — | イベリア蜂起イベント |
| `ESP_balearic_stepping` | `ESP_iberian_uprising` | — | バレアレス主張。州177へ ESP コア追加案 |
| `ESP_canary_anchor` | `ESP_balearic_stepping` | — | カナリア中継。州178へ ESP コア追加案 |
| `ESP_lisbon_question` | `ESP_iberian_uprising` | — | リスボンの ESP コアの扱い。PAL との交渉か併呑 |
| `ESP_french_gate` | `ESP_lisbon_question` | — | FRA への最後通牒 or 交渉。rapport を参照 |
| `ESP_operation_return` | 四証すべて閾値以上 | `ESP_map_spain`, `ESP_iberian_joint_charter` | 帰還作戦。FRA への戦争目標 |
| `ESP_madrid_or_nothing` | `ESP_operation_return` | — | マドリード奪還後の再建。本土州への統治効果 |
| `ESP_iberia_restored` | `ESP_madrid_or_nothing` | — | 終端。イベリア再統合と国民精神の更新 |

合計: 6+6+7+6+6+6+15+18+7+5+8+7+11 = **約108本**。実装時に90本前後へ削ってもよいが、対仏三層・アンドラ列・復帰列の末端は切らない。

## 国境・復帰計画

この計画が通るまで州は動かさない。

- 本土各州の `ESP` コアは既に付いているので追加しない。動くのは州177・178への ESP コア追加（`ESP_balearic_stepping`・`ESP_canary_anchor`）だけである。
- リスボン（州112）は `PAL`・`ESP` 二重コアのまま維持し、`ESP_lisbon_question` で PAL との交渉事件にする。PAL のコアを消さない。
- アンドラ（州925）は開幕 `FRA` 所有のまま。`ESP_restore_adr` でのみ `ADR` を解放する。三重コアは消さない。敵対ルートでは領有を動かさず要塞化するだけ。
- CEU/PML は傀儡のままか吸収かを分岐にし、いずれの場合も州1101・1098 の `CEU`/`PML` コアは残す。
- マドリードを含む全本土州の `FRA` コアは残す。ESP のコアと FRA のコアが共存する状態が前提の世界線である。
- 復帰戦争の戦争目標は `ESP_operation_return` で発行し、占領後のコア化は和平結果に置く。開幕に州を動かさない。友好確定（`ESP_iberian_joint_charter`）を取った場合はこの戦争目標を封じる。

## 実装時に残すもの

- 州307・488・489・695・971 の所有とコア、資源値、`gold_mine` 変数。
- `ESP_republic` 化粧タグ。王政・ファランヘ等では別化粧タグか既存名で処理するかを実装時に決める。
- 傀儡 `CEU`・`PML`、PML の化粧タグ `PML_esp`。
- 開幕 OOB・艦隊・航空 OOB の名前と編成。
- `nc_ESP`「スペイン・クローネ」の表示。
- 本土諸州の `ESP`/`FRA` 共存コア、リスボンの `PAL`/`ESP` 共存コア、州925の `ADR`/`ESP`/`FRA` 三重コア。
- `ADR` の化粧タグ `ADR_co-principality` と既存キャラクター定義。国史ファイルは解放時にのみ動かす。
- `autonomy_ibrgovernate` と `is_iberian_nation` の現行定義。ESP を対象に含めるかは別タスクで判断し、ここでは書き換えない。
- `PRT` のギアナ領有とコア。

要調査の残件：州488・489・971 の `add_core_of` 有無（実装前に確認する）、PRT と接する州境界の実プロビンス、ブイサ・ロペス・コントレラスの肖像有無、メキシコ・米国タグの命名、ADR 解放時の OOB（Default_oob）の差し替え要否。
