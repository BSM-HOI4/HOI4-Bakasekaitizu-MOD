# HOI4 1.18以降の累積互換性確認 (2026-10-29)

## 対象と結論

- 作業branch: `feature/_system_race_removal`。既存ID・世界観を維持。
- 実行本体: Steam macOS `Operation Postern v1.19.4.0.48d6`。`launcher-settings.json` の rawVersion は `1.19.4.0`。
- `supported_version="1.19.*"` は元から設定されており、この記載だけで互換性を判定していない。
- 1.19.4で隔離起動、メニュー、国家選択、新規ゲーム、将校団の実表示まで確認。全国家・全DLC組合せ・長期進行の保証ではない。
- 1.18本体はこの環境にないため、1.18での同時動作・旧セーブ移行は未確認。1.18以降の累積変更が不足しているという懸念に対して、現行実装との比較と実行ログで検査した。

## 修正した累積不足

| 対象 | 旧状態 | 今回の修正 |
|---|---|---|
| 将校団 | `countryofficercorpview.gui` が `countryoccupationview.gui` のバイト一致コピーで、将校団root自体がない | 現行将校団GUIを正しいファイルへ復旧。Shift+Eで実表示確認 |
| 貿易 | 自動輸入・予算・輸入優先順位がない旧レイアウト | 現行レイアウトへ更新 |
| 建設 | 修理優先順位ダイアログと起動ボタンがない | ダイアログ・entry・ボタンを追加 |
| 国家方針 | 現行C++が要求するmini_mapがない | mini_map_clip以下とカメラ枠・handleを追加 |
| ショートカット | 研究・国家方針の複数shortcut、Ctrl+Tab系がない | 現行widget追加。BSMの既存配置は維持 |
| 基礎GFX | 現行にある12sprite/8bitmapfontがない | 不足20定義を追加。既存Win95参照を維持 |
| ドクトリンGFX | 特殊部隊等の6spriteがない | 現行定義6件を追加 |
| Radar defines | RADAR_RANGE_*がNDefines直下でNBuildingsへ適用されない | 既存値10/10/1000を保持してNBuildings配下へ修正 |
| 旧海軍defines | 現行で宣言されない5keyへ代入 | 値を残して存在guard。現行にない性能効果を適用済みとは扱わない |
| SIA装備画像 | 装備graphic DBの2sprite名がDLC実名と不一致 | DLC実定義の`GFX_SIA_gwtank_medium`/`GFX_SIA_basic_light_spaa_medium`へ修正 |
| 作戦の流入 | focuses/effectsを置換する一方、未採用のvanilla SIA作戦が流入し無効参照 | 既存の作戦5ファイルを正本とする`replace_path="common/operations"`を追加。空effectによる隠蔽はしていない |
| map/buildings | 全74131レコードは正常な7列だが、終端改行を空74132行として検出 | 最終改行のみ除去し当該エラー消失。さらにstate1112既存rocket_siteと同座標/方位のrocket_site_spawnを追加。元74131レコードを保持し、計74132レコード |
| 通知配置 | x822/918, y38固定でtopbarと重なり、右余白465とも競合 | 通常/拡張ともx12,y86へ。バー下の独立行、右余白140で横方向に折り返す |

## ドクトリンの新旧体系

- `common/doctrines` は22ファイルあり、folder/grand doctrine/track/subdoctrine方式は既に導入されている。単に旧研究ツリーだけが残った状態ではない。
- 現行との差で `peoples_war` と `dispersed_operations` が不足していたため、独立した新subdoctrineを追加。peoples_warの政府条件はBSMの `communism_ideology` を使い、このMODにないvanilla INS国家方針への例外参照は取り込まない。
- 陸軍3grand doctrineはBSMの `new_superior_firepower` / `new_grand_battleplan` / `new_mass_assault` を維持。特に `_bsm_tech_level.txt` が `new_mass_assault` を参照するため、現行vanilla名へ機械的に改名したり同じ選択肢を二重追加しない。
- `common/technologies` の `doctrine = yes` は `nsi_tech.txt` の国家方針で解禁する隠し技術3件。一般の陸軍旧ドクトリンツリーとは区別する。海軍の `xp_research_type = navy` は装備/補助技術にも使われるので、これだけを旧ドクトリン扱いして削除しない。
- BSM用タグ置換と数値調整があるため、22ファイル全体をvanillaで上書きしていない。新旧研究効果の全国家・全経路での二重適用、既存セーブの移行、現行vanilla全バランス変更の採用は未確認。

## 検証

