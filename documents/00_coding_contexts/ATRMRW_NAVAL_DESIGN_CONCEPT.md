# ATRMRW 海軍設計コンセプト

- 文書ID: `ATRMRW-NDC-001`
- バージョン: `1.0-static-prototype`
- 作成日: 2026-08-02
- 対象ブランチ: `feature/_system_ATRMRW_naval_design`
- 対象MOD: HOI4-Bakasekaitizu-MOD
- GUI実装対象: インストール済みHOI4 1.19.2
- 状態: コンセプト完遂、日本5艦級の静的プロトタイプ実装完了、実機検証はユーザー指示により未実施

## 1. 定義

ATRMRW（ATRM Rework）は、旧ATRM海軍設計の物理的・視覚的な艦船設計思想と、SSW/NVRWの史実データ・計算・装備分類思想を統合した、BSM向けの次世代海軍設計コンセプトである。

統合式は次のとおりとする。

```text
ATRMRW
  = ATRMの艦上配置・スロット数・燃料／機関設計
  + SSW/NVRWの史実クラス船体・装備分類・計算・検証
  + BSM世界観向けの架空技術・国家別設計自由度
```

ATRMRWはATRMまたはNVRWの単純移植ではない。ATRMを表示・配置・設計自由度の基盤、NVRWをデータ・計算・再現性の基盤として扱い、両者の責務を分離して統合する。

## 2. コード転用契約と出典管理

SSW側でユーザー本人が作成したコードは、ユーザーが保有する契約上の許諾に基づきATRMRWへ転用できる。

転用時は次の原則を守る。

1. SSWから転用したファイルまたはブロックは、移植台帳に元パス・元コミット・移植先・変更内容を記録する。
2. ユーザー本人が作成したコードと、バニラ・第三者・共同制作者由来のコードや画像を区別する。
3. 転用許諾はユーザー本人のコードに適用し、第三者資産の権利まで自動的に包含するものとして扱わない。
4. SSWのIDをそのまま使用する必要がない場合、ATRMRW側の名前空間へ移植して依存関係を切る。
5. SSWリポジトリを実行時依存先にせず、BSM内で独立して動作する形にする。

将来の移植台帳は次の形式を標準とする。

| 項目 | 内容 |
|---|---|
| Source repository | SSW_mod |
| Source branch/commit | 移植時に固定 |
| Source path | 元ファイルのパス |
| Ownership basis | ユーザー作成・転用許諾あり |
| Destination path | ATRMRW側のパス |
| Transformation | 改名・分割・計算変更・GUI接続など |
| Third-party dependency | なし／あり／要確認 |

## 3. 設計目標

### 3.1 必須目標

| ID | 目標 |
|---|---|
| G1 | ATRMの艦上配置型Equipment Designerを継承する |
| G2 | ATRMのスロット構成と最大数を継承し、大型艦から小型艦へ段階的に減る標準スロット数へ整理する |
| G3 | NVRWの史実艦級1:1船体と汎用船体を併存させる |
| G4 | NSDB・Navypedia・NavWeaps等の根拠から船体・砲・機関性能を算出する |
| G5 | 史実艦の搭載装備を省略せず、限られたスロット内で再現する |
| G6 | プレイヤーが艦上のどこへ何を載せたか視覚的に理解できるようにする |
| G7 | 架空艦・超技術・代替燃料をBSM世界観に合わせて拡張可能にする |
| G8 | 艦種・年代・船体規模に応じて搭載可能装備を制限する |
| G9 | 船体、モジュール、variant、OOB、GUIを機械検証可能にする |

### 3.2 非目標

- Phase 0監査段階では既存BSM船体・GUI・OOBを変更しない。承認後の日本5艦級プロトタイプ実装はこの制約の対象外とする。
- 旧ATRMブランチを直接マージしない。
- SSW/NVRWをリポジトリ単位でコピーしない。
- 戦車・航空機のEquipment Designerの表示・操作を海軍作業の副作用で変えない。
- 古いID、架空艦、コメントアウト定義を整理目的で削除しない。
- 史実データが不足している数値を独自判断で補完しない。

## 4. 継承元ごとの責務

### 4.1 ATRMから継承するもの

| 領域 | 継承内容 |
|---|---|
| GUI | `origin/future/Navy_rework`の艦影中心・前部／中央／後部配置思想。旧full-replaceファイル自体は1.12.7用で欠陥があるため実装母体にしない |
| スロット | 固定枠とカスタム枠を組み合わせた多数スロット構造 |
| スロット数 | 艦種・世代ごとの物理スロット総数 |
| 燃料 | 燃料・動力源を船体設計要素として選択する思想 |
| 機関 | 複数の機関位置と推進方式を設計へ反映する思想 |
| 艦型表現 | 艦首・中央・艦尾に対応した装備配置 |
| 画像 | 前後スロット、機関、燃料、レーダー、ソナー等の視覚カテゴリ |
| 自由設計 | 既成艦級の再現だけでなく架空設計を許す設計空間 |

