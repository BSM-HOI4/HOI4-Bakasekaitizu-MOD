# Bootstrapロード 実起動確認

- canonical load_screen GUI/GFX/font移動後、1280x720 / GUI1.0、日本語、MODのみ有効の隔離userdirで検証。通常本体・settings/playset/saveは変更なし。
- 最初に撮影可能だった LOADING_GUI「世界を動かす窓を並べています……」（実進捗約7〜10%）から青背景・白見出し・Welcome/teal帯・小話・Win95実進捗が表示。後半「予想外の出来事を仕込んでいます……」でも同じ構図。観測フレームに金属UIなし。
- bootstrap-setup-early-1280x720.png はLOADING_GUIの初期寄りフレーム、bootstrap-setup-late-1280x720.png は後半イベントphase。**LOADING_DATABASES/LOADING_HISTORYはCUAのwindow取得より先に通過し、実画像未確認**。初回描画から全フレームの保証はしていない。
- 最新単一起動PID88270、userdir `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-boot-final-q_u0rond`。47.921秒でメニュー到達、実画面確認済み。error.logは既存loc key collision通知1行のみ。新GUI/GFX/fontエラーなし。
- 再試行中SIGTERMで終了しなかったこのchatの隔離PID87629/87770だけを強制終了し、最新は単一プロセス。診断連続frameは誤認防止のため一時ディレクトリへ退避。追加ゲーム内操作・OOB検証なし。最新PIDはメニューで継続中。
