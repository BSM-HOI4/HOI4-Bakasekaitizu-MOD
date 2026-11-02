# 主要GUIのWindows 95化（2026-10-30）

対象は `/Users/eightman/dev/hoi4/HOI4-Bakasekaitizu-MOD/bakasekai`、branchは`feature/_system_race_removal`。Steam本体1.19.4.0を参照し、既存のUI改装を主要画面へ拡張した。commit/pushは行っていない。

最終実確認は `Active Mod Count: 1 / バカ世界地図テスト版`、descriptorの絶対path、Baka固有のメニューと地図を照合してから操作した。ロック解除後に同名アプリから通常起動のSSW画像を取得した件は検証から除外し、SSWへキー・クリック・終了操作は行っていない。通常settings/playset/saveとゲーム本体は変更していない。

## 適用範囲

174個のGUI定義を対象に、現在249枚のchromeと57種類のfont cloneを生成した。上部バー白字化と生産・政治の追加整理は、下記および `WIN95_PANEL_LAYOUT_2026-10-30.md` を参照。MODに元からある同名GUIの編集を保ち、本体継承だけだった128ファイルは`interface/replace/`へ追加した。

| 領域 | 主な対象 |
|---|---|
| 政治・外交 | 政治、国情報、外交、決定、諜報・作戦・工作員、占領、権力均衡、戦争概要、和平 |
| 経済 | 生産、建設、貿易、兵站、国際市場と各取引子窓、州情報 |
| 軍事 | 陸海空軍一覧、配備、師団・装備・戦車・航空機設計、司令官・特性、将校団、戦域、戦闘・損害・軍歴 |
| 研究 | 研究、技術詳細、新ドクトリン、国家方針 |
| 現行機能 | 陣営、軍需企業、特別計画、襲撃、建物roster、キャリア |
| 操作・案内 | 設定、保存・読込、マルチプレイ、ロビー・チャット、イベント、通知、popup、音楽、主要共通操作部品 |
| MOD独自 | AS、Stellaris伝統、国情報等。手作りのWin95/98版Mine・EA・開始説明画面は維持 |

次の設定一覧で対象ファイル・保全する図像・純chromeの役割を明示している。領域間で同じGUIを参照するため、行数の和は174と一致しない。

| 設定ファイル (`tools/win95_themes/`) | GUI指定 | chrome指定 |
|---|---:|---:|
| `advisor_navy.json` | 0 | 0（font指定・別生成カード保全） |
| `contrast.json` | 0 | 9 |
| `custom.json` | 21 | 39 |
| `economy.json` | 41 | 63 |
| `features.json` | 37 | 33 |
| `military.json` | 47 | 102 |
| `panel_layout.json` | 0 | 11 |
| `runtime_fixes.json` | 0 | 29 |
| `supplemental.json` | 30 | 21 |
| `topbar_contrast.json` | 0 | 0（font指定22項目） |

## 見た目と保全

- 面は明灰色`#C0C0C0`、本文・入力欄は白、見出しは紺`#000080`。白/黒の立体枠、黒い本文、選択中は淡青の面と紺の枠を使用。
- 矢印・つまみ・閉じる操作を同じ意匠へ変更。汎用tooltipの2素材は淡黄`#FFFFE1`と専用黒fontを対で適用。他の専用tooltipすべてが淡黄になることは実証していない。
- spriteの元寸法、frame数、effect、borderSize、animation指定を保持。枠の中央の透明穴も保ち、肖像や旗を覆わない。通常/選択/無効frame、および別IDの艦隊`*_hl`を描き分ける。
- 国旗・肖像・装備・地図・設計図・写真・議席数・進捗バー等の意味を持つ画像を保全。赤い無効stampを含む決定行、戦場地図や空景を焼き込んだ背景も保持し、周囲の枠を変換する。このGUI変換処理は元の内容画像を上書きしない。
- 元の青いmain menu素材、コンパクトStartメニュー、国家選択、Setupロード、既存Win95/98テーマのfontは保全。ゲームルール・国家設定・既存ID・ショートカットは変更しない。sprite/font参照以外の変更は、建設の必須child補完、外交3座標、生産・政治の追加整理に伴う幅/行間/配置と4つの速度用背景。追加整理の前後でも既存widgetの名前・階層・callbackを保持し、変更値を検証記録へ保存した。
- C++が明色の親へ合成する研究詳細・政治党名・通知・軍歴等の本文は、根拠を確認したrootだけ黒字にする。暗いcounter/HQ/status欄に汎用fontの黒を一律適用しない。