ATRMの既存数値は参考値とし、そのままバランス値には採用しない。特に旧燃料モジュールの速度・信頼性・燃料消費等は、新しい計算体系で再算定する。

### 4.2 SSW/NVRWから継承するもの

| 領域 | 継承内容 |
|---|---|
| 船体 | 史実クラス単位の固有船体と汎用船体の二層構造 |
| 役割 | `ship_type_slot`に相当する艦種・任務ロール |
| 基本兵装 | 主・副・補助・軽兵装を意味論的に分類する6基本兵装枠 |
| 旧hidden装備 | 機関種別、機関出力、装甲、史実武装過多分の意味分類。ATRMRWでは全て可視枠へ変換する |
| ロック | 恒久ロックと解放可能ロックによる年代・艦型制限 |
| 砲分類 | 年代Tier×砲サイズClassの二軸分類 |
| 対空分類 | 物理占有量に基づくAA footprint band |
| データ | NSDB/Navypediaを中心とする艦級仕様と改装履歴 |
| 計算 | HPCLC、GUNCLC、排水量・航続距離・機関出力ベースの算定 |
| variant | 就役時状態と後年改装状態の分離 |
| 検証 | ID、category、allowlist、loc、GFX、variant/OOBの整合検査 |

### 4.3 ATRMRWで新設するもの

1. ATRM物理スロットをNVRW意味スロットへ割り当てるマッピング層。
2. 物理スロット総数を超えずに史実装備を保持する集約モジュール方式。
3. 艦上位置、装備用途、年代、砲塔占有量を同時に制約する搭載判定。
4. 史実設計モードと自由設計モードの共存。
5. 旧ATRM資産とSSWコードの転用元を追跡する移植台帳。

## 5. 中核アーキテクチャ

ATRMRWは次の4層に分離する。

```text
┌──────────────────────────────────────────────┐
│ Presentation Layer                           │
│ ATRM式艦影・前中後配置・物理スロット表示       │
├──────────────────────────────────────────────┤
│ Slot Contract Layer                          │
│ ATRMスロット数・位置・表示/編集/ロック状態      │
├──────────────────────────────────────────────┤
│ Semantic Equipment Layer                     │
│ NVRW式役割・兵装・機関・装甲・センサー・燃料    │
├──────────────────────────────────────────────┤
│ Data & Calculation Layer                     │
│ NSDB / HPCLC / GUNCLC / variant / OOB         │
└──────────────────────────────────────────────┘
```

GUI上の位置と、ゲーム内での装備の意味を同じIDへ押し込まない。物理位置はSlot Contract Layer、性能と分類はSemantic Equipment Layerが管理する。

## 6. スロット数の継承契約

### 6.1 最重要原則

ATRMRWはATRMのスロット「名称」だけでなく、スロット「数」と大小関係を継承する。ただし、旧ATRM派生船体に残る継承・再定義由来の不規則な実効数はそのまま凍結せず、船体規模に応じた標準プロファイルへ正規化する。

```text
ATRMRW_TOTAL_SLOT_COUNT(hull)
  = ATRM_SIZE_PROFILE_SLOT_COUNT(hull_size)

large hull slot count > small hull slot count
```

NVRW由来の役割・機関・装甲・旧hidden武装は、各ATRMRW標準プロファイルの物理スロット総数内へ収容する。hidden運用は継承せず、固定装備を含む全枠にGUI widgetを与える。史実上多数ある同種兵装は、同用途・同口径・同zone単位の可視batch moduleへ集約する。

役割、機関方式・出力、燃料、装甲、センサー、史実兵装batch、史実overflowは交換可能とする。交換不能な`fixed_visible`は船体構造だけに限定する。ここでGUIの`fixed`アンカー群は配置上の名前であり、交換不能状態を意味しない。

同一規模では世代が進んでも物理スロット総数を増減させず、未使用枠・ロック枠・編集可能枠の配分だけを変える。例外的な増減は、対象艦型・旧数・新数・理由・variant/OOB影響を提示し、ユーザーが個別承認した場合に限る。

### 6.2 スロット台帳

全船体は次の値を持つ設計台帳で管理する。

```text
total_slot_count
  = editable_slot_count
  + fixed_visible_slot_count
  + locked_visible_slot_count

hidden_slot_count = 0
```

