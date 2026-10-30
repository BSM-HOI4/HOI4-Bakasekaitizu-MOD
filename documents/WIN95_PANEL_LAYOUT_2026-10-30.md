# 生産・政治画面と上部バーの追加整理（2026-10-30）

対象は `HOI4-Bakasekaitizu-MOD/bakasekai`、branch `feature/_system_race_removal`。ユーザーの日本語スクリーンショットで確認した重なりを修正した。commit/pushは行っていない。

## 変更

- 上部バーの標準17数値/日時に加え、MOD独自の世論・文化度・統一通貨・国家通貨切替・威信順位を白字へ変更。元fontの字形・大きさと赤/緑等の意味色を維持する。
- 生産の装備名と速度欄に7pxの間隔を設け、見出し・名称を16/24pxの枠へ整理。4種の展開行へ速度用の紺背景を追加し、既存の緑進捗バーと白い速度表示を組み合わせる。
- 軍需工場・造船所・稼働数・修理数の表示を分離。29px幅の修理アイコンと数値欄の間に4pxの余白を確保した。12個のフィルター数値欄も24px幅へ整列した。
- 生産の暗い専用面を灰色/白へ変更。上部に焼き込まれた6個の工場glyphは元の画素を保ち、数値と重ならない位置へ8px移動した。
- 造船所の背景はframeごとの5/10/15枠（5列×1/2/3行）を描き分ける。MIO付きの見出しは銀/金枠で通常の白い行と区別。選択は淡青の見出しと紺枠、透明な本体へ変え、元の不透明な暗い選択画像が白い行や工場枠へ重ならないようにした。旧式警告・装備絵・進捗・操作アイコンを保全した。
- 政党一覧を15pxから22px間隔へ広げ、4行が94px枠内に収まるよう調整。既存のスクロールを保持した。
- 陣営作成/表示ボタンを57pxから29px高へ整理。国民精神と政党一覧の間に収めた。管理ボタン、経済同盟、政策欄は各6px以上の間隔で別の段へ配置した。
- 茶色の国家方針画像上は白字、灰色の国民精神見出しと経済同盟ボタンは黒字へ限定。旧版政治rootとの重複定義でも共有レイアウトを揃えた。

## 検証

- 変更した4GUIと生成GFX/fontの既存構文検査: PASS。
- 既存named widgetの階層・callback・frame・text保持、追加背景4個の配置: PASS。
- 装備名/速度/工場割当の間隔、政党4行、管理/経済同盟/政策の離隔: PASS。
- 10個のGFXの元寸法/frame/effect/border、8 alpha mask、6工場glyphの画素保持: PASS。2つの選択画像は本体を意図して透明化し、元にない不透明部分を増やしていないことを別途確認。
- 造船所frameの1/2/3行の違い、選択見出しの明色と工場枠上の本体透過: PASS。
- major generatorの生成総数: 174GUI / 249textures / 57font clones。
- 最終 `generate_win95_major_gui.py --check` と `git diff --check`: PASS。

上部の標準値・日時の白字化は1.19.4のBaka専用起動で視認した。独自5項目と生産・政治の追加整理は起動後の編集であり、実表示は未確認。ユーザーが操作しているゲームへ入力・終了・再起動を行っていないため、次回起動から反映される。CUAの追加撮影はtimeoutし、実画面のPNGを保存できなかった。素材previewを実ゲーム画像として扱わない。

証跡: `verification/hoi4-1194-2026-10-29/panel-layout-2026-10-30/` の `production-layout-changes.json`、`production-filter-changes.json`、`politics-layout-changes.json`、`chrome-static-verification.json`、`layout-static-verification.json`。`production-chrome-preview.png` は素材だけの比較用画像。
