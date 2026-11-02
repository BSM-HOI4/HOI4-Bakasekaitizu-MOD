# 上部バー白字の実表示確認

- 起動PID98370、隔離userdir `/var/folders/cm/bpt58vms6gl1m8j0hb9k5mfr0000gn/T/bsm-hoi4-topbar-white-ej9qk5z0`。enabled_modsはbsm_localのみ、descriptor正本bakasekai。system.log ActiveModCount1/バカ世界地図テスト版。通常settings/SSW/save未変更。
- 最初のCUA読み取り時点で大日本帝国1936/1/1 12:00 pauseのゲーム画面だった。検証者は起動後キー/クリックを一切送っておらず、ユーザーが操作中の可能性を親へ報告しread-only限定。BAT開始経路は今回未実施。
- 会話内の実スクショで標準上部値100%/77%/5.54M/88/100%/365、日時は白字化を視認 PASS。緑の燃料『満杯』や意味色は保持。赤の数値はこの静止状態では出現しておらず実機未検証（palette静的確認はroot担当）。
- BSM独自COUNTRY_PO/COUNTRY_CD/COUNTRY_ecに対応する10/5%/3677は黒の旧版表示。独自5項目の追加white修正はこの起動後のため実反映未確認。標準17の結果と分離する。
- 証拠PNG保存用getAXStateAndScreenshotは30秒timeout/kernel reset、getApp再取得も30秒timeout。PNG保存未確証、初回画像は会話内ツール結果のみ。以後UI試行停止、キー/クリック/終了ゼロを維持。
