# ATRMRW Phase 0 棚卸し結果

- 対象: `ATRMRW-NDC-001`
- 旧ATRM固定コミット: `64ceb88ba3e836ef248e473b90b6f646b1bf720d`
- 現行BSM固定コミット: `964b31677d3f4f12d85bfe4e1a51ec8794fb680e`
- 実施日: 2026-08-02
- 状態: 静的棚卸し完了、HOI4実機の継承挙動確認は未実施

## 1. 成果物

| 成果物 | 用途 |
|---|---|
| `tools/atrmrw/inventory_atrm_slots.py` | git objectから旧ATRM船体を読み、継承込み実効スロットを再生成 |
| `ATRMRW_PHASE0_ATRM_SLOT_LEDGER.csv` | 人間による表計算・レビュー用台帳 |
| `ATRMRW_PHASE0_ATRM_SLOT_LEDGER.json` | Phase 1以降のチェッカー入力 |
| `tools/atrmrw/inventory_bsm_naval.py` | 現行BSMの船体、module、variant、参照、GUI/GFXを棚卸し |
| `ATRMRW_PHASE0_BSM_INVENTORY.json` | 現行BSM影響面の機械可読スナップショット |
| `ATRMRW_MIGRATION_LEDGER.md` | ATRM/SSWからの転用元と権利・依存関係の台帳 |

## 2. 旧ATRMスロットの継承規則

静的定義に整合する解決規則は次のとおり。

1. 継承元は`parent`を優先し、存在しない場合は`archetype`とする。
2. `module_slots = inherit`は継承元の実効集合を丸ごと複製する。
3. `module_slots = { ... }`は親集合への追加ではなく、列挙されたIDによる集合全体の置換として扱う。
4. `slot_id = inherit`は継承元の同名スロット設定をコピーするが、物理枠として1枠を占める。
5. `slot_b = slot_a`は設定のエイリアスであり、`slot_b`も別の物理枠として1枠を占める。
6. 循環、未解決継承元、存在しない個別継承、存在しないエイリアス先は抽出エラーとする。

この規則は旧ATRMファイルの構造から静的に確認した。HOI4 1.13実機のエンジンダンプによる最終確認はPhase 6まで保留する。

## 3. 旧ATRM実効スロット結果

全62船体IDを抽出し、`module_slots`ブロック32件、全体`inherit`30件を解決した。

| 系列 | ID数 | 実効スロット数の分布 |
|---|---:|---|
| 空母 | 10 | 36枠×6、7枠×4 |
| 巡洋艦 | 17 | 9枠×1、10枠×6、11枠×3、12枠×7 |
| 主力艦 | 15 | 10枠×1、11枠×9、12枠×2、14枠×3 |
| 軽艦艇 | 9 | 8枠×7、9枠×1、10枠×1 |
| 潜水艦 | 11 | 2枠×1、3枠×7、5枠×3 |

コンセプト初版の9／10／7／3／0という一部の「旧実測値」は、個別`inherit`とエイリアスを除いた本体ブロック数に近く、物理スロットID数ではなかった。初版の36／11／9／7／3／0案はその後のユーザー補足で廃止され、承認済みATRMRW標準プロファイルは36／30／24／18／15／12／9である。

## 4. 現行BSM影響面

`ATRMRW_PHASE0_BSM_INVENTORY.json`の生成結果:

| 領域 | 確認値 |
|---|---:|
| 艦船equipment/hull ID | 85（主要5系列79＋repair/support 6） |
| `00_ship_modules.txt`内module ID | 116（トップレベル`limit`を除外） |
| 海軍technology ID | 130 |
| 全`create_equipment_variant` | 885 |
| うち既存hull IDを`type`に持つ艦船variant | 589（`_BSM_navy_no_MtG.txt`の99件を含む） |
| OOB艦艇entry | 911（67ファイル） |
| hull IDを参照するscripted effect/technology/history/OOBファイル | 105 |
| `gfx/interface/equipmentdesigner`配下アセット | 26 |

現行BSMには`interface/replace/equipmentdesignerview.gui`の上書きが存在しない。海軍GUI移植は新規の全体Designer上書きになるため、陸空領域を現行ゲーム／BSM基準から巻き戻す危険が高い。Phase 4ではATRM旧ファイルの全置換ではなく、現行基準ファイルへ海軍差分だけを移植し、戦車・航空機領域を比較検証する。

## 5. Phase 1へ持ち越す判断

- 旧実効数から標準プロファイルへの変換は、ID単位の変換表で明示する。
- 36／30／24／18／15／12／9への割当だけでなく、editable/fixed-visible/locked-visibleの合計一致と`hidden=0`を検証する。
- 旧ATRMの小型艦8〜10枠、巡洋艦10〜12枠、主力艦12〜14枠、潜水艦5枠は、装備を省略せず集約moduleへ変換する必要がある。
- 特殊潜航艇は旧実効2枠から目標0枠へ変換するため、機関・魚雷をvariant固定値／船体性能へ移す契約が必要である。
- 589件の現行艦船variantと911件のOOB艦艇を一括置換しない。Phase 3の5代表艦で変換器と検証器を固めてから国単位で展開する。

## 6. 再生成・検証

```bash
python3 tools/atrmrw/inventory_atrm_slots.py \
  --csv documents/00_coding_contexts/atrmrw/ATRMRW_PHASE0_ATRM_SLOT_LEDGER.csv \
  --json documents/00_coding_contexts/atrmrw/ATRMRW_PHASE0_ATRM_SLOT_LEDGER.json
python3 tools/atrmrw/inventory_bsm_naval.py \
  --json documents/00_coding_contexts/atrmrw/ATRMRW_PHASE0_BSM_INVENTORY.json
python3 -m unittest discover -s tools/atrmrw -p 'test_*.py' -v
```