- `python3 tools/validate_mod.py bakasekai`: 0 errors / 139 warnings (既存の重複scripted effect/trigger等を含む)。
- 編集したGUI/GFXの引用文字列とコメントを除いたbrace解析、追加widgetの存在、`git diff --check` を実施。
- `-userdir=<temp>` と隔離 `dlc_load.json` / ローカルmod descriptorで起動。ユーザーの通常settings・playset・セーブを変更していない。
- 初回起動のerror.logはSIA作戦・SIA画像・map終端等の8行。修正後のメニュー到達時点は既存localisation collision通知1行のみ。
- 新規ゲームで追加確認したstate1112 gun emplacementは既存rocket_site座標からspawnを追加。NSIは既存Elite Guardの砲兵supportに必要なgw_artillery=1を付与。GBRはTown/Leander設計そのものを増やさず、既存船体解禁のbasic_ship_hull_cruiser=yesを他の技術と同じ1へ補正。最終再起動で再確認する。
- LVEのsmall_plane_airframe_0初期variant不足は、根拠不明の架空設計を新作せず残件。
- 国家方針のmini_map欠落は新規ゲーム検査で発見し修正。1024x768新規ゲームで当該エラーが消えたことを確認。最終再起動の結果は下記追記で記録。

## 実画像

- `verification/hoi4-1194-2026-10-29/country-selection.png`: 1280x720で国家選択 (初回UI検査時点)。
- `verification/hoi4-1194-2026-10-29/officer-corps.png`: 新規ゲームでShift+Eの将校団実表示。
- `verification/hoi4-1194-2026-10-29/mainmenu-final-1024x768.png`: 最終元bg版の低解像度main。
- `verification/hoi4-1194-2026-10-29/singleplayer-final-1280x720.png`: 最終SPの縦3ボタンと実X印。
- `verification/hoi4-1194-2026-10-29/loading-actual-1280x720.png`: 最終独自ロード窓・実ステータス/進捗・小話。

## 追加検証の経過

- 1024x768 (gui_scale=0.8) の新規ゲームで通知8個がバー下の横一列に収まることを実画面で確認。元のx918/y38配置との重なりは解消。
- 1280x720 (gui_scale=1.0) の最終mainは元bg.pngを使用し、終了ボタンまで画面内に表示。`verification/hoi4-1194-2026-10-29/mainmenu-final-1280x720.png`。
- 検証画像は撮影時点の状態。ユーザーの画面操作が入った画像は`politics-1024x768.png`として区別し、アラートの証跡とは扱わない。

## 最終起動 (ロード画面・メニュー最終版を含む)

- 隔離userdir: `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-1194-acceptance-sqpofbpz`。
- 起動完走・メニュー到達、1024x768のmainで終了まで表示を確認。`mainmenu-final-1024x768.png` が最終元bg版。
- `dlc-welcome-popup-1024x768.png` はDLC案内popupであり、ロード画面ではない。この1024x768起動ではロード状態窓の撮影を逃した。次の1280x720起動で実ロード画像を取得し確認した。
- `mainmenu-compact-comparison-1024x768.png` / `singleplayer-large-comparison-1024x768.png` は途中版の比較画像であり、最終メニューの証跡ではない。
- メニュー到達時のerror.logは既存localisation collision通知1行のみ。SIA作戦/装備画像/map終端/新subdoctrineについて追加起動エラーなし。

## 最終確定結果 (1280x720 / gui_scale=1.0)

- 隔離userdir: `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-1194-ui-proof-i3v527z6`。通常の設定・playset・セーブは変更していない。
- 起動: `Startup time: 40138ms`、メニュー到達。error.logは既存localisation collision通知1行のみ。
- ロード画面: 最初のスプライト読込段階はvanilla窓、その後の海図距離計算中は独自Win95窓へ切り替わる。青タイトル、実際のロード文言、進捗バー、小話を実表示確認し、`loading-actual-1280x720.png`に保存。
- main: 元bgのまま終了まで表示。1024x768/1280x720の最終画像あり。
- SP: 最終520x300ダイアログ、縦3ボタンとX印がすべて画面内。`singleplayer-final-1280x720.png`で実表示確認。
- 最終SPの新規ゲーム操作は、CUAのRetina画像座標とMacウィンドウboundsの不整合で `noWindowsAvailable` が発生し、最後まで再実行できなかった。UIの画面外欠落とは区別する。
- 途中の新規ゲームでは通知独立行と将校団の実表示、mini_mapエラー消失まで確認済み。最後に追加したNSI砲兵技術・GBR船体技術の数値修正・state1112 spawnの、新規ゲームでのエラー消失は未確認。これらを実機検証済みとは扱わない。
- 確認手順: 最終SPから新規ゲームを開始し、隔離`logs/error.log`で `no gun emplacement defined for state 1112` / NSI artillery locked / GBR cruiser2 variantエラーの有無を確認する。LVE空軍variantは未解決の既知残件。
- 全国家・長期進行・旧セーブ・1.18実行互換性は未確認。単なる対応版文字列変更ではなく、今回確認した具体的な差分と実行結果を上記に限定して報告する。

## Windows 95 Setup構図・読込文言の追加改訂

ユーザー提示のSetup構図を採用し、ロード画面を青い背景・中央Welcome面・左のMODブランド帯・下部進捗へ更新。読込ステータス23項目を日英で変更し、樹木は「世界に緑を植えています……」、海図距離は「七つの海の道のりを測っています……」などへ統一した。進捗・小話のエンジン接続は維持。

最新Setup版の1.19.4 / 1280x720 / gui_scale=1.0起動で背景・文字・行間・実ステータス・実進捗を視認し、43.628秒で完走。既存localisation collision通知1行以外のエラーなし。1024x768は今回のSetup外形の静的確認のみ。新規ゲーム/OOBの未確認範囲は上の記録から変更していない。

