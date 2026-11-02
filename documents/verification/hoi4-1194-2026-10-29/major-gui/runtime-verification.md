# Major GUI runtime verification

2026-10-30 初回確認

- HOI4 1.19.4.0、今回MODのみを有効化した新しい隔離userdir: `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-major-uopf_9f2`。PID60407。通常settings/playset/save・ゲーム本体は変更していない。
- 起動前settings.before-launch.txtと起動後settings.txtは1280x720/min_gui1280x720/gui_scale1.000000一致。setup.log Startup time 47342msで完走。
- 起動error.logは既存localisation collision通知1行のみ。今回追加のGUI/GFX/font構文・素材・font読込エラーは出ていない。
- CUA getApp('hoi4')はMac locked / automatic unlock could not unlock itと報告。画面取得・S/N/Enter操作は実行できず、新規ゲーム開始と各sidebar実表示は未検証。手動unlock待ち。
- state1112 spawn / NSI artillery / GBR cruiser variantの新規ゲーム時再確認も未実施。初期起動でエラーが無いことを新規ゲーム整合性の保証とは扱わない。

## ロック解除後のinstance照合

- 再開時、旧隔離PID60407は終了済み。生存は引数なし通常起動PID66937のみで、CUA getApp(hoi4)画像も全画面の宇宙艦/金属ロードとなり今回隔離GUIと一致しなかった。画像取得のみで、キー/クリック/終了/新規起動は実行せず停止。
- 旧隔離dlc_load.jsonはmod/bsm_local.modのみ、descriptor絶対pathは本作業ツリーbakasekai、system.log Active Mod Count1 / バカ世界地図テスト版で正しい。過去startup PASSを現在の通常instance実証へ流用しない。
- Macの公開CUA APIはapp name/path/bundleID指定でPID指定なし。windowID指定/listWindowsはLinux/Windows用と文書化され、getStateもhoi4 windowID/PIDを返さなかった。複数起動時に通常instanceを誤操作しないため、rootのユーザー状況照合を待つ。

## ロック解除後の起動識別（2026-10-30）

- 解除後、旧検証PID60407は終了済みだった。同名appを再取得した画像は通常起動のSSWであり、バカ世界地図の表示確認として採用しない。
- 通常userdirのsystem.logは00:27:06にActive Mod: The Sun Shining on the Worldを記録。dlc_load.jsonはmod/ssw.mod、pathは/Users/eightman/dev/hoi4/SSW_mod_tech_rework。通常起動へのキー・クリック・終了操作は行っていない。
- 一方、旧検証userdirのsystem.logはActive Mod Count:1 / バカ世界地図テスト版、descriptor pathは/Users/eightman/dev/hoi4/HOI4-Bakasekaitizu-MOD/bakasekaiであり、47.342秒の起動結果自体は正しい対象だった。
- Mac版CUAの公開APIはアプリ名/path/bundle IDを選べるがPID指定が確認できない。以後は新しい隔離起動のlog/descriptorと、入力前のBaka固有画面を照合し、一致しない画面へは入力しない。

## 正しいBaka instanceでのv1巡回（2026-10-30）

- 新隔離PID68791、userdir `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-major-confirmed-qiunsmrl`。ActiveModCount1/バカ世界地図テスト版、descriptor絶対pathが本作業ツリーbakasekaiであること、CUA画像identified-baka-main.pngがBaka固有compactmenuであることを親も目視照合してから入力再開。SSW通常processへ入力/終了していない。
- S→SP、N→Baka国家選択、Return→BAT開始設定、Return→ゲーム開始を各画面観察して実施。1936/1/1 12:00pauseのまま日付進行なし。

