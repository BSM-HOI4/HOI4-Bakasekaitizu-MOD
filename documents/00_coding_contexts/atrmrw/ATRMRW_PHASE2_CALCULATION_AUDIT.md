# ATRMRW Phase 2 計算コード監査

- 状態: READ-ONLY監査完了、主要係数選択はユーザー承認済み・日本プロトタイプへ反映済み
- SSW固定コミット: `4bcb07d5c11f3c78c3383db393abc9bbbf4dbdc1`
- 対象: `HPCLC.py`、`gun_clc.py`、`gun_calc_settings.py`、`gun_calc_config.json`、`nsdb_tool.py`
- 実施日: 2026-08-02

## 1. 結論

SSWコードをファイル単位でコピーしてATRMRWの正本にしてはならない。HPCLC v3の純粋計算関数は転用候補だが、GUNCLCはコード・設定・文書の係数が矛盾し、NSDB helperは正規化不足と計算式の簡略化を含む。Phase 2では「raw data」「正規化」「計算式」「ゲーム値丸め」を分離し、式ごとにversion IDを持たせる。

## 2. 転用範囲

| 元コード | 判定 | ATRMRW方針 |
|---|---|---|
| `calculate_base_strength_v3` | 条件付き転用 | `atrmrw_hp_v1`候補。入力単位と`ship_hull_type`対応表を明示し、回帰ケースを固定する |
| `calculate_base_org_v3` | 条件付き転用 | HOI4艦艇で組織値を使用する接続先を確認するまで計算補助値扱い |
| era multiplier | 条件付き転用 | 年代境界を表データ化し、BSM世界観補正と分離する |
| `calculate_hp_v2` | 互換参照のみ | 新規ATRMRW値には使用しない |
| `gun_calc` | 採用済み | 固定コミットのtracked configを明示入力として採用。現コードの無条件コピーは禁止 |
| `gun_role_ratio` | 転用候補 | 閾値表をschemaへ移し、境界テストを追加する |
| endurance変換 | 転用 | `target_naval_range = endurance_nm × 1.852 ÷ 2`を式ID付きで実装する |
| NSDB検索・raw clean | 参考転用 | DBをread-only入力にし、source URLとraw cellを保存する |
| SRM正規表現parser | 不採用 | ネスト括弧・コメントを扱える既存ATRMRW parserへ統合する |

## 3. 確認した式

### 3.1 HPCLC v3

```text
area = length_m × breadth_m
raw_strength = 1100 × sqrt(displacement_t / (displacement_t + 45000))
             + 300 × sqrt(area / (area + 15000))
             + 50
hull_mult = 0.85 + 0.10 × ship_hull_type
max_strength = max(20, raw_strength × hull_mult × era_strength_mult)
```

ATRMRWの正式対応表は、小艇0.3、軽艦／潜水艦0.5、フリゲート／支援艦0.8、巡洋艦／空母1.5、主力艦2.0とする。これは2026-08-02のユーザー承認値である。

### 3.2 航続距離

SSW policyと`nsdb_tool.py`は一致している。

```text
endurance_km = endurance_nm × 1.852
target_final_naval_range = endurance_km ÷ 2
```

最終値は船体base、燃料、機関種別、機関出力、他moduleの合算後にこの目標へ近づける。入力文字列と抽出した巡航速力を保存する。

### 3.3 速力

SSW policy:

```text
target_speed = (maximum_speed_kn + cruising_speed_kn) ÷ 2
cruising_speed_knが不明なら maximum_speed_kn × 0.80
```

現`nsdb_tool.parse_speed`は最初の数値しか返さず、`23.6 / 8`から最大速力23.6だけを採るため、この要件を満たさない。ATRMRWでは水上／水中速度の区別もschemaで保持する。

## 4. 確認した矛盾・欠陥