## 再生成と記録

`tools/generate_win95_major_gui.py --plan`は変更前の一覧、`--apply`は適用、`--check`は生成済み画像・GFX/font・GUI固定点・参照閉包・GUI機能tokenの照合を行う。Pillowが必要。

- 定義: `bakasekai/interface/_bsm_win95_major_gui.gfx`、`_bsm_win95_major_gui_fonts.gfx`
- 新素材とmanifest: `bakasekai/gfx/interface/win95/major/`
- tooltip再生成: `tools/generate_win95_tooltips.py` / `--check`
- 本体GFXに元からある外側閉じbrace欠落は、読取時に完結した個別spriteだけを利用する。本体は変更せず、生成するGFXは厳密に閉じる。
- 適用前の既存46 GUIの一時退避: `/tmp/bsm-win95-major-before-20261030`。既存編集を保持した状態の退避であり、Gitへのcommitではない。

## 検証結果

- 主要変換時点の174 GUIを適用前と照合。sprite/font参照と、child補完・外交3座標以外の全tokenが一致。PASS。後続の生産・政治整理は独立した変更記録と配置検査で区別する。
- 177 GUI/GFXの既存syntax validator: PASS。
- `validate_mod.py`: **0 errors / 139 warnings**。警告数は今回前の既存値と同じ。
- major generator再生成照合と、共有UI・frontend・国家選択・bootstrap loading・tooltipの5 generator検査: PASS。
- 上部バー白字化前の独立したsource比較で240 GFXのframe/effect/border等、192 alpha mask、57 fontの各source familyのglyph metrics/atlas指定、31言語override、艦隊の別ID選択stateを照合。明色37cloneの必要9palette keyと、暗色20cloneの元palette保持もPASS。追加した白字fontは下記の局所検査で元定義と照合した。
- 引用符内のbrace/comment、callback/位置変更の検出、透過穴、1px track、選択row、aliasの固定名を小さなfixtureでも確認。PASS。
- `git diff --check`: PASS。
- **追加整理前の1.19.4隔離起動・新規ゲーム**: 1280x720 / GUI1、Baka専用userdirでBAT新規ゲームを開始し、1936/1/1 12:00 pauseを維持。main/SP/国家選択/開始前設定、政治、決定、研究、実外交、国際市場、貿易、建設、生産、配備、兵站、将校団、諜報、国家方針、pause menu、設定、ロードdialogを実表示確認。現在の生産・政治の追加整理をこの実証へ含めない。
- 最終外交はPID83264、userdir `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-major-v4-han5v076`。`diplomacy-spacing-final.png`で3行の重なり解消を確認。外交行動、設定値変更、実セーブ読込は行っていない。
- state1112 spawn / NSI砲兵 / GBR巡洋艦variantの旧エラーは新規ゲームで再発しなかった。建設missing-childも修正後は再発なし。
- 新規ゲーム後のログは既存localisation通知1行と、既知LVE小型機variant/airwingの2行。画面右下の「3 errors」をGUIエラー消失と混同しない。LVEは設計根拠がないため架空moduleを補っていない。

陣営/MIO/特別計画/設計/戦闘等の深い変種の実表示は網羅していない。低解像度の実確認は従来のmain/国家選択の1024x768・GUI0.8と、今回の代表画面の1280x720・GUI1を区別し、174画面すべての低解像度実証とは扱わない。

1.18本体は環境になく、1.18実行・他の1.19 patch・旧セーブ・全国家/DLC組合せ・長期進行は未確認。

詳細は`verification/hoi4-1194-2026-10-29/major-gui/runtime-verification.md`、機械照合は同所`static-contract-verification.json`。同所`chrome-preview.png`は**素材の模式図であり、実ゲームのスクリーンショットではない**。