| 値 | 定義 |
|---|---|
| `total_slot_count` | ATRM標準プロファイルから継承する物理枠総数。同一規模では原則不変 |
| `editable_slot_count` | プレイヤーがモジュールを交換できる枠 |
| `fixed_visible_slot_count` | GUI上に表示するが、艦級固有装備として固定する枠 |
| `locked_visible_slot_count` | GUI上に表示する未使用、恒久封鎖、または研究後解放の枠 |
| `hidden_slot_count` | ATRMRWでは常に0。SSW由来hiddenは可視枠へ変換する |

表示状態や編集可否を変更しても、可視3区分の合計は`total_slot_count`と一致させる。

標準プロファイルでは`fixed_visible_slot_count = 1`（船体構造）とする。SSW互換ID `ship_type_slot` は接頭辞規則に従いcustom 0へ配置し、`editable`に数える。最大36枠の実装時GUI内訳はcustom 18／fixed 18である。

全profileは機関方式・機関出力・主動力源・燃料搭載量／航続方式の4 engineering/fuel枠を持つ。小型profileでは総数を維持するため兵装枠を減らし、複数同型兵装をbatch moduleへ集約する。`locked`は共通profileへ一律設定せず、個別船体の未使用・年代制限枠を解決した時点で割り当てる。

### 6.3 艦体規模別の標準スロット数

大型から小型へ物理スロット数が減少することをATRMRWの固定規則とする。艦種はSSWの`ship_type_slot` taxonomyと同期するが、roleと物理規模を一対一対応させない。profileは排水量・船体容積・航空設備で決め、同じ艦種でも個別overrideを許可する。

| 規模プロファイル | 主な対象 | 総スロット数 | 物理規模の目安 |
|---|---|---:|---|
| Maximum | 大型空母、超大型戦艦、大型戦闘空母 | **36** | 40,000t超または航空設備特大 |
| Capital | 通常戦艦、巡洋戦艦、正規空母 | **30** | 20,000～40,000t |
| Large | 重巡洋艦、前弩級、小型空母、大型補助艦 | **24** | 10,000～20,000t |
| Medium | 軽巡洋艦、大型駆逐艦、護衛空母、巡洋潜水艦 | **18** | 4,000～10,000t |
| Escort | 駆逐艦、フリゲート、航洋潜水艦 | **15** | 1,300～4,000t |
| Coastal | 沿岸艦艇、沿岸潜水艦、小型支援艦 | **12** | 500～1,300t |
| Minimal | 特殊潜航艇、魚雷艇、哨戒艇、小型掃海艇 | **9** | 500t以下の特例船体 |

この大小順序は艦種の重要度ではなく、船体容積・排水量・搭載余地を表す。航空艦は飛行甲板・格納庫・航空燃料・航空管制を表現するため原則1段階上へ補正する。潜水艦は水上艦と排水量を直接比較せず、特殊潜航艇9、沿岸潜12、航洋潜15、巡洋・特殊潜18～24の独立ラダーを使う。

プロファイル内訳と全85現行船体の暫定割当は`atrmrw/ATRMRW_PHASE1_SLOT_CONTRACT.json`と`atrmrw/ATRMRW_PHASE1_HULL_PROFILE_MAP.csv`を正本とする。

### 6.4 旧ATRM最大レイアウトとATRMRW変換

旧ATRMのEquipment Designerは、次の最大配置を持つ。

| 区分 | 数 | 内容 |
|---|---:|---|
| 固定スロット | 19 | 燃料、機関、副砲、対空、飛行甲板、装甲、艦首、射撃管制、レーダー、ソナー等 |
| カスタムスロット | 17 | 中央7、艦尾5、艦首5の配置枠 |
| 合計 | **36** | ATRM最大物理スロット数 |

空母の旧ATRM原型は36枠を実際に宣言している。ATRMRW空母はこの36枠を最大予算として継承し、NVRW由来の意味スロットも36枠の内側へ配置する。

旧ATRM空母原型の36枠は次のとおりである。

**固定19枠:**

```text
fixed_ship_fuel_slot_1
fixed_ship_fuel_slot_2
fixed_ship_engine_slot
fixed_ship_engine_slot_2
fixed_ship_secondaries_slot
fixed_ship_secondaries_slot_2
fixed_ship_secondaries_slot_3
fixed_ship_secondaries_slot_4
fixed_ship_secondaries_slot_5
fixed_ship_anti_air_slot
fixed_ship_deck_slot_1
fixed_ship_deck_slot_2
fixed_ship_armor_slot
fixed_ship_armor_slot_2
fixed_ship_bow_slot_1
fixed_ship_bow_slot_2
fixed_ship_fire_control_system_slot
fixed_ship_radar_slot
fixed_ship_sonar_slot
```

