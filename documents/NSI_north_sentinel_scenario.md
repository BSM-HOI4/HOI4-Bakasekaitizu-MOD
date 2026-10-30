# 北センチネル島シナリオ案

タグは `NSI`。1936年1月1日開始。既存の国家方針樹（幹 `NSI_Sinkou` 起点、約42本＋共有8本）、国民精神、開幕アイデアはすでに実装済みである。この文書は樹の作り直しではなく、既存を残したまま足りない枝を追記する案である。新規IDは既存と衝突させない。

## 地図

領有は州943だけである。北センチネル島は州カテゴリ `small_island`、manpower 9999、資源は油1・鋼1・ゴム3・石炭2、インフラ1、民需工場1。州変数 `gold_mine = 1` が付いている。コアは `NSI` と `IND` の二重である。インドのコアは史実の行政管轄（アンダマン・ニコバル行政区）の名残として読み、消さない方向で扱う。

州733（アンダマン）は `GMI` の所有とコアで、manpower 29500、インフラ2、プロビンス12251に海軍基地2がある。`GMI` はファイル名こそ Guam だが実体はアンダマンの「グアム皇国」（化粧タグ `GMI_imperial_state`）であり、NSI に `autonomy_psonal_union` で従属している。ポートブレア側の海軍基地は、隔離国家が持つ唯一の近代港湾である。

海の外は `IND`（コア保持）、`RAJ` 系の隣接海域、東にビルマ方面がある。外来船の絵面を書くときの「北の大きな国」は実装上 `RAJ` 系タグを想定するが、タグの実在は実装時に周辺ファイルで確認する。

## 開幕

正式名称は「北センチネル島」。化粧タグは持たない。通貨トークンは `nc_NSI` で、表示は北センチネル島・テンゲ（T）。政権は `political_set_0` により `mythologicalism` で始まり、人気は mythologicalism 100 の一色である。指導者は `NSI_Zokutyo`（族長、サブイデオロギー `animism`）。開幕アイデアは `animism` のほか、初期アイデアとして `nsi_ancient_isolation`（宣戦不可・陣営不可・防御寄り）、`nsi_primitive_society`（産業・研究ペナルティ）、`nsi_tribal_unity`（安定・ドリフト耐性）が想定される構成である。

軍事は `NSI_1936` で、部族戦士テンプレ「NSI Tribal Warriors」の衛隊2個と、砲兵支援付きの「NSI Elite Guard」1個、計3個師団。艦隊は持たない。OOBのコメントにも「港湾を持たない未開の孤立部族のため開始海軍なし」とある。ただし国史では `navy_tech_level_1` と、Man the Guns 時の初期潜水艦・初期軽船体・基本魚雷・輸送船を取得済みである。「船を知っているが作る場所がない」状態が開幕である。

## 政治

政治分岐は既存の `NSI_tribal_council` → `NSI_elder_wisdom` → `NSI_isolation_laws` の一本道と、信仰側の覚醒系に留まる。追加するのはイデオロギーの切替ではなく、「外界をどこまで認めるか」の座標である。

**掟の三方向。** 追加分岐は、完全拒絶（外来船は岸辺の砲と槍で追い返す）、条件付き観測（船は沈めるが漂着物は拾う）、選別的接触（GMI経由で外の言葉だけ入れる）の三つに絞る。いずれも mythologicalism のまま動かし、民主・共産・ファシズムへの転向ルートは置かない。島に政党は生えない、という前提である。

**GMI の位置。** グアム皇国は `democratic_ideology` 50・`fascism_ideology` 36 のまま従属している。宗主の神話国家と臣下の「皇国」が同じ枠にいる歪さは、そのまま題材にする。統合するなら島の名を冠した自治に解き、分離するなら港湾だけを共有したまま独立寄りにする。

**インドのコア。** 州943の `IND` コアは、外界が島に主張を持つ唯一の根拠である。拒絶側を進むと `IND` との外交事件が増え、接触側を進むとコアの取り下げ交渉が一つの出口になる。

### 潮位（固有メカニクス案）

