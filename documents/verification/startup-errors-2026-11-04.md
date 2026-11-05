# BSM 起動エラー確認（2026-11-04）

## 追補: BSM移植と残件修正

後続依頼「BSMの世界観に合わせて移植、英国は他ブランチのLONコンテンツと合わせる」に対応。以下の旧調査記録の未移植問題は、復元・新実装によって対応した。

- `feature/london_three_sovereignties` は既に現ブランチの祖先。mergeは追加せず、導入済みLONシナリオを統合基準とした。
- 英国本体はBSMの`GBR`。設計書を基に41方針・10同意イベント・5再交渉決定・6国民精神を実装。LONの既存47イベントを維持し、国勢調査・憲法会議・帰還・北部協議へ接続。領土取得は対仏の明示的受諾のみ。
- インドは、バニラ導入前の既存BSM55方針を復元。全DLC構成で使用し、旧IDと政治分岐を保持。DEU/NTS等のBSM国家参照、自治/独立の当事国scope、SAEC招待の同意処理を修正。
- 置換前の未移植ツリー・ローカライズは各移植記録の`previous-*`等へ原文保全。空の代替効果や未定義架空国家の追加でログを隠していない。
- 日本語localisationの重複を整理。専用・動的な既存説明を優先し、異文はコメントまたは移植前snapshotに保全。バニラoverrideは`localisation/replace/`へ集約。BOM保持・キー欠落を検証。
- `buildings.txt` はEOFの余分な改行だけ除去。バックアップとのバイト比較で全74132レコード不変を確認。通常userdirのキャッシュ・セーブには触れず、隔離userdirでキャッシュを生成/再読込する。
- スペインの既登用人物の重複recruitを除去。アンドラの既存人物は履歴で登用し、方針ではpromoteする。スペインの初期師団名グループを利用可能な共和派グループへ修正し、モナガスの既存航空配備に必要な基地を追加。
- ラスベガスの初期航空隊が参照する設計を既存Patrol Fighter仕様から作成。機数60は保持。
- 初回統合起動で見つかったESP/FRAのAI戦略とNTS triggerの比較演算子9箇所も現行辞書に合わせた。

限定検証: `verify_britain_bsm.py` PASS、`verify_london_scenario.py` PASS、INDの55方針ID/参照/自治scope検査PASS、map不変条件7項目PASS。全体`validate_mod.py`は0 errors / 52 warnings。これらの静的/model検証は、全方針の実プレイ確認を意味しない。

実起動の最終結果は同ディレクトリの`startup-world-port-runtime-2026-11-04.json`へ保存する。検証用起動スクリプトでは2回目に前回のsetup.logを拾う偽陽性を発見したため、再起動前にログフォルダを退避し、新しい起動完了行だけで判定するよう修正した。

最終結果: 同一の新規userdirでGBRを指定した起動が2回とも完走（43159ms / 50327ms）。両回とも`error.log`は0行、`text.log`のlocalisation衝突は0件。両方のnaval cacheファイルが初回に生成され、2回目はそれらを保持して起動。2回目のプロセスは終了せず残した。通常userdirと実セーブは変更していない。

詳細: [英国移植](britain-bsm-port-2026-11-04/README.md)、[インド移植](india-port-2026-11-04/README.md)。旧ツリー進行中のセーブ移行は未対応。各方針の実操作・全同意/拒否分岐・長期AI・マルチプレイ・セーブ再読込は未検証。

以下は初回修正時点の履歴であり、追補後の残存状態を表すものではない。

## 条件

- ブランチ: `fix/startup_errors_20261104`（commit/pushなし）。
- インストール済みHOI4を `-debug -userdir=<一時フォルダ>` で起動。
- descriptorのpathはこのcheckoutの `bakasekai`。通常userdirと既存セーブは編集しない。
- 通常userdirの古いログはSSWのものだったため、診断根拠から除外。
- 初回はSteam未起動でDLC/装備画像のエラーが混入。Steam起動後の再検証を基準とする。

## 修正

- `bsm_ind_decisions.txt`: script先頭のBOMを除去。localisationのBOMは変更しない。
- `NTS.txt`: `greater_than_equals` を現行辞書の `greater_than_or_equals` へ修正。
- `_bsm_national_currency.txt`: collection反復を現行ドキュメントの `input = { input = collection:... }` へ修正（9箇所）。
- ESP/NSIの未定義海軍補正を `naval_defense_factor` / `naval_speed_factor`、FRAの修理補正を `repair_speed_factor` へ修正。値は保持。ESP/NSIは指揮官能力の割合補正という未対応指定から、艦隊の防御/速度補正になる。
- `uk.txt`: 支持率比較22箇所をMODの `communism_ideology` / `fascism_ideology` に統一。
- `spain.txt`: `ESP_caribbean_assembly` と `ESP_operation_return` の排他を対称にする。
- `ENG_scripted_effects.txt`: 導入済み英国方針が呼ぶ `ENG_viceroy_reduce_autonomy_effect` を、インストール済みゲームの同名定義から復元。

## 検証

- `python3 tools/validate_mod.py`: PASS、0 errors / 139 warnings。
- `git diff --check`: PASS。
- 初回はsetup.logの起動完走53356ms、ゲーム画面の描画を確認。
- Steam正常条件の修正後起動: setup.logの起動完走56839ms。
- 英国副王効果を含む最終起動: setup.logの起動完走52960ms。起動後のerror.logは704行（複数行メッセージを含むためエラー件数ではない）。
- 最終修正の確認ログ: `/tmp/bsm-startup-final.json` が指す一時userdirの `logs/error.log` / `logs/setup.log`。
- 決定、NTS比較、collection反復、未定義modifier、旧イデオロギー、非対称排他、英国副王効果のエラーが最終ログから消失。
- 各方針の完了・通貨一覧の操作結果・バランス・マルチプレイは未検証。

## 未解決

起動完走はエラーログ全解消を意味しない。インド・英国のバニラ依存未移植が残る。

- `india_goe.txt` はIND向けだが、バニラのRAJ人物・国民精神・動的補正・決定・MIO・藩王国・効果を参照する。
- `HYD` 等は未定義。BSMの `RAJ` はラージプーターナー、`MYS` は「謎」であり、バニラ依存を一括追加すると別国家へ誤適用される。
- バニラ側の主要所有元は `RAJ_GOE_scripted_effects.txt`、`british_raj_goe.txt`、`GoE_dynamic_modifiers.txt`、`characters/RAJ.txt`、`decisions/RAJ_GOE.txt`、`RAJ_names_divisions.txt`。イベントまで推移依存がある。
- 英国も共有方針、国民精神、決定、労組ミッション等の参照切れがある。
- その他、ESPのruntime recruit_character警告、localisation衝突、map/buildings.txtのEOF次行を指す引数エラーが残る。buildings.txtは全74132行とも7列であり、原因は未確定。mapデータは変更していない。

未定義IDの捏造、空効果による隠蔽、ツリー削除は実施しない。残る移植には、BSMのどの国家・人物・地域へ対応させるかの設計が必要。