**カスタム17枠:**

```text
main_weapon_slot_1
main_weapon_slot_2
main_weapon_slot_3
main_weapon_slot_4
mid_1_custom_slot
mid_2_custom_slot
mid_3_custom_slot
rear_1_custom_slot
rear_2_custom_slot
optional_slot_1
optional_slot_2
optional_slot_3
front_1_custom_slot
front_2_custom_slot
optional_slot_4
optional_slot_5
optional_slot_6
```

ATRMRWでは必要に応じてIDを正規化できるが、改名前後の一対一対応と総数36を台帳で維持する。

ATRMRW実装ではSSW互換の`ship_type_slot`をcustom 0へ置くため、旧ATRMのfixed 19／custom 17をそのままGUI groupへ移さず、fixed 18／custom 18へ再配分する。これは物理枠総数36を維持した接頭辞契約上の変換であり、編集可否とは独立する。

### 6.5 旧ATRM実測スロット表

Phase 0では`origin/future/Navy_rework`の固定コミット`64ceb88ba3e836ef248e473b90b6f646b1bf720d`から全62船体IDを機械抽出した。初版の一部の「明示枠数」は、個別`inherit`とスロットエイリアスを数えない本体ブロック数であり、物理スロットID数ではなかったため、次の実効分布へ訂正する。

| 船体系 | ID数 | 旧ATRM実効物理枠の分布 | ATRMRW正規化先 |
|---|---:|---|---|
| 空母 | 10 | 36枠×6、旧式7枠×4 | 航空補正込み18～36枠 |
| 巡洋艦 | 17 | 9枠×1、10枠×6、11枠×3、12枠×7 | 排水量別18～30枠 |
| 主力艦 | 15 | 10枠×1、11枠×9、12枠×2、14枠×3 | 排水量別24～36枠 |
| 軽艦艇 | 9 | 8枠×7、9枠×1、10枠×1 | 排水量別12～18枠 |
| 潜水艦 | 11 | 2枠×1、3枠×7、5枠×3 | 独立ラダー9～24枠 |

実効集合は、`parent`を`archetype`より優先し、`module_slots = inherit`を全体継承、`module_slots = { ... }`を列挙IDによる集合置換として解決する。`slot = inherit`と`slot_b = slot_a`も物理枠として各1枠を占める。詳細は`atrmrw/ATRMRW_PHASE0_AUDIT.md`と`atrmrw/ATRMRW_PHASE0_ATRM_SLOT_LEDGER.csv`を正本とする。

### 6.6 スロット数検証

実装前に旧ATRMブランチへ対して次の台帳を生成する。

```text
hull_id
parent_id
archetype_id
declared_slots
inherited_slots
overridden_slots
effective_slots
fixed/custom split
front/mid/rear split
```

ATRMRW移植後は、各船体が指定された規模別標準数に一致することと、旧ATRMからの変換表に未処理variantがないことを検証する。

## 7. ATRMRW標準スロットモデル

### 7.1 意味スロット

NVRWの意味分類を維持しつつ、ATRM物理枠へ割り当てる。

| グループ | 標準用途 |
|---|---|
| Role | 艦種・任務・ドクトリン上の役割 |
| Main armament | 主砲、主魚雷、主ミサイル、主航空運用設備 |
| Secondary armament | 副砲、副魚雷、副ミサイル、補助航空運用設備 |
| Light armament | 軽砲、近接対空、CIWS、対潜兵装 |
| Propulsion | 機関種別、機関出力、補助機関 |
| Fuel/Energy | 動力源、燃料搭載方式、航続距離設計 |
| Protection | 装甲材、装甲厚、水雷防御、ダメージコントロール |
| Sensors | 射撃管制、レーダー、ソナー、電子戦 |
| Hull feature | 艦首形状、飛行甲板、格納庫、特殊設備 |
| Historical overflow | 6基本兵装に収まらない史実武装の集約枠 |

### 7.2 6基本兵装＋役割

次の7意味枠は、全船体で論理的に存在させる。

```text
ship_type_slot
primary_armament_slot
secondary_armament_slot
primary_sub_armament_slot
secondary_sub_armament_slot
primary_light_armament_slot
secondary_light_armament_slot
```

`ship_type_slot`は最小9枠を含む全profileで可視の物理枠とする。15枠以上では6基本兵装を各1枠以上持ち、9/12枠では使用しない用途を省略し、同用途兵装を可視batch moduleへ集約する。使用不能枠もGUIから隠さず、`Non_releasable_locking_module`または`Releasable_locking_module`相当の可視ロックとして表現する。