## 同時進行のポートレート作業との区別

別チャット「ポートレートの低解像度・減色実験」では、ユーザーが候補選択後に「本番適用」を指示し、793肖像を104x140・256色・Floyd–Steinbergで変換した。原本backupと実験記録は別作業側で保持している。作業ツリーのleaders画像差分はその別作業として保持し、このGUI変更の差し戻し対象には含めない。GUI側は肖像spriteの参照・配置を維持している。既存のtracked interface画像は今回上書きしていない。

## 実表示から修正した問題

Baka専用起動を再作成し、画面の固有ロゴとActive Mod/descriptor pathを照合してBAT新規ゲームを開始。通常userdir側のSSW画面は証跡に含めず、入力・終了していない。

v1で政治・研究・市場・貿易・建設・配備・兵站・将校団・諜報・国家方針・設定・ロード等を実際に開き、静的検証では検出できない文字色問題を確認。v2～v4で次を修正して再確認した。

- C++が政治背景をNoDLCの元IDへ差し替えるため、GUI aliasだけに依存せず、`GFX_pol_view_bg`/`GFX_pol_view_bg_no_dlc`を既存MODの政治GFXへ明示binding。元の全カスタム定義を保全する。
- 黒を焼き込んだ`jis30`等は白tintでも白くならない。研究・配備等の限定見出しを、白い字形がある既存`hoi_24header`/`hoi_20bs`等へ接続。該当widgetのfont family変更を明示し、他の字形・atlasは維持する。
- 明色font cloneだけ、inline色T/Wを黒、G/R/Y/H/O/g/Bを濃い意味色へ。元fontにないpalette keyも補完し、暗色面用white cloneのpaletteは維持。
- 貿易の数値はC++が白色を指定するため、対象数値widgetだけ既存の黒字atlas`bsm_16_blk`へ接続。neutralの0と数量が読め、正負の赤/緑も保持されることを実確認。
- 専用の工場数帯・産出量板・建設上部・兵站帯・設定入力・ロード一覧を明色化。obsolete師団行は通常の白と区別できるクリーム面/銅枠へ。刻印や写真を持つ部品は保全し、captured-commanders/agency/NF検索/load tab等のcaptionだけ白へ戻す。
- 開始前の旧BSM白文字は、その子rootだけ明示して黒へ。既存main/国選択/OE/EA/Mineの手製fontは保全。
- 建設の`start_construction_entry`直下に不足していた`repair_order_number_window`/`repair_order_number`を本体の正確な定義から復旧（canonical/replaceの2か所）。既存の別root内の同名childは代用にならない。
- 実外交の中段3背景を明色化。`party_name`/`ideology_name`/`elections`のyを-5/10/25から-4/18/40へ調整し、22pxの行間で3段に分かれることをv4再起動で確認。60pxの親枠内に収まり、肖像・旗・円グラフ・関係値・行動一覧を保持。

適用前退避46GUIと本体継承128GUIの合計174定義を独立照合。最終240GFX/192alpha/57font/31言語override、177GUI/GFX syntax、再生成固定点、差分空白はPASS。全体validatorは0 errors/139既存warnings。実表示の各撮影時点は`runtime-verification.md`、最終外交画像は`major-gui/diplomacy-spacing-final.png`を参照。

## 上部バーの数値・日時を白字へ（2026-10-30追加修正）

上部文字が黒すぎるとのユーザー指示により、政治力・人的資源・安定度・戦争協力度・陸海空経験値・核関連値・指揮力・工場数・陣営initiative・輸送船・燃料・補給・国際緊張・日時の17項目を白字へ変更した。`topbar_contrast.json`にwidget別の明示指定を保存し、再生成時にも維持する。

追加画像の3数値は、標準CP/緊張/政治力とは別のMOD独自の `COUNTRY_PO`（世論）/`COUNTRY_CD`（文化度）/`COUNTRY_ec`（統一通貨）だった。これらと通貨切替時の `nc_icon_text`、国旗下の丸い威信順位 `bsm_prestige_badge_num` も白字指定に追加。合計22項目。威信badgeの金色枠と図像は維持する。

