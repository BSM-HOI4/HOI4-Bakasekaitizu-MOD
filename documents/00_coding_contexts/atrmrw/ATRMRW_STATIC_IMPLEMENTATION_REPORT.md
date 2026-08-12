# ATRMRW 日本5艦級 静的実装報告

- 実施日: 2026-08-02
- 対象: HOI4 1.19.2静的契約
- 状態: 静的実装完了、HOI4実機起動はユーザー指示により未実施

## 実装結果

- SSW互換role ID `ship_type_slot`をcustom 0へ配置した。
- 最大36枠をcustom 18／fixed 18とし、全profileを9／12／15／18／24／30／36枠へnested配置した。
- `hidden_slot_count = 0`、船体構造だけを`fixed_visible`、他の物理枠を編集可能または可視lockとした。
- HOI4 1.19.2の`equipmentdesignerview.gui`と艦種別5 GUIをSHA-256固定の原本から生成した。
- 大和、高雄、吹雪、赤城、伊十五の5船体、59論理module、5variantを生成した。
- JPN 1936 OOBは赤城1隻、高雄4隻、吹雪23隻の計28隻を新船体IDへ移行した。旧variant定義は削除していない。
- 日本語／英語localisationはUTF-8 BOM付きで生成した。

## 数値契約

- exact 10 moduleはSSW固定コミットのeffective statsをID単位で転用した。
- aggregate 21 moduleは史実基数の0.8乗で非線形batch化し、航空容量は32+28=60機を加算合成した。
- historical_new 28 moduleは出典がある数値だけを導出し、出典なしの構造・機関方式等はidentity moduleとしてstatを付けていない。
- HP、ORG、速力、航続距離は5史実variantの目標から`final=(base+A)*(1+M)`でbaseを一度だけ逆算し、module構成digestと共に固定した。
- 加算・乗算順序のHOI4実機校正は未実施であり、台帳の`runtime_calibration_status`はpendingのままとする。

## 検証結果

```text
python3 -m unittest discover -s tools/atrmrw -p 'test_*.py'
Ran 60 tests
OK

PYTHONPATH=. python3 tools/atrmrw/validate_japan_game_integration.py
ATRMRW Japan game integration PASSED: 5 hulls, 59 modules, 5 variants, OOB=28

python3 tools/validate_mod.py
Validation PASSED: 0 errors, 139 warning(s)
```

139 warningは今回のATRMRW追加以前から存在する既存警告であり、本作業のスコープでは変更していない。

OOB一括移行後に次を確認した。

- 対象ファイルの行数: 747行で不変
- brace balance: 736 `{` / 736 `}`
- 旧対象参照: 0
- 新対象参照: 赤城1、高雄4、吹雪23
- JPN country historyのBOM: 1個を維持

## 未検証範囲

ユーザーの「HOI4起動禁止」指示に従い、次は確認していない。

- Designerの目視・クリック領域・tooltip
- role／module交換、設計保存、建造、改装
- OOBのゲーム内ロード
- 海戦性能、燃料消費、AI設計
- ATRMRW由来のruntime `error.log`

したがって本報告の「完了」は静的プロトタイプを意味し、ゲーム内動作確認済みを意味しない。
