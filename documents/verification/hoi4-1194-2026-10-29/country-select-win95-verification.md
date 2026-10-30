# 国家選択Win95 実起動確認

- HOI4 1.19.4.0、1280x720 / GUI1.0を起動前後settingsで確認。隔離PID5140、userdir `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-country-shz42n26`。通常settings/playset/save・本体変更なし。
- 38.475秒でmain到達、S→SP→Nで新国家選択へ遷移。明灰枠/白本文/紺見出し、6card、小旗、portrait、青選択枠を実確認。初期バトル三国の政府は『民主国家』でrawgroupkey消失、文字は枠内。
- Raise/freshAX後の座標clickで謎カードへ変更、選択青枠と国名/portrait/idea/history/政府更新を実確認。さらにJapan小旗から日本へ変更、岡田啓介・国旗・国別idea・履歴の更新を確認。
- 日本政府に `constitutional_monarchy_...` rawkey表示が残りrootへ修正依頼。今回GUI枠そのものの重なり・はみ出しは見られない。
- 保存済みcountry-select-win95-final-1280x720.pngは初期国家、country-select-win95-mystery-1280x720.pngは切替後。Japanは画面をtooltipが覆ったため最終証拠には採用していない。
- CUAのnoWindowsAvailableが断続、履歴領域・下部戻る/国家を選択はRetina raw座標がwindow論理boundsを超え直接操作不可。Escも遷移完了を確認できず、戻る/選択action/履歴scroll実操作は未検証。国家選択そのもののcallbackのみ実証。ゲーム開始は実行していない。
- error.logは既存loc collision通知1行のみ、新GUI/GFX/fontエラーなし。1024/.8はこの段階で実起動未実施。

## 最終1024x768確認

- 政府loc22groups補完後に一度だけ隔離再起動。PID8231、userdir `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-country-final-d87x19y9`。起動前後settingsは1024x768/gui_scale=.8で一致。40.115秒でmain到達。S→SP画面確認→Nで国家選択へ。
- 1200x690modalの全外形、6カード、portrait/旗、情報/履歴panel、戻る/国家を選択buttonが画面内に収まる。明灰/白/黒字と紺見出しの分離、文字折返し/溢れ問題なし。最終実画像 country-select-win95-final-1024x768.png 保存。
- Japan小旗のclickはRaise/新handle後もnoWindowsAvailableで実行できず、追加反復せず停止。日本政府の最終rawkey消失は実画面未確認。sourceにconstitutional_monarchy_desc: "$constitutional_monarchy$"を確認し、rootが既存和名へのalias補完済み（静的確認）として区別。
- Escはworker再調査でvanilla chooser BACK契約を保持していると報告済み。mainへ戻る契約とは異なるため、上記のEsc観測をバグ認定していない。history標準text_sliderも定義保持・実scroll未確認。
- 最終error.logは既存loc collision通知1行のみ、新規GUI/GFX/fontエラーなし。外部リンク/購入/本ゲーム開始は未実行。PID8231は国家選択で継続、追加操作終了。