使用する `vanilla_hoi_18mbs` / `hoi_18mbs` は元の白字atlasとmetricsを再利用し、赤・緑・黄などのinline paletteも元定義と一致させた。白字cloneへの切替後に未使用の黒字cloneを除き、現在の総数は57。上部バーでは画像素材と配置・サイズ・callbackを変更していない。

局所照合で、生成物の差分は `replace/topbar.gui`、`BSM_topbar.gui`、font GFX、manifestの4ファイルのみ。2GUIのfont参照22箇所以外のtoken、他172GUI、全240textureは適用直前と一致。元font定義とのglyph metrics/atlas/日本語override/意味色palette一致と、変更GUI/GFXの既存syntax検査もPASS。

証跡は `verification/hoi4-1194-2026-10-29/topbar-white-2026-10-30/`。`static-verification.json`は生産・政治整理前の局所検査の記録。標準上部数値の白字化は実表示を確認し、独自5項目は次回起動からの反映待ちとして `runtime-note.md` へ区別した。

追加5項目の編集時、隔離ゲームをユーザーが操作している可能性があり、キー・クリック・終了・再起動は行っていない。この5項目は次回起動で反映する静的確認済みの変更であり、起動中の旧表示を反映済みの実証とは扱わない。

## 生産・政治の追加整理

ユーザー提示の日本語画面をもとに、装備名と生産速度・工場数、政治の政党一覧・陣営・管理/経済同盟/政策欄を分離した。生産の専用背景を明色化し、造船所の5/10/15枠、MIO状態、既存の図像と進捗を保全。選択画像は淡青の見出しと透明な本体へ変え、旧暗色背景による上書きを避けた。現在の総数は174GUI/249textures/57font。構文・配置・alpha・frameと参照の静的検査はPASS。操作中のゲームを維持しているため、この追加整理の実表示は未確認。詳細は [追加整理の記録](WIN95_PANEL_LAYOUT_2026-10-30.md)。

## 後続の起動確認と顧問・艦隊の追加修正

別作業で切り替わった `feature/nts_scenario_content` 上のUI修正を含む作業ツリーを、実環境1.19.4.1で隔離起動。64.2秒で完走し、NTS新規ゲームの実画面を確認した。GUI読み込みエラーはなく、NTSのcompare構文6行と既知LVE2行、loc通知は残る。顧問/企業の候補カードと艦隊の文字色・行間はこの起動後に追加修正したため、起動時点の実証と区別する。詳細は [顧問・艦隊の記録](WIN95_ADVISOR_NAVY_2026-10-30.md)。


## 素材の仕上げ修正

2026-10-30: 元の紙や金属枠の輪郭を灰色の面へ流用する方法を、27種類について用途別の描画設定に置き換えた。共通枠も四段階の明暗へ変更。素材結合プレビュー・428項目の検証結果・実機未確認の範囲は [WIN95_MATERIAL_FINISH_2026-10-30.md](WIN95_MATERIAL_FINISH_2026-10-30.md) を参照。


## Decision画面の仕上げ追加

2026-10-31: イベント見出し・通知設定・カテゴリ・一覧の4素材を用途別に調整。項目名／コスト／残り時間と進捗領域を分離し、通常・緑・赤の3状態を維持した。88項目の検証、結合プレビュー、実機未確認の範囲は [WIN95_DECISION_FINISH_2026-10-31.md](WIN95_DECISION_FINISH_2026-10-31.md) を参照。


## ポップアップ／師団テンプレート／国家方針完了BGの仕上げ

2026-10-31: 共通見出し・下端・本文面と通常／旧式師団の8素材を用途別に調整。国家方針完了の金属・月桂冠BGは依頼により白い本文枠へ変更し、中央の方針アイコンを維持。441項目の検証、15見出しの確認、結合プレビューは [WIN95_POPUP_DEPLOYMENT_FINISH_2026-10-31.md](WIN95_POPUP_DEPLOYMENT_FINISH_2026-10-31.md) を参照。