「机」や「点数」の代わりに、島では**潮位**を数える。国変数 `NSI_tide_gauge`（0〜10）を「外界が島に寄せる圧力」として使う。外来船事件が起きるたび潮位は上がり、撃退・拒絶の選択を取ると下がる。潮位の低い側は既存の孤立バフが強く残り研究が遅いまま、高い側は漂着技術・港湾・GMI統合の枝が開く。どちらの端も罰ではなく、どの高さで釣り合わせるかを樹の軸にする。変数と発火はMTTH小の国事件チェーンに載せ、頻繁な `any_state` スキャンは置かない。

## 産業

島の産業は既存の地下都市列（`NSI_chikatoshi` 系）が幹で、追加分は「海が運ぶもの」側に置く。

**漂着製鉄。** 沈没船の鉄を浜で鍛える小さい列。民需よりも修繕と小銃の補修を増やす方向。`nsi_primitive_society` の産業ペナルティを全部は消さず、一部だけ相殺する。

**ゴムと貝。** 州943のゴム3を「採れるが出せない」資源として扱い、通商に回すか地下都市の材料に回すかを分岐にする。

**アンダマンの港。** GMI 側の海軍基地2を宗主として使う根拠を作る枝。統合側では埠頭と造船、分離側では寄港料として `nc_NSI` の獲得に繋げる。

**地下都市MIO。** `chikatoshi` の建設バフは既存アイデアのまま残し、後述の設計局へ橋渡しする枝だけ足す。

## 軍事

既存は陸の防御・衛隊・古代兵器で閉じており、海は白紙である。追加候補は三つ。

**沿岸魚雷艇。** 取得済みの `basic_torpedo`・初期軽船体を生かし、「島の外へ出ない海軍」として小型艇だけを許す列。艦種を護衛・輸送・小型攻撃艇に限定する国民精神で縛る。母港は GMI 統合前なら事件で借りる形、統合後なら州733を直接使う。

**浜の哨戒。** 外来船撃退事件と連動し、沿岸防衛と哨戒の経験を陸軍経験か海軍経験へ振り分ける。撃退を選び続けると海軍経験は貯まるが艦がいない、という状態をそのまま許す。

**覚醒後の外海。** 既存の覚醒列（`NSI_awakening_wrath` 以降）は `annex_everything` の戦争目標まで行く。その直前に、ベンガル湾の出口としてアンダマンを基点にする一段を足す案。

## 企業

`common/ideas` の designer として置く。島に「会社」はないので、名前は外界から見た呼称か部族内の役職名にする。数値方向のみ固定。

| ID | 種別 | 史実・設定の核 | 解禁 | 効果の方向 |
| --- | --- | --- | --- | --- |
| `NSI_beach_smiths` | industrial_concern | 沈没船の鉄を鍛える浜の鍛冶 | 漂着製鉄の方針 | 歩兵装備産出、建設速度を微増 |
| `NSI_coral_masons` | industrial_concern | 地下都市の石材調達 | `NSI_underground_expansion` | 建設速度、要塞建設 |
| `NSI_andaman_harbor` | industrial_concern | 州733の海軍基地（GMI側） | GMI統合か寄港の方針 | 造船所建設、輸送船産出 |
| `NSI_shell_coiners` | industrial_concern | 貝と布の交換所（テンゲの実体がない説明） | 開幕から | 消費財を微減、通商収入 |
| `NSI_tide_watchers` | materiel_manufacturer | 潮位を読む役職。観測器材は拾い物 | 条件付き観測の方針 | 偵察・支援装備の研究 |

開幕から見せるのは `NSI_shell_coiners` と `NSI_beach_smiths` の二つに留め、残りは方針の報酬で `available` を開く。

## 設計局

島には設計局の実体がない。MIOは「浜の修理場」と「地下の炉」から始め、艦艇局はGMI絡みでのみ出す。ファイルは `common/military_industrial_organization/organizations/NSI_organization.txt` を新設する案。

**浜の修理場** `NSI_beach_yard_organization`