| 画面 | v1結果 | 証拠/問題 |
|---|---|---|
| main/SP/国家選択 | PASS | 固有青menu/白国選択/portrait旗青選択保持 |
| 開始前設定 | FAIL contrast | setup-contrast-issue.png、明灰右情報/難易度等に白字残り |
| BAT新規開始 | PASS | bat-welcome.png、固有地図とwelcome、pause維持 |
| 政治Q | FAIL contrast | politics-v1.png、暗専用上半に黒字 |
| 決定ShiftQ | PASS visible | decisions-v1.png、紺header白字/緑semanticrow白字保持 |
| 研究W | FAIL contrast | research-v1.png、紺titleに黒/灰字、研究slot本文は読める |
| 国際市場E | FAIL contrast | international-market-v1.png、上帯暗黒字/参入銀白字。Eはこのinstanceで市場を開いたため外交と呼ばない |
| 貿易R | FAIL contrast | trade-v1.png、暗上帯/左説明黒字、銀上白0値 |
| 建設T | FAIL contrast + runtime contract | construction-v1.png、暗上帯黒字。start_construction_entryのrepair_order_number_window/repair_order_number不足23組 |
| 生産Y | PASS visible | production-v1.png、絵/元暗semanticpanel白字保持 |
| 配備U | FAIL contrast | deployment-v1.png、師団名暗row黒字/師団編制紺上黒字 |
| 兵站I | FAIL contrast | logistics-v1.png、暗上帯/燃料header黒字 |
| 将校団ShiftE | FAIL contrast | officers-v1.png、陸海軍司令部紺黒字、勲章指揮官button黒字 |
| 諜報ShiftW | partial contrast | intelligence-v1.png、暗創設panelcost黒字、他紙tab/本文は読める |
| 国家方針AltQ | partial contrast | focus-v1.png、icon/connectors保持、検索黒field黒字 |
| 陣営CtrlQ | 未表示 | BATは陣営なし、mapのまま。faction-attempt-v1.pngは陣営proofではない |
| pause menu | PASS visible | pause-menu-v1.png、銀button黒字 |
| 設定 | partial contrast | settings-v1.png、ビデオtab、元暗gradientfield上黒字だが可読。設定値操作/適用なし |
| 読込dialog | FAIL contrast | load-dialog-v1.png、暗local/cloudtab黒字、空list/下button保持。読込実行なし |
| 保存/MIO/SP/師団装備設計/ドクトリン/外交詳細 | 未実施 | v2修正前巡回拡大を止めた |

- 新規開始直後errorは既存loc通知+既知LVE small_plane_airframe_0 variant/OOB2件のみ。state1112 spawn/NSI artillery/GBR cruiser variantの旧エラーは今回出ていない（全国家ゲーム進行保証ではない）。建設表示後上記child不足46行が追加し49行。
- 視認性issueは逐次親へ具体画像で報告済み。v2freeze通知までUI操作/reload/再起動を停止。主要PNGはv1suffixで比較証拠として保持。

## v2実巡回（2026-10-30）

- 隔離PID80366/userdir `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-major-v2-kp81_f3f`。ActiveModCount1/Baka descriptor絶対pathと固有青main画像identified-baka-main-v2.pngを照合後に入力。1280x720/GUI1、BAT 1936/1/1 12:00 pause維持。通常SSW/settings/save未操作。

| 画面 | v2結果 | 原画像/所見 |
|---|---|---|
| 開始前 | contrast PASS / 最終配置未再撮影 | setup-v2.png 黒字/銀button/紺選択。1000ms animation途中のclipの可能性を区別 |
| 政治 | 改善 / caption残件 | politics-v2.png 上半暗潰れ解消、国民精神caption白on灰のみ弱い |
| 貿易 | 改善 / neutral残件 | trade-v2.png 民需/説明黒、正負/金濃色保持。neutral白0が銀上で弱い |
| 建設 | PASS visible/runtime | construction-v2.png 専用帯可読、repair_order child不足再発なし |
| 配備 | PASS visible | deployment-v2.png 師団row黒/白、見出し白/紺 |
| 兵站 | PASS visible | logistics-v2.png header/資源帯可読、燃料意味bar保持 |
| 研究 | PASS visible | research-v2.png 白title/紺、slot本文可読 |
| 将校団 | 改善 / 捕虜数残件 | officers-v2.png 陸海見出し白/紺。捕虜0暗金が暗緑上で弱い |
| 諜報 | PASS visible | intelligence-v2.png 費用5白/30日黄、紙tab/図像保持 |
| 国家方針 | PASS visible | focus-v2.png 検索白/黒、node/icon/connectors保持 |
| 実外交 | FAIL contrast | diplomacy-v2.png 外国rightclickでオージー外交表示。中段暗NoDLC政体/選挙/国民精神が黒で潰れる。他国名/旗/portrait/pie/関係値保持。外交行動未実行 |
| 設定 | PASS visible | settings-v2.png 銀tabs黒/白帯黒、1280x720/1x実表示。値変更なし |
| 読込 | PASS visible | load-dialog-v2.png 暗local/cloud白字/白空一覧/銀黒button。実ロードなし |