### 7.3 物理位置

カスタム枠は次のゾーンへ分類する。

| ゾーン | ATRM継承位置 | 主用途 |
|---|---|---|
| Bow | `front_*` | 前部主砲、魚雷、艦首設備、前部対空 |
| Midship | `mid_*` | 主機、中央砲塔、煙突、飛行甲板、格納庫 |
| Stern | `rear_*` | 後部主砲、後部魚雷、航空設備、爆雷 |
| Optional | `optional_*` | 補助兵装、電子装備、特殊設備 |
| Fixed | `fixed_*` | 船体固有・自動算出・原則固定の装備 |

モジュールの搭載可否はcategoryだけでなく、艦種、年代、ゾーン、砲塔占有量の組合せで決める。

### 7.4 史実武装の集約

史実上多数搭載された副砲・対空砲は、スロットを1門・1基ずつ増やして表現しない。NVRWのbatch module方式を継承し、複数基を1モジュールへ集約する。

```text
物理スロット数はATRMに合わせて固定
性能・門数はbatch moduleで史実値へ合わせる
```

これにより、ATRMスロット数を守りながらNVRWの「実艦装備を省略しない」要件を満たす。

## 8. 燃料・機関システム

### 8.1 ATRMからの継承

旧ATRM空母は燃料2枠・機関2枠を持つ。ATRMRWではこれを次の意味へ整理する。

| ATRM枠 | ATRMRW用途 |
|---|---|
| Fuel 1 | 主動力源・燃料方式 |
| Fuel 2 | 燃料搭載量・航続距離方式・補助燃料 |
| Engine 1 | 機関種別 |
| Engine 2 | 機関出力・推進構成 |

NVRWの`hidden_EN_slot`と`hidden_ENPOWER_slot`はEngine 1/2へ変換し、通常GUIに表示する。元のhidden IDは移植後の船体・variantで使用しない。

### 8.2 動力源候補

ATRM資産に存在する思想を継承し、少なくとも次を表現可能にする。

- 帆走・補助帆装
- 石炭
- 石炭・重油混焼
- 重油
- 軽質油・高性能燃料
- 原子力
- 松根油等の代替燃料
- BSM世界観固有の超技術動力

各方式は単純な上位互換にせず、航続距離、速度、信頼性、燃料消費、被発見性、建造費、必要資源、研究条件へトレードオフを持たせる。

### 8.3 算定原則

- 機関出力はNVRWの`SM_ENPOWER`方式を転用可能とする。
- 航続距離はNSDBのEnduranceを海里からkmへ変換し、ゲーム内目標値を算出する。
- 速力は巡航速力と最大速力の平均を基本目標とする。
- 旧ATRM燃料モジュールの既存statは直接転用せず、ATRMRW計算式で再算定する。
- 架空動力も同年代の史実動力との比較表を持たせる。

## 9. 船体体系

### 9.1 三階層

| 階層 | 対象 | 実装方式 |
|---|---|---|
| S 固有 | 自国設計系譜を持つ主要海軍 | 史実・設定艦級1:1船体＋固有研究ツリー |
| A 半固有 | 象徴艦や少数の自国設計艦を持つ国 | 汎用船体＋準固有船体／variant |
| B 汎用 | 外国設計運用国、小海軍 | 年代Tier×艦種の汎用船体＋variant |

艦数ではなく設計原産性を判定軸とする。架空国家については、設定上の造船技術系譜を設計原産性として扱う。

### 9.2 標準艦種

- heavy / cruiser / light / frigate
- carrier / light carrier / battle carrier / cruiser carrier
- submarine / submarine carrier
- tender / tanker / repair / surveillance / submarine oiler
- special air support / support / craft

これら18海軍archetypeと105個の`SRM_*` role IDは、固定SSWコミットから機械抽出した`atrmrw/ATRMRW_SSW_ROLE_AND_ARCHETYPE_INVENTORY.json`を同期正本とする。`medium`は独立archetypeではなく`ship_hull_cruiser`配下の系統として扱う。旧ATRMに存在しない艦種も、roleではなく物理規模に基づいて9～36枠へ割り当てる。

## 10. 砲・対空・モジュール体系

### 10.1 砲

砲モジュールはNVRWの年代Tier×サイズClassを継承する。

```text
module_id: SM_<mount><type>_<TAG>_<bore>_L<caliber>
category:  SM_<mount><type>_T<tier>_SZ<size>
```

砲の性能はGUNCLCで算定し、最低限、口径、口径長、砲身数、発射速度、砲弾重量、初速、仰角、旋回・俯仰速度、砲塔重量を根拠として持つ。