- 実画像: `verification/hoi4-1194-2026-10-29/loading-setup-actual-1280x720.png`
- 実進捗比較: `verification/hoi4-1194-2026-10-29/loading-setup-progress-1280x720.png`
- 詳細: `verification/hoi4-1194-2026-10-29/setup-loading-verification.md`

## 後続UI改訂の最終結果

以下は、上の各撮影時点からさらに変更した現在のUIについての結果。

- 初期ロードは正規の`interface/load_screen.gui`/`.gfx`/`load_screen_font.gfx`へ統合。1280x720/GUI1の起動で、撮影できた最初のGUI読込段階（進捗約7～10%）からイベント読込段階まで同じSetup画面を確認し、47.921秒で完走。DATABASE/HISTORYの短い最初期は撮影できず、全初期フレームを実証したとは扱わない。`bootstrap-loading-verification.md`参照。
- Startメニューは元の青い背景素材の画素を保ち、426x384へ改装。SNSを182x64の2段グリッドに収め、主操作・リンク・終了を整理。1024x768/GUI0.8と1280x720/GUI1で表示、SでSP、Escでmain復帰を確認。`compact-startmenu-verification.md`参照。
- 国家選択は1200x690、明灰色の立体枠・紺見出し・白本文・黒字へ変更。肖像と旗の元画像、262箇所のwidget名、国家設定を維持。1280x720/GUI1で謎と日本への国家情報更新を確認し、1024x768/GUI0.8の最終起動でもカード・下部本文・両ボタンが画面内に収まることを確認（40.115秒）。`country-select-win95-verification.md`参照。
- 日本語の22ideology groupについて、政府説明の不足キーを既存の説明／和名へのaliasで補完。基本政体は実表示で解消、日本の最終補完は静的確認に限定。IDや政体データは変更しない。
- 各最終起動のerror.logは既存localisation collision通知1行のみ、新規GUI/GFX/fontエラーなし。国家選択の下部ボタン直接クリック・履歴スクロールはCUA制約で未確認。chooserのBACKと全体のMAIN_MENU_BACKは別の標準契約であり、Escでmainまで直接戻るとは扱わない。

現在の実画像は`startmenu-compact-final-1024x768.png`、`startmenu-compact-final-1280x720.png`、`bootstrap-setup-early-1280x720.png`、`bootstrap-setup-late-1280x720.png`、`country-select-win95-final-1024x768.png`、`country-select-win95-final-1280x720.png`。全て同じ`verification/hoi4-1194-2026-10-29/`内に保存。1.18実行・旧セーブ・全国家長期進行・OOB修正の最終新規ゲーム再確認という上記の未確認範囲は変わらない。

## 主要GUIスキン拡張（2026-10-30）

174GUI/240chrome/57fontへ拡張し、177GUI/GFX syntaxとmod validator（0 errors/139既存warnings）、参照閉包/再生成/機能token保持を検証。240GFXの契約・192alpha・font source metricsも独立照合した。詳細は`WIN95_MAJOR_GUI_2026-10-30.md`、`verification/hoi4-1194-2026-10-29/major-gui/`を参照。

### ロック解除後の最終新規ゲーム・実表示確認

この結果は、上の撮影時点で未確認としていた新規ゲーム再確認を更新する。

- 同名アプリを取得した際のSSW画像は証跡から除外。通常SSWへキー・クリック・終了操作をせず、Baka専用の新しい隔離userdirを使用した。Active Mod Count1/バカ世界地図テスト版、descriptorの正本絶対path、固有menu/地図を照合してから入力した。
- 1.19.4 / 1280x720 / GUI1、BATの新規ゲームを開始。1936/1/1 12:00 pauseを保ち、政治・決定・研究・実外交・国際市場・貿易・建設・生産・配備・兵站・将校団・諜報・国家方針・設定・ロード等を実表示確認した。
- 明色面の白字、暗色見出しの黒字、C++が元IDへ戻すNoDLC政治背景、貿易neutral数値を修正。建設の`start_construction_entry`へエンジンが必要とする`repair_order_number_window/repair_order_number`を本体定義から補完し、missing-child反復エラーが消えたことを確認した。
- 外交の政体3行の行間を22pxへ調整し、最終v4再起動で重なり解消を確認。`major-gui/diplomacy-spacing-final.png`が最終証跡。
- **state1112 gun-emplacement spawn / NSI砲兵locked / GBR巡洋艦variantの旧エラーは再発しなかった。** メニュー到達だけでなく、新規ゲーム後のログで確認した。
- 残るログは既存localisation通知1行と、既知LVE `small_plane_airframe_0` variant/airwingの2行。根拠不明の架空機体設計を追加していない。GUIエラーは増えていないが、ゲーム全体のエラー0とは扱わない。
- 通常settings/playset/saveとゲーム本体は変更していない。1.18本体は環境になく、1.18・他の1.19 patch・旧セーブ・全国家/DLC組合せ・長期進行は未確認。今回の主要174GUIすべてについて低解像度を網羅した実証ではない。
