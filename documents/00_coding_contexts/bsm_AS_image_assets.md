# アノマリーシステム 追加すべき画像アセット一覧

このドキュメントは、アノマリー（ステラリス要素）GUI 実装が参照しているが、
**実アートとしては未作成（プレースホルダ）** の画像をまとめたもの。
アート担当は、下記パスのファイルを正式な画像で**上書き**すれば差し替え完了（.gfx の編集不要）。

## 方針
- 発見画像は **アノマリー固有ではなくカテゴリー別**（7 種）。
- 現状の中身は `gfx/event_pictures/battlecivilwar.png` のコピー（全カテゴリ同一の仮画像）。
- カテゴリ ID は DB（`_bsm_anomaly_system.txt` の category）に対応:
  `1=政治 / 2=陸軍 / 3=海軍 / 4=空軍 / 5=信仰 / 6=文明 / 7=経済`

## カテゴリー別 4:3 発見画像（最優先）

| カテゴリ | GFX 名 | 差し替えパス | 推奨サイズ | 用途 |
|---|---|---|---|---|
| 政治 | `GFX_bsm_AS_cat_politics` | `bakasekai/gfx/interface/GUI/anomaly/cat_politics.png` | 4:3（例 200×150〜400×300） | 発見ポップアップ左の画像 |
| 陸軍 | `GFX_bsm_AS_cat_army` | `bakasekai/gfx/interface/GUI/anomaly/cat_army.png` | 同上 | 同上 |
| 海軍 | `GFX_bsm_AS_cat_navy` | `bakasekai/gfx/interface/GUI/anomaly/cat_navy.png` | 同上 | 同上 |
| 空軍 | `GFX_bsm_AS_cat_air` | `bakasekai/gfx/interface/GUI/anomaly/cat_air.png` | 同上 | 同上 |
| 信仰 | `GFX_bsm_AS_cat_faith` | `bakasekai/gfx/interface/GUI/anomaly/cat_faith.png` | 同上 | 同上 |
| 文明 | `GFX_bsm_AS_cat_civ` | `bakasekai/gfx/interface/GUI/anomaly/cat_civ.png` | 同上 | 同上 |
| 経済 | `GFX_bsm_AS_cat_economy` | `bakasekai/gfx/interface/GUI/anomaly/cat_economy.png` | 同上 | 同上 |

定義ファイル: `bakasekai/interface/bsm_AS.gfx`

## 任意（将来追加候補・現状は既存スプライト流用で未作成）

| 用途 | 想定 GFX 名 | 備考 |
|---|---|---|
| 探検隊 規模アイコン（小/中/大） | `GFX_bsm_AS_size_s/m/l` | 現状は文字ラベル（小規模/中規模/大規模）で表示。アイコン化する場合に作成 |
| 研究者 顔（顔枠） | `GFX_bsm_AS_researcher_face` | drawio の「顔」枠。現状は未使用。キャラ顔を出す場合に作成 |
| カテゴリ バッジ背景 | `GFX_bsm_AS_badge_bg` | 一覧/ポップアップのバッジ装飾。現状は標準テキスト表示 |

## 注意
- `.png` / `.dds` どちらも可（本 mod は GUI で png 実績あり: `gfx/interface/GUI/mine/`）。
- 4:3 を厳密にする必要はないが、ポップアップの `iconType` 表示枠に合わせると見栄えが良い。
- 差し替え後は `mcp__hoi4__hoi4_check_missing_gfx` で参照欠落が無いことを確認。