| 重要度 | 箇所 | 事実 | ATRMRW対応 |
|---|---|---|---|
| 高 | GUNCLC係数 | policy §5.3、`gun_clc.py`、tracked configの係数が一致しない | 固定コミットのtracked configを正本として採用し、formula IDと設定hashを記録する |
| 高 | GUN設定初期化 | `gun_calc_settings.py`の`_TEMPLATE`と`_DEFAULTS`が不一致。設定欠落時はファイルを書き、環境で結果が変わる | import時書込みを廃止し、checked-in設定を必須read-only入力にする |
| 高 | build cost | policyは`full_load / 15**((year-1800)/10000)`、`nsdb_tool estimate`は`full_load / 15` | policy式を候補正本とし、近傍艦比較とユーザー承認を必須にする |
| 高 | HPCLC期待値 | 再計算計画はIowa v3を約1944と記すが固定コード実行値は1110.1 | 文書値をgoldenにせず、採用式と期待値を同時承認する |
| 高 | NSDB raw品質 | 同名異種艦、複数値連結、寸法種別、潜水艦の水上／水中値が同一cellに混在 | class名だけで自動確定せず、country/type/source_urlを含む一意選択とreview flagを要求 |
| 中 | GUN入力検証 | `T_count`の正数検証がない | `T_count > 0`を必須化する |
| 中 | GUN役割比率 | 13cm・8cm等はLG+HGが1未満で、未配分分の意味が文書化されていない | 意図的な非砲戦寄与か欠落かを確定してから転用する |
| 中 | HP寸法 | `Length`にpp/wl/oaが混在。最初の数値採用ではHPCLC例とズレる | 原則OA、なければWL、次にPPを選び、選択根拠を保存 |
| 中 | source URL | 表示時だけmirrorへ変換し、raw DBは旧URLのまま | raw URLとnormalized mirror URLを両方保存 |
| 中 | テスト | 対象コードに独立した自動テストがなく、`__main__`のprint harnessのみ | 固定fixture、境界値、式hash、期待値テストをATRMRW側で追加 |

GUNCLCについて、固定コミットのtracked configは攻撃力指数`0.70/0.60/0.60/0.50/0.25`、除数650等を使う。一方policy §5.3は`0.55/0.35/0.60/0.70/0.25`、除数15等を記載する。これは丸め差ではなく別式である。

ATRMRWへ格納したconfigは、固定コミット原本から`_説明`・`_計算式`等の説明metadataだけを除いた派生物である。原本SHA-256は`bf5c7f164e89013a916195a155aa8c49f8b185517b44d2767e7c12c3b4b460ce`、派生config SHA-256は`8ac721425d0c6aabb11bb47c57339a06b2e7914dc84da4fef6018ad5be5e3070`。数値係数とrole閾値は同一で、変換内容をformula manifestへ記録する。

## 5. プロトタイプ候補のNSDB存在確認

READ-ONLY DB検索で次を確認した。

| 候補 | NSDB class | 判定 |
|---|---|---|
| 大和型 | `YAMATO1942) Class` / battleships / Japan | 寸法・排水量・速力・航続・乗員あり |
| 高雄型 | `TAKAO Class` / heavy-cruisers / Japan | 同名旧式巡洋艦もあるためtype/source URLで識別必須 |
| 吹雪型 | `FUBUKI1932) Class` / destroyers / Japan | 基本諸元あり |
| 赤城型 | `AKAGI Class` / aircraft-carrier / Japan | 同名patrol craftが複数あるためtype/source URLで識別必須 |
| 伊十五型 | NSDB上は`Otsu-GataB1`系 | 日本語通称からの単純LIKE検索不可。source URL・艦名表との照合が必要 |

SSW固定コミットには大和・高雄・赤城の固有hull/variantが存在する。吹雪はgenerated hull localisationを確認したが、同じvariant生成経路かは追加確認が必要である。

## 6. DB版の固定

指定SSWコミットには`nvpda-db/NSDB.db`が存在せず、`NSDB_new.db`だけが存在する。現行SSWの`NSDB.db`は`/Users/eightman/dev/data/nsdb/NSDB.db`へのシンボリックリンクであり、監査時点で次の版だった。

```text
CLASS rows: 11144
SHA-256: 6d5418efa26f8c73afb386b8eb3f0dea47cf65fa03303d3c0f8c17e52122f1ad
```

固定コミット側`NSDB_new.db`は別版であり、調査結果ではCLASS 10921行だった。ATRMRW成果物はDBをリポジトリへ複製せず、行数・SHA-256・取得日時を入力manifestへ記録する。

## 7. ユーザー決定と残課題

1. **決定済み:** GUNCLCは固定コミットのtracked configを正本とする。
2. **決定済み:** HPCLC対応表は§3.1記載のユーザー承認値とする。
3. **決定済み:** 燃料・機関は史実方式を先行し、架空方式は後続フェーズとする。
4. **残課題:** 史実燃料方式のTier、研究、転換費用。
5. **残課題:** BSM固有超技術動力の比較対象と性能上限。
6. **残課題:** LG/HG役割比率の未配分分を意図的な損失として維持するか、合計1へ正規化するか。
