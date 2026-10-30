# Windows 95 Setup風ロード画面 実起動検証

検証日: 2026-10-29 (JST)
本体: HOI4 1.19.4.0、macOS、1280x720 / gui_scale=1.0、windowed。

## PASS

- 起動後半のMOD GUIへ切り替わった後、青い新背景と白い「バカ世界地図 セットアップ」見出しが描画された。
- 中央の白いWelcome、左teal帯、thumbnail/BSM95/既存原ロゴ、右の案内と特徴、小話が描画された。
- 本文の複数行が重ならず、行間が確保された。font atlasのmissing textureエラーは解消。
- 実ステータスが「ひと味違う国境線を引いています……」から「七つの海の道のりを測っています……」へ進み、実進捗バーの幅も増加した。
- 初期段階はvanilla窓、その後MODのSetup画面へ切り替わる。画像は後半の実画面であり模式図ではない。
- 起動完走しメニュー/DLC案内まで到達。最新error.logは以前からあるlocalisation collision通知1行のみ。今回のGUI parse/font missingエラーはない。
- 通常のsettings/playset/saveを変更せず、新規temp userdirのdlc_load/local descriptorで検証。

## 画像

- `loading-setup-actual-1280x720.png`: 新背景、本文、海の道のりステータス、後半の実進捗。
- `loading-setup-progress-1280x720.png`: その前の国境線ステータスと実進捗。後半画像との比較で進捗変化を確認できる。

## 1024x768の境界 (静的確認)

最新load_screen.guiの中央anchorと760x424/760x70素材から計算:

| 解像度 | Welcome矩形 | status矩形 | title最大矩形 |
|---|---|---|---|
| 1024x768 | (132,156)-(892,580) | (132,674)-(892,744) | (28,22)-(988,66) |
| 1280x720 | (260,132)-(1020,556) | (260,626)-(1020,696) | (28,22)-(988,66) |

いずれもviewport内。背景は1448x1086 spriteをcenter基準scale2で配置するため両サイズを全面カバーする。
1024x768の今回Setup画面そのものは実起動しておらず、上記は静的境界確認。今回ロード外の新規ゲーム/OOB検証は行っていない。

## 実行記録

Userdir: `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-setup-capture-uchpphc8`

[19:15:15][1936.01.01.12]: Startup time: 43628ms

error.log:
```text
[19:14:57][no_game_date]: The game has loc key collisions. Check logs/text.log for more details
```
