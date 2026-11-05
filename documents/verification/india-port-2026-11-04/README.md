# IND 独立シナリオ復元・移植

## 原因と方針

`67f29a6df` で既存のBSM独立シナリオ55方針がバニラのIndia/TfVツリーに置換され、同時に未移植のGoEツリーが追加されていた。イベント・国民精神・日本語文言は旧BSM版のまま残り、決定だけがGoEの方針IDへ向けられていた。

`67f29a6df^:bakasekai/common/national_focus/india.txt` のBSM版を復元した。55個のIDと政治3路線・独立後の行政/工業・SAECの分岐を保持し、DLC非依存で選択する。元のGoE/TfVソースは `previous-vanilla/` に原文保全した。GoE追加分に独自のBSM方針は無かった。

## 世界観・機能の整合

- `RAJ` はラージプーターナー、`MYS` は「謎」なので、未移植バニラの藩王国効果を流用しない。
- ハイデラバードは既にIND領であり、旧BSM方針の国内行政統合として説明を修正。
- 南カシミールはIND、北カシミールはNTS。交渉相手をPAKからNTSへ変更し、領土の強制移転を行わない。
- ドイツへの独立支援要請はゲルミヤン侯国の`GER`でなく`DEU`へ送る。
- 自治承認は宗主国側で `set_autonomy target = FROM` を実行。完全独立を承認した場合は実際に `end_puppet` を実行して独立フラグ・cosmeticを揃える。
- 決定5件を復元したIND方針IDに接続。世俗憲法で分割問題の解決フラグを立てる。
- SAECは既存経済同盟の仕組みを使い、SRL/BRM/NEPも承認イベントで招待する。独立政府が存在しない国の招待方針はbypassできる。遅延中に従属・戦争・他経済圏加入が発生した場合は承認不可。
- PAKが既に存在する場合に政権を上書きしない。解放で他国NTSの領土を強制的に移転しない。

## Localisation

- 独自方針55本と説明を保持。重複したイベント101キーを `bsm_ind_events_l_japanese.yml` に集約し、旧文言は `previous-localisation/` に保全。
- RAJコピーからバニラと同値の1736定義を除去。独自216定義は保持し、バニラとの差分7定義は正規の `localisation/replace/IND_legacy_l_japanese.yml` で保持。
- `IND_ADJ` / `IND_DEF` は同値の正本 `map/bsm_countries_l_japanese.yml` に集約（旧行はコメント保全）。
- 全元キーが現在のMODまたはインストール済みバニラに存在すること、編集したYMLのBOMが1個であることを検証。件数は `localisation-migration.json`。

## 検証

- `python3 tools/validate_mod.py`: PASS、0 errors / 52 warnings（並行作業を含む時点の全体結果）。
- 対象スクリプト5ファイルの構文木parse: PASS。
- 旧BSM版と55方針ID集合が一致。全prerequisite/relative_position/排他・決定参照・イベント呼出し・方針日本語参照: PASS。
- 自治承認のROOT/FROM、独立処理、NTS外交相手、誤ったRAJ/MYS/HYD/GER国家scope不存在: PASS。
- `git diff --check`（IND担当ファイル）: PASS。
- 詳細は `static-validation.json`。実起動の最終確認は親タスク側で実施する。

未検証: 全55方針のキャンペーン完了、AIの長期挙動、外交承認の実操作、バランス、旧バニラ方針の途中セーブからの進捗移行。旧GoE/TfV方針の途中セーブを自動変換する処理は追加していない。
