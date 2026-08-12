# ATRMRW 移植台帳

## 判定記号

- `内部`: BSM/ATRMリポジトリ内の既存コード。履歴と変換内容を保持して移植する。
- `許諾主張`: ATRMRW設計文書において、ユーザー本人作成コードとして転用許諾が示されている。
- `要確認`: コードと同時に第三者データ・画像・ライセンスが混在し得るため、実移植前にファイル単位で確認する。
- `参照のみ`: ATRMRWへ複製せず、根拠データとして参照する。

## 台帳

| Source repository | Source commit | Source path | Ownership basis | Destination path | Transformation | Third-party dependency | 状態 |
|---|---|---|---|---|---|---|---|
| BSM旧ATRM | `64ceb88ba3e836ef248e473b90b6f646b1bf720d` | `bakasekai/common/units/ship_hull_*.txt` | 内部 | 現行`bakasekai/common/units/equipment/ship_hull_*.txt` | スロットID・数・継承を台帳化し、標準プロファイルへ再構成 | vanilla ID/categoryとの互換確認 | 棚卸し済 |
| BSM旧ATRM | 同上 | `bakasekai/common/units/modules/00_ship_fuel.txt` | 内部 | `bakasekai/common/units/equipment/modules/_atrmrw_fuel.txt` | IDを`atrmrw_`へ分離し、statを再計算 | GFX出典は別途確認 | 候補 |
| BSM旧ATRM | 同上 | `bakasekai/interface/replace/equipmentdesignerview.gui` | 内部 | 現行GUIへ直接コピーしない | 艦影中心思想と36枠上限のみ参照 | 1.12.7用・欠損/重複座標あり | 参照のみ |
| HOI4 vanilla | インストール済み1.19.2 / SHA-256 `c1a6cf7c0b74f9f428cf5d50c3f422c5f675b38adbcef9c8c1e13070fa9dbc22` | `interface/equipmentdesignerview.gui` | vanilla基準 | `bakasekai/interface/replace/equipmentdesignerview.gui` | 原本を保持し、custom 7～17 / fixed 7～17のposition anchorだけ決定論的に追加 | ゲーム本体に依存 | 静的生成・test済、実機未実施 |
| HOI4 vanilla | インストール済み1.19.2 / 艦種別SHA固定 | `interface/equipmentdesigner/ships/ship_hull_{heavy,cruiser,light,carrier,submarine}.gui` | vanilla基準 | 同一相対パス | 原本を保持し、ATRMRW 36枠のexact-name containerのみ追加 | ゲーム本体に依存 | 静的生成・test済、実機未実施 |
| BSM旧ATRM | 同上 | `bakasekai/interface/replace/equipmentdesignerview.gfx` | 内部／要確認 | `bakasekai/interface/_atrmrw_naval.gfx` | 海軍spriteだけ抽出、名前空間化 | 画像実体の出典確認が必要 | 要確認 |
| SSW_mod | `4bcb07d5c11f3c78c3383db393abc9bbbf4dbdc1` | `tools/naval/HPCLC.py` | 許諾主張、git履歴上の作者確認済 | `tools/atrmrw/calculations.py` | 純粋関数化し、船体種別係数・年代補正・入力検証を固定 | Python標準ライブラリのみ確認 | golden test済み |
| SSW_mod | 同上 | `tools/clc/gun_clc.py`、`gun_calc_settings.py`、`gun_calc_config.json` | 許諾主張、git履歴上の作者確認済 | `tools/atrmrw/calculations.py`、`tools/atrmrw/gun_calc_config_ssw_4bcb.json` | import時書込みとglobal設定を除去し、純粋関数＋固定configへ分離 | policy係数は不採用。固定commitのtracked configを採用 | ユーザー承認済み・golden test済み |
| SSW_mod | 同上 | `tools/naval/nsdb_tool.py` | 許諾主張、git履歴上の作者確認済 | `tools/atrmrw/nsdb_readonly.py` | query-only接続、URL一意選択、DB manifest/SHA固定へ分離 | コミット外NSDB.dbに依存 | 実装・test済み |
| SSW_mod | 同上 | `nvpda-db/NSDB.db` | 第三者データを含む可能性あり | リポジトリへ複製しない | 外部DBとして参照し、出典URL・取得日・行数・SHA-256を成果物へ記録 | 固定コミットには不在。現行は外部symlink、NSDB/Navypedia由来 | 参照のみ |
| SSW_mod | 同上 | `common/units/equipment/modules/00_S_*.txt` | 許諾主張／要確認 | `bakasekai/common/units/equipment/modules/_atrmrw_japan_modules.txt` | 32 source blockをID単位で追跡し、exact 10・非線形batch 21・史実新規28の計59moduleへ変換 | GFXは転用せず、数値と分類だけを採用 | 日本prototype実装・静的test済 |
| SSW_mod | 同上 | `common/units/equipment/ship_hull_*.txt` | 許諾主張／要確認 | `bakasekai/common/units/equipment/_atrmrw_japan_hulls.txt` | 大和・高雄・吹雪・赤城・伊十五の数値IDを共有し、9～36全可視slotへ再構成 | NSDB source URL/SHAを別台帳で固定 | 日本prototype実装・静的test済 |

## 運用規則

1. SSW作業ツリーには未コミット変更があるため、移植元は必ずコミットハッシュで固定する。
2. `要確認`の行は、画像・データ・共同制作ブロックの由来を確認するまで実装へコピーしない。
3. ソースファイル全体をコピーせず、採用ブロックと変換理由を行単位またはID単位で追記する。
4. SSWの作業ツリーやDBシンボリックリンクをATRMRWの実行時依存にしない。
5. 各Phase完了時にDestination、Transformation、状態を更新する。