### 10.2 対空

対空モジュールは物理占有量によるfootprint bandを使用する。

```text
SM_AA_SS / S / SM / M / ML / L / LL / X
```

小型艦へ大型の対空砲群を搭載できないよう、艦種別allowlistを設定する。主砲座を防空砲群へ転用する設計は、砲座サイズとAA footprintの等価表に基づいて許可する。

### 10.3 モジュール配置制約

各モジュールは次の属性を持つ設計とする。

```text
year_tier
size_class_or_footprint
allowed_hull_roles
allowed_zones
space_cost
power_requirement
crew_requirement
technology_requirement
conversion_group
```

HOI4スクリプトで直接表現できない属性は、category生成、船体allowlist生成、検証ツールの入力データとして管理する。

## 11. 史実設計と自由設計

### 11.1 史実設計モード

- 船体defaultは就役時・竣工時装備とする。
- 後年改装は別variantとする。
- 副砲・対空砲の門数は参照年の史実値へ一致させる。
- 艦級性能はNSDB、Navypedia、NavWeaps等へ追跡可能にする。
- 不明値は推測せずレビュー対象へ送る。

### 11.2 自由設計モード

- 同じ物理スロット数と搭載制約の範囲で装備を交換できる。
- 砲塔、対空群、航空設備、燃料、機関の選択に明確な代償を設ける。
- 史実variantを壊さず、プレイヤー設計を別versionとして保存する。
- 架空艦も同年代・同排水量帯の基準と比較して性能を決める。

### 11.3 両モード共通の禁止

- 物理スロット数の超過
- 艦型に収まらない砲塔・対空群の搭載
- 機関出力や燃料方式を無視した速力設定
- 装備を省略して見かけ上のスロット数だけ合わせること
- 同一兵装を可視枠と集約枠で二重計上すること

## 12. GUIコンセプト

### 12.1 基本画面

対象HOI4版の権威あるvanilla `equipmentdesignerview.gui`を実装母体とし、hardcoded widget契約を維持したまま海軍用position anchorだけを追加する。`origin/future/Navy_rework:bakasekai/interface/replace/equipmentdesignerview.gui`は、艦影を中央に置き装備位置を前部・中央・後部へ配置する視覚思想と最大36枠の参照に限定する。

```text
┌──────────────────────────────────────────────┐
│ 艦級・役割・設計年・経験値                    │
├───────────────┬──────────────────────────────┤
│ 固定技術欄     │      艦影・物理スロット       │
│ 燃料／機関     │  Bow     Midship      Stern   │
│ 装甲／管制     │   ○ ○    ○ ○ ○ ○      ○ ○    │
│ センサー       │      optional / support       │
├───────────────┴──────────────────────────────┤
│ 速力 航続距離 火力 対空 装甲 信頼性 乗員 費用 │
└──────────────────────────────────────────────┘
```

### 12.2 表示規則

- ATRM由来の物理位置と総数を保持する。
- 艦体規模に応じて36／30／24／18／15／12／9枠の表示プロファイルを切り替える。
- プレイヤー編集可能枠、固定表示枠、可視ロック枠を視覚的に区別する。hidden枠は作らない。
- 固定装備は消さず、折り畳みまたは技術詳細として確認可能にする。
- 史実variantでは搭載装備数と参照年を表示する。
- 砲塔・対空群は口径、門数、基数、占有Classを表示する。
- 燃料・機関は方式、出力、航続距離への寄与を表示する。
- 旧ATRMの座標思想を参照し、対象版vanillaへcustom index 7～16、fixed index 7～18を追加する。既存index 0～6とwidget名・型は変更しない。
- 同ファイル内の戦車・航空機Designer領域は現行BSM基準を維持し、ATRM旧版で巻き戻さない。
- ATRMブランチの`plane_designer_view.gui`や`tank_designer_view.gui`は海軍GUI移植の対象に含めない。

## 13. 名前空間とファイル方針

### 13.1 名前空間

新規ATRMRW所有IDは原則として次を使う。

```text
atrmrw_
ATRMRW_
GFX_ATRMRW_
```

SSWから転用する既存IDは、variant/OOB/technologyとの互換性を維持する必要がある場合のみ保持する。新規IDへ改名する場合は参照置換表を先に作る。

### 13.2 想定配置

```text
bakasekai/common/units/equipment/_atrmrw_japan_hulls.txt
bakasekai/common/units/equipment/modules/_atrmrw_*.txt
bakasekai/common/scripted_effects/_atrmrw_japan_variants.txt
bakasekai/interface/replace/equipmentdesignerview.gui
bakasekai/interface/_atrmrw_naval.gfx
bakasekai/localisation/japanese/bakasekai/atrmrw_l_japanese.yml
bakasekai/localisation/english/bakasekai/atrmrw_l_english.yml
documents/00_coding_contexts/ATRMRW_*.md
tools/atrmrw/
```

