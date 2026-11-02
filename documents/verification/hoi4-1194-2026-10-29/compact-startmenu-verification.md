# Compact start menu runtime verification

- 通常本体/settings/playset/saveを変更せず、MODのみ有効の隔離起動。外部リンク・購入項目は未クリック。
- 1024x768は起動前gui_scale=1.000000をfile再読込で確認・settings.before-launch.txt保存したが、エンジンが起動後0.800000へ自動補正。実証条件は1024x768 / GUI .8。白font修正後最終PID99553、48.913秒でメニュー到達。
- 1280x720は起動前後ともgui_scale=1.000000を確認。最終PID981、48.064秒でメニュー到達。
- 両条件でコンパクトメニューは左下に収まり、左7操作・右5短リンク・SNS9個の2段・終了が青い元枠の内側。日本語ラベルは折返し/隣接文字重なり/クリップなし。白見出しとversionを実確認。friends領域は隔離Steam social非表示のため空白。
- 1024/.8でSキーからシングルプレイヤーdialog表示、Escでmain復帰を実確認。外部callbackはnative名/URL保持の静的検証のみ。
- 最終画像 startmenu-compact-final-1024x768.png / startmenu-compact-final-1280x720.png は両方白font修正後の今回実画面。
- 両最終起動のerror.logは既存localisation collision通知1行のみ、新GUI/GFX/fontエラーなし。今回はメニュー到達を撮影、bootstrapの短い初期phaseを連続撮影していない。
- 1280最終userdir: `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-compact-1280-25f2wb9g`。PID981をmainで継続。旧隔離プロセスだけ終了した。追加データ/OOB/newgame検証なし。
