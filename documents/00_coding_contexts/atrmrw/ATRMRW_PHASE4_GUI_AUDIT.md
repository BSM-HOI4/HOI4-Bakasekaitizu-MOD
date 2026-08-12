# ATRMRW Phase 4 Equipment Designer GUI監査

- 状態: HOI4 1.19.2基準の静的生成・検証完了、実機目視は未実施
- 旧ATRM固定commit: `64ceb88ba3e836ef248e473b90b6f646b1bf720d`
- 対象HOI4: インストール済み1.19.2

## 1. 結論

旧ATRMの`equipmentdesignerview.gui`は丸ごと移植できない。インストール済みHOI4 1.19.2 vanillaファイルを基準とし、既存widget名・型・index 0～6を保ったまま、海軍用の追加position anchorだけを増設する。

```text
pos_custom_module_slot_window_7 .. 17
pos_fixed_module_slot_window_7  .. 17
```

ATRMから継承するのは艦影中心の前／中／後配置思想と36枠上限であり、旧full-replaceファイルそのものではない。

## 2. 旧ATRMで確認した欠陥

- `@UPPER_3_y`を4回、`@UPPER_3_y_t`を1回参照するが、変数定義がない。
- fixed anchor 12と13が同一座標で重なる。
- 空母equipmentは36枠だが、船体GUI側containerは33枠しかない。
- 欠落は`fixed_ship_bow_slot_1`、`fixed_ship_bow_slot_2`、`optional_slot_6`。
- rootを1541×651へ拡張しており、1366×768やUI scalingで画面外になる危険がある。
- 1.12.7用ファイルであり、現行1.19.2のwidget群を持たない。

## 3. 回帰隔離契約

次のhardcoded IDとelement typeを1.19.2 vanillaから変更しない。

```text
countryequipmentdesignerview
equipment_modules
equipment_preview
module_selector_window
equipment_designer_module_slot_entry
icn_module_slot_frame
btn_module_slot
icn_requirements
icn_warning
```

旧ATRMの戦車・航空GUI、36組の手書きbutton/icon、旧root寸法、旧背景spriteは移植しない。既存index 0～6も移動しない。これにより、追加indexを使わない戦車・航空機への影響を限定する。

## 4. 7 profile共通配置

profileごとにGUIファイルを7個複製せず、最大36枠の共通座標表を使う。各slot台帳は次を持つ。

```text
slot_id
fixed_or_custom
ui_index
x
y
profile_min
```

9→12→15→18は3枠ずつ、18→24→30→36は6枠ずつ外側へ増えるnested配置とする。SSW互換の`ship_type_slot`をcustom 0とし、custom 0～17、fixed 0～17は欠番・座標重複を禁止する。

## 5. 1.19.2実装ゲート

インストール済み1.19.2 vanillaファイルのSHA-256を固定し、次を確認する。

- source: `/Users/eightman/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV/interface/equipmentdesignerview.gui`
- SHA-256: `c1a6cf7c0b74f9f428cf5d50c3f422c5f675b38adbcef9c8c1e13070fa9dbc22`
- panel: 512×350
- slot entry: 76×47
- 生成器: `tools/atrmrw/generate_equipmentdesigner_gui.py`
- 出力: `bakasekai/interface/replace/equipmentdesignerview.gui`

1. 1.19.2のwidget manifestとslot entry実寸。
2. 戦車・航空のcustom/fixed最大index。
3. 36枠が既存panel内またはpanel外へ非重複配置できるか。
4. 1366×768、1920×1080、利用UI scaleで全枠が画面内か。
5. MIO、保存、auto、duplicate、モデル選択、戦車・航空Designerに回帰がないか。

1.19.2 baselineのhashと機械パッチ手順を記録せず、full-replace GUIを作成しない。

静的配置は6段とし、vanilla 0～6を保持する。

| group | index | y | x列 |
|---|---|---:|---|
| custom | 0～6 | 0 | 0, 73, 146, 219, 292, 365, 438 |
| custom | 7～13 | 50 | 同上 |
| custom | 14～17 | 100 | 0, 73, 146, 219 |
| fixed | 7～13 | 200 | 0, 73, 146, 219, 292, 365, 438 |
| fixed | 14～17 | 250 | 0, 73, 146, 219 |
| fixed | 0～6 | 300 | vanilla同上 |

全36座標の一意性とpanel境界内配置は`test_gui_layout.py`で検証する。クリック領域、tooltip、UI scale、戦車・航空・MIO回帰は実機ゲートとして残す。

艦種固有GUIは`tools/atrmrw/generate_ship_archetype_guis.py`で、heavy/cruiser/light/carrier/submarineの1.19.2原本SHA-256を個別固定し、最大profileの36 `game_slot_id` containerをexact-nameで追加する。全原本との差分はこのcontainer追加だけである。

## 6. 旧1.13候補の追跡結果（参考のみ）

ローカル全候補をgit履歴込みで確認したが、vanilla 1.13からのbit-identicalコピーと証明できるファイルはなかった。

### 構造参照A: EoaNB AAT Update

- repository: `/Users/eightman/dev/hoi4/EoaNB`
- commit: `d3a6f604e682ce9c369bc1ad9efd06b66372e5b1`
- `supported_version`: `1.13.*`
- GUI blob: `7269c3c54abfee696d07e21263ab41dbe593ce3c`
- SHA-256: `c9497920e8d2d7f2fdc501152c198fc9256c12c9b8865712dba4b7a9759f4a31`
- 確認できる1.13構造: MIO/historical design widget、root 1097×542、module panel 512×350、slot entry 76×47、custom/fixed anchor各0～6

同commitでdescriptorを1.12から1.13へ更新しAAT/MIO関連ファイルを導入しているため、1.13互換構造の第一参照にはできる。ただしmod full-replacementであり、vanilla原本のdepot manifestやhash記録がないため実装baselineには昇格しない。

### 構造参照B: SSW 1.13.1

- repository: `/Users/eightman/dev/hoi4/SSW_mod`
- GUI commit: `399005e9e7912013d113d0b64f4408c3fc864b2e`
- 1.13.1 descriptor commit: `193afc524e694d928ddd4e9d5759a914d83190e7`
- GUI blob: `87d5fab86470fe1e5669c259310e9d7bed78c102`
- SHA-256: `2635b0332d0b7009e428f701659f80e8be4f5a4bb55b68d38e9ba151f71adf88`

EoaNBと同じMIO/historical widget群を持つため独立した裏付けになる。一方、root拡張、custom/fixed各0～8、`#SSW追加分`を含む明示的改造版なのでbaselineには使わない。

### 棄却: 旧ATRM

旧ATRM導入元は`descriptor.mod`で`1.12.7`を指定しており、1.13 GUIではない。よって「ATRM GUIを実装母体にする」という初版文言は、視覚思想の参照という意味へ改訂する必要がある。