- 装備は歩兵火器と支援装備。
- 初期特性「拾い物の口径」：信頼性を少し下げ、生産コストを下げる。
- 特性「鍛え直した舶来鉄」は漂着製鉄の方針で開く。
- 解禁は `NSI_hidden_arsenals` の後。

**地下の炉** `NSI_deep_forge_organization`

- 装備は歩兵火器・砲。
- 初期特性「換気の穴が少ない」：生産コストを下げ、信頼性を微減。
- 特性「地熱の炉」は `NSI_underground_forges` の後に開く。
- 解禁は `NSI_chikatoshi` 系の終盤。

**アンダマン船渠** `NSI_andaman_yard_organization`

- 装備は軽船体・魚雷艇・輸送船に限定。
- 初期特性「借りた港」：航続距離を上げ、攻撃を下げる。
- 解禁は GMI 統合方針、または寄港協定の維持選択。

## 国民精神

カテゴリは `country`。数値は実装時に調整し、方向だけ固定する。既存精神はすべて残す。

**潮の重さ** `NSI_tide_weight`（開幕から、案）

- `NSI_tide_gauge` が低いほど安定と防御に微増、研究に微減。動的 modifier の実装可否は変数範囲と既存実装を照合して決める。難しければ段階別の静的ideaに切り分ける。

**借りた港** `NSI_borrowed_harbor`（GMI方針）

- 艦艇研究の小さな加算、GMIへの従属度圧力を説明する文面。統合側では消滅し、分離側では残る。

**拾い物の暦** `NSI_wreck_calendar`（漂着列）

- 研究速度に微増、隔離系アイデアの効果を一部相殺する方向。「漂着物がなければ外の技術は増えない」を説明にする。

**浜に火を** `NSI_beach_fires`（完全拒絶側）

- 沿岸防御・敵性上陸への防御側ボーナス、外交受諾の悪化。`nsi_isolation_policy` と重ねる方向。

**アンダマンの二つの名** `NSI_two_islands`（GMI列）

- 従属国からの資源・人力吸い上げか、統合後の州コア化準備かを、統合/分離で効果を振り分ける。

## このMODの国家idea

**文明度（Cultural_Degree）。** 開幕値は低いまま据え、潮位の高い側に進んだときだけ `base_Cultural_Degree` を小さく足す。拒絶側では上げない。「外の言葉が入ると暦が進む」説明に留める。

**国家統合力（National_Unity）。** 既存の `nsi_tribal_unity`・`nsi_isolation_laws` が安定とドリフト耐性を担っているため、追加分では `daily_National_Unity_Power_gain` には直接触れず、GMI 統合時に一度だけ係数を足す程度に抑える。

**統一通貨。** `nc_NSI` の表示名「テンゲ」は変えない。島内が物々交換のままなので、獲得係数は `NSI_shell_coiners` 側で小幅に足し、外界と取引しない限り実体のない通貨である、という説明を説明文で処理する。

**宗教。** 開幕アイデア `animism` をそのまま使い、宗教法を新設しない。信仰列は既存の覚醒系が担当しているため、追加側で宗教関連の枝は増やさない。

## 方針樹

接頭辞は `NSI_`。既存樹の配置（Sinkou 起点、左に軍事・地下都市、中央に政治・孤立、右に民需・信仰、下部に覚醒）は維持し、追加分は空いている右下〜下部へ枝を増やす。共有フォーカス（HRE系・sf系8本）と既存42本はそのまま残す。追加分は約20本の中規模。

### 潮位の幹（新規・3本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `NSI_strange_sails` | `NSI_Sinkou` | — | 外来船事件チェーンを起動し `NSI_tide_gauge` を初期化 |
| `NSI_read_the_tide` | `NSI_strange_sails` | — | 潮位の説明イベント。以降の三方向分岐を開く |
| `NSI_weigh_the_beach` | 三方向のいずれか一本 | — | 潮位を現在値で固定し、対応する精神を確定させる |

