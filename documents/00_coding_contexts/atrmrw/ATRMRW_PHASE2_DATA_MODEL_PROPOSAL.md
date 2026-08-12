# ATRMRW Phase 2 データモデル契約

- 状態: ユーザー承認済み
- 原則: raw値、正規化値、導出値、HOI4出力値を上書きせず分離する

実装済みのread-only入口は`tools/atrmrw/nsdb_readonly.py`とする。DBパスは`--db`または`ATRMRW_NSDB_PATH`で明示し、manifestで行数・schema・SHA-256を固定する。class名検索は候補列挙に留め、採用行はnormalized source URLで一意選択する。

## 1. 共通出典レコード

全ての史実値・設定値・計算値は次のprovenanceを持つ。

```json
{
  "source_id": "nsdb:japan/jap_bb_yamato",
  "source_type": "nsdb",
  "source_repository": null,
  "source_commit": null,
  "source_path": "CLASS",
  "source_locator": "source_url=https://.../jap_bb_yamato.htm",
  "source_url_raw": "https://www.navypedia.org/ships/japan/jap_bb_yamato.htm",
  "source_url_normalized": "https://myownonpmirror.com/ships/japan/jap_bb_yamato.html",
  "fetched_at": "<DB記録値>",
  "ownership_basis": "third_party_reference",
  "review_status": "confirmed"
}
```

`source_type`は`nsdb`、`navweaps`、`vanilla`、`bsm_existing`、`ssw_owned_code`、`user_spec`、`derived`を許可する。`derived`は入力source IDとformula IDを必須とする。

## 2. 値レコード

```json
{
  "field": "displacement_full_t",
  "raw_value": "63200 / 72810",
  "normalized_value": 72810.0,
  "unit": "metric_ton",
  "normalization_rule": "maximum_numeric_candidate",
  "source_ids": ["nsdb:japan/jap_bb_yamato"],
  "status": "confirmed",
  "review_notes": null
}
```

`status`は`confirmed`、`derived`、`unknown`、`conflict`、`user_spec`を許可する。`unknown`または`conflict`を含む必須入力からゲーム値を自動生成してはならない。

## 3. 船体台帳

必須項目:

```text
hull_id
class_name_english / class_name_japanese
country_tag / historical_country
role_id
slot_profile_id
design_year / commissioned_year / reference_year
displacement_normal_t / displacement_full_t
length_oa_m / breadth_m
maximum_speed_kn / cruising_speed_kn
machinery_raw / power_shp
fuel_raw / endurance_nm / endurance_cruise_kn
armor_raw / complement
source_ids[]
computed_stats {
  max_strength, max_organisation, naval_speed,
  naval_range, build_cost_ic, manpower,
  formula_ids[], input_digest, review_status
}
```

史実classと汎用hullを同一schemaで扱う。架空hullは`source_type=user_spec`と比較対象hull IDを必須にする。

## 4. モジュール台帳

必須項目:

```text
module_id / module_kind
display_name_english / display_name_japanese
country_tag
design_year / year_tier
size_class_or_footprint
category / gui_category
allowed_hull_roles[] / allowed_zones[]
space_cost / power_requirement / crew_requirement
technology_requirement / conversion_group
physical_inputs {
  bore_cm, caliber_length, muzzle_velocity_mps,
  barrels_per_mount, mount_count, rounds_per_minute,
  shell_weight_kg, elevation_deg, elevation_rate_deg_s,
  train_rate_deg_s, mount_weight_kg
}
computed_stats { formula_id, config_digest, values, review_status }
source_ids[]
```

入力欠損時にcaliber-band defaultを使った場合、そのdefault tableのIDと適用理由をsourceとして記録する。

## 5. スロット台帳

Phase 1契約JSONを正本とし、各hullの解決後レコードは次を満たす。

```text
total_slot_count
  = editable_slot_count
  + fixed_visible_slot_count
  + locked_visible_slot_count

hidden_slot_count = 0
```

各slotは`physical_slot_id`、`zone`、`state`、`semantic_slots[]`、`allowed_categories[]`、`default_module_id`を持つ。全宣言slotのdefaultとallowlist整合を静的検証する。

`role`は編集可能、`hull_structure`だけが固定singletonである。GUIのfixed/customアンカー区分をslot stateとして解釈してはならない。

## 6. variant/OOB台帳

```text
variant_id / version_name / reference_year
hull_id
slot_modules { physical_slot_id: module_id }
historical_armament_snapshot[]
aggregation_records[]
source_ids[]
oob_references[] { country_tag, file, fleet, ship_name }
```

`aggregation_records`は史実門数と物理module数を結び、同一兵装の可視枠・overflow枠二重計上を禁止する。

## 7. 計算式台帳

全式は次を持つ。

```text
formula_id
formula_version
source_repository / source_commit / source_path
coefficient_set
input_units / output_units
rounding_rule
valid_input_range
test_vectors[]
approval_status
```

計算成果物は`formula_id`、設定内容のSHA-256、入力レコードのdigestを保存する。同じ入力から同じ出力を再生成できない値は台帳へ採用しない。

## 8. 史実基準variantの固定基礎値

速度・航続距離等の最終目標値`T`に対し、史実基準variantの全既定moduleが与える加算合計`A`と乗算合計`M`から船体基礎値を一度だけ逆算する。

```text
final = (base + A) * (1 + M)
base_reference = T / (1 + M_reference) - A_reference
```

`1 + M_reference > 0`かつ`base_reference >= 0`を必須とする。基礎値は基準variantのmodule構成digestと共に固定し、プレイヤーがmoduleを交換した後に再計算しない。交換後は同じ固定基礎値へ新module寄与を順方向適用する。これにより高性能目標の船体から弱いmoduleへ交換して基礎値だけを維持・増幅する逆算悪用を防ぐ。

HOI4 1.19.2実機で加算・乗算の適用順を制御実験し、一致が確認されるまで`runtime_calibration_status=pending`とする。

## 9. 史実値と架空値の区分

| 区分 | source_type | 自動生成 |
|---|---|---|
| 史実raw | nsdb/navweaps | 可。ただし曖昧値はreviewへ |
| 史実derived | derived | 承認済formulaとconfirmed入力の場合のみ可 |
| BSM設定値 | user_spec | ユーザー指定をそのまま保存 |
| 架空derived | derived＋user_spec | 比較対象と上限ルール承認後のみ可 |
| 不明値 | unknown | 不可。推測せず保留 |

## 9. Read-only DB検証

```bash
python3 tools/atrmrw/nsdb_readonly.py --db /path/to/NSDB.db manifest
python3 tools/atrmrw/nsdb_readonly.py --db /path/to/NSDB.db \
  search AKAGI --country Japan --type aircraft-carrier
python3 tools/atrmrw/nsdb_readonly.py --db /path/to/NSDB.db \
  select --source-url https://myownonpmirror.com/ships/japan/jap_cv_akagi.html
```

SQLite接続はURI `mode=ro`と`PRAGMA query_only=ON`を併用し、書込み試行が失敗することをテストする。
