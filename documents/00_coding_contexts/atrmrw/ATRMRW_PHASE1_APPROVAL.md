# ATRMRW Phase 1 承認記録

- 状態: ユーザー承認済み
- 承認日: 2026-08-02
- 機械契約: `ATRMRW_PHASE1_SLOT_CONTRACT.json`
- 全船体割当: `ATRMRW_PHASE1_HULL_PROFILE_MAP.csv`
- 検証: `python3 tools/atrmrw/validate_slot_contract.py`

## 1. 承認内容

ユーザー回答`1ok`～`5ok`と次の補足を契約の根拠とする。

- 艦種はSSWと同期する。
- スロット数は船体の物理的大きさで決め、最大36とする。
- 船体構造等を表示するため、最小も約9枠を確保する。
- SSWのhidden運用は継承せず、全枠をGUIへ表示する。
- GUNCLCは固定コミットのtracked configを正本とする。
- HPCLC係数は小艇0.3、軽艦／潜水艦0.5、フリゲート／支援艦0.8、巡洋艦／空母1.5、主力艦2.0とする。
- 燃料・機関は史実方式を先行し、架空方式は後続フェーズとする。
- 日本海軍プロトタイプは大和型、高雄型、吹雪型、赤城型、伊十五型とする。

## 2. 標準profile

SSWのroleと物理サイズを分離し、船体を次の7段階へ割り当てる。

| Profile | 枠数 | 主対象 |
|---|---:|---|
| Maximum | 36 | 大型空母、超大型戦艦、大型戦闘空母 |
| Capital | 30 | 通常戦艦・巡洋戦艦・正規空母 |
| Large | 24 | 重巡洋艦、前弩級、小型空母、大型補助艦 |
| Medium | 18 | 軽巡洋艦、大型駆逐艦、護衛空母、巡洋潜水艦 |
| Escort | 15 | 駆逐艦、フリゲート、航洋潜水艦 |
| Coastal | 12 | 沿岸艦艇、沿岸潜水艦、小型支援艦 |
| Minimal | 9 | 特殊潜航艇、魚雷艇、哨戒艇、小型掃海艇 |

排水量の目安は`≤500 / ≤1,300 / ≤4,000 / ≤10,000 / ≤20,000 / ≤40,000 / >40,000t`とする。ただし航空艦は原則1段階上、潜水艦は独立したサイズラダーで割り当てる。艦種名だけでprofileを自動決定せず、船体台帳に個別根拠を保存する。

## 3. 全可視契約

```text
total_slot_count
  = editable_slot_count
  + fixed_visible_slot_count
  + locked_visible_slot_count

hidden_slot_count = 0
```

`ship_type_slot`、機関方式、機関出力、燃料、船体構造、装甲、センサー、史実武装を通常の物理枠として表示する。役割、機関、燃料、装甲、センサー、史実武装・overflowは`editable`、船体構造だけを交換不能な`fixed_visible`とする。GUIのfixed/custom区分は座標アンカー群であり、編集可否とは独立する。SSWの旧hidden武装は同用途・同口径・同zone単位の可視batch moduleへ変換する。

## 4. SSW同期の意味

- `ship_type_slot`のrole taxonomyを同期する。
- heavy / cruiser / light / frigate / carrier / light carrier / submarine / battle carrier / cruiser carrier / submarine carrier / tender / tanker / repair / surveillance / special support / craft等のarchetypeを同期対象とする。
- roleは任務分類、profileは物理サイズ分類であり、一対一対応させない。
- 34,000t級大型巡洋艦や23,000t級潜水艦等は、archetype名ではなく物理規模で上位profileへ割り当てる。

## 5. 現行BSM 85船体の移行割当

`ATRMRW_PHASE1_HULL_PROFILE_MAP.csv`に全85船体を割り当て済みである。ただし現行BSMの汎用船体には排水量原典がないものがあるため、全行を`provisional_displacement_review=yes`として記録した。これは参照欠落を示すreview flagであり、Phase 3の5艦級プロトタイプの承認を妨げない。

旧`ATRMRW_PHASE1_*_PROPOSAL`成果物は、ユーザー補足前の36/11/9/7/3/0案を示す監査資料であり、実装契約として使用しない。