プロトタイプ船体は既存定義を副作用で変更しないよう、生成正本`_atrmrw_japan_hulls.txt`へ分離する。全国家展開時は国別乱立を避け、生成器の責務単位で統合する。

## 14. 実装フェーズ

### Phase 0: 凍結・棚卸し

- [x] 旧ATRM全船体の実効スロット数を継承込みで抽出する。
- [x] 固定／カスタム、前／中／後を台帳化する。表示／隠しは旧定義とGUI契約が一致しないため、Phase 1の最終マッピングで確定する。
- [x] SSW転用候補コードの所有・出典・第三者依存を分類する。
- [x] 現行BSMの船体、module、variant、OOB、GUI参照を棚卸しする。
- [x] ゲームコードを変更せず、`tools/atrmrw/`と監査文書だけを追加する。

### Phase 1: スロット契約

- [x] 全船体を36／30／24／18／15／12／9枠の規模別プロファイルへ割り当てる（現行85船体。原典排水量未結合行はreview flag付き）。
- [x] ATRM物理枠からATRMRW意味枠へのマッピング表を作る。
- [x] role、固定、可視ロック、全可視・hidden 0の契約をユーザー確認する。
- [x] SSW固定コミットから105 roleと18海軍archetypeを機械抽出し、同期対象を固定する。
- [x] 規模別スロット数と大型＞小型の順序を検証するチェッカーを先に作る。

### Phase 2: データモデルと計算

- [x] 船体台帳、モジュール台帳、スロット台帳の形式を決める。
- [x] HPCLC/GUNCLC転用範囲を確定する（GUNCLCは固定コミットのtracked config、HPCLC係数表は承認済み）。
- [x] 史実燃料・機関・航続距離のプロトタイプ計算規則を作る。航続目標の50%を交換可能endurance moduleへ配分し、残りを固定船体baseへ校正する。機関出力はSSW日本15万shp基準を線形参照し、未知値はstatを捏造しない。
- [x] 史実値と架空値の出典区分を定義する（史実方式を先行し、架空方式は後続フェーズ）。

### Phase 3: 最小プロトタイプ

代表船体を各1隻だけ実装する。

- [x] 主力艦: 大和型 `ship_hull_JAP_BB_3`
- [x] 巡洋艦: 高雄型 `ship_hull_JAP_CA_0`
- [x] 駆逐艦: 吹雪型 `ship_hull_JAP_DD_13`
- [x] 空母: 赤城型 `ship_hull_JAP_CV_0`
- [x] 潜水艦: 伊十五型 `ship_hull_JAP_SS_9`
- [x] 59論理module、5史実variant、英日localisation、技術接続を生成する。

プロトタイプでは全国家・全モジュールへ展開しない。

### Phase 4: 海軍専用GUI

1. [x] 対象HOI4版vanilla GUIを母体として、ATRM式最大36枠レイアウト用anchorを追加する。
2. [x] heavy/cruiser/light/carrier/submarineのexact-name containerを1.19.2原本から生成する。
3. [x] 陸空Designerの既存anchor 0～6をbyte-for-byte維持する静的回帰検証を行う。
4. [ ] 各物理枠と意味枠の目視・操作確認は、ユーザー指示により実機起動せず保留する。

### Phase 5: 史実・設定艦の移行

1. [x] 日本5艦級プロトタイプを最初のS固有海軍として実装する。
2. [ ] A半固有、B汎用への全国家展開は後続goalとする。
3. [x] variantとOOBを同時に配線する（赤城1、高雄4、吹雪23、計28隻）。
4. [x] 旧variantを削除せず、新船体IDへOOB参照だけを移行する。

### Phase 6: バランス・実機検証

このPhaseはユーザーの「HOI4起動禁止」指示により未実施である。静的プロトタイプ完了と実機完了を区別し、次の項目を確認済みと表現しない。

- Equipment Designer表示
- 建造可否
- 改装可否
- AI設計
- variant生成
- OOBロード
- 海戦性能
- 燃料消費
- セーブ互換性
- error.log
- profiler

## 15. 検証要件

### 15.1 静的検証

