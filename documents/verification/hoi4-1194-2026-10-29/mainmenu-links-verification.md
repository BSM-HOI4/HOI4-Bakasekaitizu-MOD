# メインメニューリンク列 実起動確認

- HOI4 1.19.4.0、隔離userdir、1280x720 / GUI 1.0。PID 83816、起動完走39.804秒。通常settings/playset/save変更なし。
- `mainmenu-links-final-1280x720.png` は今回起動の実画面。浮いた丸SNS9アイコン列が消え、HP/掲/DC/規/BS/X/f/IG/YTが灰色ボタン1列として右列下部に表示。全9文字が枠内、折返し・隣接ラベル重なりなし。
- toolbarとfooterの縦方向干渉なし。幅310へ修正した最終版でtoolbar右端まで青い元メニュー可視枠内に収まり、右に余白があることを実表示確認。Steam social領域はこの隔離起動では空白で、friendsボタン実描画は未確認。
- error.log は既存localisation key collision通知1行のみ。今回GUI/GFX/fontの新規エラーなし。
- 外部リンクは未クリック。9native button名・tooltip key・定義済みURL、friends callback名の保持をソースで確認。hover表示は入力API制約のため未確認。
- 1024x768 / GUI .8は実再起動せず静的確認。toolbar local x325..635 / y494..526 は665x600メニュー内、subscription下端488から6px、footer開始529から3pxの間。9ボタン右端はcontainer内245、friends領域右端306で幅310内。
- 隔離プロセスPID83816はメインメニューで継続中。