### 外界接触（新規・6本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `NSI_repel_the_sails` | `NSI_read_the_tide` | `NSI_salvage_gospel` | 完全拒絶。撃退事件の頻度増、`NSI_beach_fires` |
| `NSI_salvage_gospel` | `NSI_read_the_tide` | `NSI_repel_the_sails` | 条件付き観測。`NSI_wreck_calendar`、漂着技術ボーナス |
| `NSI_words_from_the_water` | `NSI_salvage_gospel` | — | 選別的接触。翻訳事件、外交受諾の微増 |
| `NSI_raj_survey_ship` | 潮位が中間以上 | — | RAJ側測量船の来航事件。拒否すれば潮位低下、許せば上昇 |
| `NSI_indian_claim` | `NSI_raj_survey_ship` | — | `IND` コアの扱いを交渉事件にする。取り下げか決裂 |
| `NSI_burma_tide` | `NSI_indian_claim` | — | ビルマ方面の漂着先事件。海の出口の説明 |

### GMI・アンダマン（新規・5本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `NSI_andaman_question` | `NSI_tribal_council` | — | GMI の位置づけを問う。従属維持の説明 |
| `NSI_one_realm` | `NSI_andaman_question` | `NSI_two_flags` | GMI 統合。annex して州733へコア、`NSI_two_islands` |
| `NSI_two_flags` | `NSI_andaman_question` | `NSI_one_realm` | 自治の維持。港湾寄港権と `NSI_borrowed_harbor` |
| `NSI_port_blair_yard` | `NSI_one_realm` or `NSI_two_flags` | — | `NSI_andaman_harbor`・`NSI_andaman_yard` 解禁 |
| `NSI_imperial_court` | `NSI_one_realm` | — | グアム皇国の名を島の宮廷位に取り込む化粧的事件 |

### 海と船（新規・4本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `NSI_reef_flotilla` | `NSI_port_blair_yard` | — | 魚雷艇・軽船体の研究ボーナス、小型艇限定精神 |
| `NSI_tide_riders` | `NSI_reef_flotilla` | — | 初の艇隊OOB（小型艇数隻）を配備 |
| `NSI_sunken_dock` | `NSI_underground_expansion` | — | 地下都市側の船渠。州943へ造船所建設 |
| `NSI_first_horizon` | `NSI_tide_riders` か `NSI_sunken_dock` | — | ベンガル湾出口の説明。覚醒列への橋渡し |

### 文明・統合の配線（新規・3本）

| ID | 前提 | 排他 | 効果の方向 |
| --- | --- | --- | --- |
| `NSI_grove_census` | `NSI_elder_wisdom` | — | National_Unity 周りの一回加算と人口の説明 |
| `NSI_calendar_of_wrecks` | `NSI_words_from_the_water` | — | `base_Cultural_Degree` の小幅上昇 |
| `NSI_bengal_reach` | `NSI_awakening_wrath` 完了後 | — | 覚醒後の外海方針。アンダマン基地の強化 |

## 実装時に残すもの

- 既存の全42本の方針と効果、8本の共有フォーカス。位置も原則そのまま。
- `nsi_ancient_isolation` の宣戦不可ルール。追加分岐はこのルールと矛盾しない範囲で書き、解除は既存の覚醒列に任せる。
- `GMI` 側のファイル名・化粧タグ・政党値。統合は NSI 側の効果として処理し、GMI の国史は書き換えない前提にする。
- 州943の `IND` コアと `gold_mine` 変数、manpower 9999 の架空値。
- `autonomy_psonal_union` の綴りは定義側idのまま使う。直さない。
- `nsi_events.1`・`nsi_events.2` の既存イベント名前空間。新規は同じ `nsi_events` に連番で足す。
- `nc_NSI` の表示「テンゲ」。
- NSI_1936 OOBの3師団と「開始海軍なし」の状態。海軍追加は方針の報酬として扱い、開幕OOBはいじらない。

実装時に要確認の点は、潮位を動的 modifier にするか段階ideaにするか、GMI 統合時の `IND` コア・自治レベル遷移、`nsi_ancient_isolation` の `can_not_declare_war` と覚醒列の `create_wargoal` が同時に成立する挙動の三点である。
