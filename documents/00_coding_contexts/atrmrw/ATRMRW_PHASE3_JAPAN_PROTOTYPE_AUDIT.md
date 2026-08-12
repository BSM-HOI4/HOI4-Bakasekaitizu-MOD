# ATRMRW Phase 3 日本海軍5艦級プロトタイプ入力監査

- 状態: 史実入力・profile・role・ゲーム実装ID確定、静的プロトタイプ実装済み
- 入力台帳: `ATRMRW_PHASE3_JAPAN_PROTOTYPE_LEDGER.json`
- NSDB SHA-256: `6d5418efa26f8c73afb386b8eb3f0dea47cf65fa03303d3c0f8c17e52122f1ad`
- 再生成: `python3 tools/atrmrw/build_japan_prototype_ledger.py --db <NSDB.db> --output documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_PROTOTYPE_LEDGER.json`

## 1. 確定入力

| 艦級 | SSW role | Profile | 計算排水量 | 目標速力 | 目標航続距離 |
|---|---|---|---:|---:|---:|
| 大和型 | `SRM_BB` | 36 | 72,810t | 21.50kn | 6,667.2km |
| 高雄型 | `SRM_CA` | 24 | 14,260t | 24.75kn | 7,871.0km |
| 吹雪型 | `SRM_DD` | 15 | 2,097t | 26.50kn | 4,352.2km |
| 赤城型（1927） | `SRM_CV` | 36 | 34,364t | 22.50kn | 7,408.0km |
| 伊十五型／乙型一型 | `SRM_SC` | 18 | 3,654t（水中） | 19.80kn（水上） | 12,964.0km（水上） |

速力は`(最大速力＋巡航速力)/2`、航続距離は`航続海里×1.852/2`。船体HP・組織率は承認済みHPCLC対応表で算出する。丸め前値と入力digestはJSON台帳へ保存しており、HOI4出力時の丸めは別adapterで行う。

## 2. 原典上の注意

- 大和型: NSDBのbreadthは36.9mだが、SSW HPCLC test harnessは38.9mを使用している。プロトタイプはDB rawを優先し36.9mとし、差異を隠さない。
- 高雄型: 1932状態は満載14,260t。1938～39改装後の15,875tは後年variantとして分離する。
- 赤城型: 1927状態は石炭・重油混焼、航空機60機。1938改装後の石油専焼・91機状態は別variantとする。
- 伊十五型: NSDBの`Displacement_full`が空で、`Displacement_normal`に水上2,589t／水中3,654tが併記される。HPCLC入力には水中3,654tを明示的に採用した。
- 伊十五型: speed、endurance、powerも水上／水中併記である。ゲームの基本目標には水上23.6kn・巡航16kn・14,000nmを使い、水中値をrawから削除しない。

## 3. 承認済み実装ID（ユーザー回答1B）

| 艦級 | 実装ID | 根拠・注意 |
|---|---|---|
| 大和型 | `ship_hull_JAP_BB_3` | SSW大和型IDを共有 |
| 高雄型 | `ship_hull_JAP_CA_0` | SSW高雄型IDを共有 |
| 吹雪型 | `ship_hull_JAP_DD_13` | SSW本国用吹雪型IDを共有。`DD_3`は輸出用史実性能枠 |
| 赤城型 | `ship_hull_JAP_CV_0` | SSW赤城型IDを共有 |
| 伊十五型 | `ship_hull_JAP_SS_9` | SSW/NGUで巡潜乙型の共有先に使われるID。SSW船体コメントの「乙改一」と名称差があるため移行台帳に残す |

数値IDはSSWと同期する。ID共有は性能値の無条件コピーを意味せず、ATRMRWの基準年・史実入力・全可視スロット契約で船体と既定variantを再構成する。吹雪型と伊十五型の名称・基準年差は黙って吸収せず、variant/OOB移行台帳で追跡する。