- v1で確認済み決定/生産はv2反復せず。保存/陣営/MIO/SP/師団装備設計/ドクトリン等の深い変種は未実施。全DLC/戦闘進行保証はしない。
- v2巡回後errorは既存loc通知+既知LVE小型機variant/OOB2行のみ。state1112 spawn/NSI artillery/GBR cruiser variant/repair_order missing再発なし。
- 親へ具体画像を報告し、最終小修正通知待ち。

## 最終v3対象絞り込み確認（2026-10-30）

- 所有PID80366のcommand/userdir照合後のみ終了し、新PID82233/userdir `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-major-v3-wrg2eern` で隔離起動。ActiveModCount1/Bakaと正本descriptor path、identified-baka-main-v3.png固有mainを照合してから入力。通常SSW/settings/save未操作。起動前後1280x720/min_gui1280x720/GUI1。BAT1936/1/1 12:00 pause維持。
- setup-final-v3.png: animation完了後、portrait/史実AI/footer収まりと黒字銀button PASS。v2途中clipは最終状態では再現せず。
- politics-final-v3.png: 国民精神caption黒on銀 PASS。
- trade-final-v3.png: neutral0等黒、赤negative/緑positive保持、budget0黒/金26保持 PASS。
- officers-final-v3.png: 捕虜0が明黄on暗緑へ改善 PASS。
- diplomacy-final-v3.png: portrait/旗/pie/関係値/意味art保持、3明灰panelと国民精神黒/茶focus白によるcontrast PASS。ただしportrait右政体3行（立憲君主体制2行/選挙なし）が縦に詰まり重なる。raw座標x514..710,y575..660。親へ画像報告、外交行動なし。
- construction-final-v3.png: 建設を一度開いた後もerrorは既存loc通知+既知LVE small_plane_airframe_0/OOB2行のみ。state1112/NSI/GBR/repair_order child不足は再発なし。
- v2でPASS済み他sidebarは再反復しない。深いDLC/戦闘変種は未検証を保持。外交政体の行間残件のみ通知し検証操作停止。

- 外交行間ソース修正後の開閉では自動反映せず。隔離BSM Promptをgraveで表示確認しreload interface入力を試したが、typeTextは日本語IMEによりUnknowncommand、ASCIIpaste→Return一度も反映を確認できなかった。有効reload成功とは扱わない。consoleを閉じ外交再表示、pause維持。diplomacy-final-v3.pngはcontrast最終/spacing旧版であり、diplomacy-spacing-final.pngは未作成。行間修正の実機再確認は未完了として親へ報告。

## 外交行間の最終v4実証（2026-10-30）

- Baka所有PID82233のcommand/userdir照合後のみ終了、新隔離PID83264/userdir `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-major-v4-han5v076`。ActiveModCount1/バカ世界地図テスト版と固有compact青main、descriptor正本bakasekaiを照合後S/N/Returnを各段階観察しBAT新規開始。通常SSW/settings/saveは無操作。起動前後1280x720/min_gui1280x720/GUI1。
- 外国rightclickだけでオージー外交を開き、animation完了後の `diplomacy-spacing-final.png` にて政体2行/選挙なしの3行が分離し重なり解消 PASS。明灰上黒字、茶focus白字、国民精神黒字、portrait/旗/pie/関係値/外交行動一覧は保持。外交行動未実行、1936/1/1 12:00 pause維持。
- 新規game後error.logは既存loc通知+既知LVE small_plane_airframe_0/OOB2行のみ、新規GUIerror無し。
- v3のhotreload成功は未確証であり、spacing修正の実証は今回v4画像のみ。diplomacy-final-v3.pngはcontrast最終/旧spacing比較証拠として保持。その他主要画面はv2/v3実証を参照、未検証DLC/戦闘変種へ拡大せず検証操作完了。