| ID | 検証 |
|---|---|
| V1 | 全船体が36／30／24／18／15／12／9枠の指定プロファイルに一致し、大型から小型へ枠数が減少する |
| V2 | 全宣言スロットにdefault moduleがある |
| V3 | default moduleのcategoryがslot allowlistに含まれる |
| V4 | module ID、category、gui_categoryが正規形式である |
| V5 | variant/OOB/techからの参照が解決する |
| V6 | 日本語・英語locが存在する |
| V7 | GFX名と画像実体が存在する |
| V8 | 史実variantの砲・対空門数が参照データと一致する |
| V9 | 物理スロット総数を超える意味スロットがない |
| V10 | ATRM GUI移植後も戦車・航空機Designerの表示・操作に回帰がない |
| V11 | `hidden_*`スロット宣言・参照がATRMRW移行対象に残らず、全物理枠にGUI widgetがある |
| V12 | SSW固定コミットの105 role IDとATRMRW role台帳の同期差分がない |

### 15.2 実機検証

1. 各代表艦種でDesignerを開く。
2. 全物理枠が意図した位置に表示される。
3. ロック枠が不正に交換できない。
4. 前部用装備を艦尾等の不正位置へ搭載できない。
5. 大型砲・大型AA群を小型艦へ搭載できない。
6. 燃料・機関変更が速力、航続距離、消費、費用へ反映される。
7. 史実variantが正しい装備数を持つ。
8. 設計保存、建造、改装、OOBロードが成功する。
9. `error.log`にATRMRW由来のエラーがない。

## 16. 完了条件

コンセプトフェーズの完了条件:

- [x] ATRMとNVRWの責務を分離した
- [x] ATRMのスロット数を継承対象へ含めた
- [x] 旧ATRM最大36枠（固定19＋カスタム17）を記録し、ATRMRW実装をSSW互換custom18＋fixed18へ変換した
- [x] 大型から小型へ36／30／24／18／15／12／9枠とする標準プロファイルを定めた
- [x] 対象版vanilla GUIを実装母体、旧ATRM GUIを視覚・36枠思想の参照に定めた
- [x] NVRW意味スロットをATRM枠内へ収容する原則を定めた
- [x] SSWコード転用契約と出典管理方針を記録した
- [x] 燃料・機関・史実計算・GUIの統合方針を定めた
- [x] 旧ATRM全船体の継承込み実効スロット台帳を生成する
- [x] 艦種と物理サイズを分離した最終スロットマッピングをユーザー承認する
- [x] 全slot可視・hidden運用廃止を決める
- [x] 最小プロトタイプを大和・高雄・吹雪・赤城・伊十五型に決める

実装完了を名乗るには、静的検証だけでなくHOI4実機でのDesigner、建造、改装、OOB、海戦、ログ確認が必要である。

本版が完了とする範囲は「コンセプト文書」と「日本5艦級静的プロトタイプ」であり、ゲーム内動作確認済みの意味ではない。実機検証はユーザー指示により明示的に未実施とする。

## 17. 未決事項

| ID | 論点 | 決定時期 |
|---|---|---|
| OQ-5 | ATRM燃料方式のTier・研究・転換コスト | Phase 2 |
| OQ-6 | BSM固有超技術動力の性能上限 | Phase 2 |
| OQ-8 | 既存セーブ・既存variant IDの互換方針 | Phase 5 |
| OQ-9 | SSW roleのうちBSM開始年代外・世界観外roleをいつ解禁するか | Phase 3～5 |

## 18. 参照

### ATRM

- Git branch: `origin/future/Navy_rework`
- `bakasekai/common/units/modules/00_ship_fuel.txt`
- `bakasekai/common/units/ship_hull_carrier.txt`
- `bakasekai/common/units/ship_hull_cruiser.txt`
- `bakasekai/common/units/ship_hull_heavy.txt`
- `bakasekai/common/units/ship_hull_light.txt`
- `bakasekai/common/units/ship_hull_submarine.txt`
- `bakasekai/interface/replace/equipmentdesignerview.gui`

### SSW/NVRW

- Fixed commit: `4bcb07d5c11f3c78c3383db393abc9bbbf4dbdc1`
- `SSW_mod/documentation/ai/naval_hull_implementation_policy.md`
- `SSW_mod/documentation/ai/naval_equipment_module_implementation_policy.md`
- `SSW_mod/documentation/ai/naval_secondary_aa_implementation_policy.md`
- `SSW_mod/documentation/ai/naval_rework_requirements_2026-06.md`
- `SSW_mod/documentation/ai/naval_gun_tier_size_rework_draft.md`
- `SSW_mod/documentation/ai/naval_module_current_migration_policy_2026-07.md`
- `SSW_mod/tools/naval/HPCLC.py`
- `SSW_mod/tools/clc/gun_clc.py`
- `SSW_mod/tools/naval/nsdb_tool.py`
- `SSW_mod/nvpda-db/NSDB.db`
