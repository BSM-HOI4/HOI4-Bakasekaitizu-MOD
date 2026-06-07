# 伝統・アセンション / アノマリー・探検隊 GUI 画像素材リスト

GUI 2画面分離リニューアル（2026-06-07）に伴い、推奨／要差し替えの画像素材を整理する。
現状は多くがバニラ流用（`GFX_decision_generic_decision` 等）で動作はするが、Stellaris風の見やすさを目指すには専用素材が望ましい。

- 形式: `.dds`（DXT5 / 32bit, mipmap有）推奨。アイコンは `.tga` でも可。
- 配置: `bakasekai/gfx/interface/...`、`.gfx` 定義は `bakasekai/interface/*.gfx`。
- 既存の本格アセット一覧は `bsm_AS_image_assets.md` も参照（アノマリーカテゴリ画像等）。

---

## 1. Topbar カスタムボタン（最優先）

`interface/replace/topbar.gfx` で定義。現状 `GFX_topbar_stellaris` は `topbar_anomaries.dds` を流用しており、2ボタンが同一絵で見分けがつかない。

| スプライト名 | 用途 | 現状 | 推奨サイズ | 備考 |
|---|---|---|---|---|
| `GFX_topbar_stellaris` | ボタン1: 伝統・アセンション | anomaries 流用 | 60×60（3フレームstrip 180×60 推奨） | 月桂冠／星／伝統ツリーを想起させる絵。normal/hover/pressed |
| `GFX_topbar_anomaries` | ボタン2: アノマリー・探検隊 | 専用 `topbar_anomaries.dds` | 60×60 | 既存流用可。望ましくは虫眼鏡＋未知マーク |

> 旧 `GFX_topbar_naisei` は不使用化（topbarから削除済み）。素材ファイルは残置で問題なし。

---

## 2. 伝統ツリー アイコン（7種）

`bsm_stellaris.gui` 左カラム。現状すべて `GFX_decision_generic_decision`。

| 推奨スプライト名 | 伝統 | モチーフ案 |
|---|---|---|
| `GFX_bsm_trad_exploration` | 探索 | 羅針盤・帆船 |
| `GFX_bsm_trad_expansion`   | 拡張 | 旗・開拓地 |
| `GFX_bsm_trad_prosperity`  | 繁栄 | 金貨・麦 |
| `GFX_bsm_trad_armaments`   | 軍備 | 剣・盾 |
| `GFX_bsm_trad_diplomacy`   | 外交 | 握手・条約 |
| `GFX_bsm_trad_governance`  | 統治 | 天秤・庁舎 |
| `GFX_bsm_trad_harmony`     | 調和 | 蓮・円環 |

- 推奨サイズ: 32×32 または 40×40（ボタン兼アイコン）。
- 進捗段階（0〜7）を色で表すなら 8フレームstripも可。

---

## 3. アセンションパーク アイコン（8種）

`bsm_stellaris.gui` 右上。現状 `GFX_decision_generic_decision`。

| 推奨スプライト名 | パーク | モチーフ案 |
|---|---|---|
| `GFX_bsm_asc_1` | 技術的卓越 | 歯車＋電球 |
| `GFX_bsm_asc_2` | 世界規模行政 | 地球＋庁舎 |
| `GFX_bsm_asc_3` | 危機対処機構 | 盾＋警告 |
| `GFX_bsm_asc_4` | 破局への道 | 黒い炎（3と排他） |
| `GFX_bsm_asc_5` | 国土改造 | 山＋造成 |
| `GFX_bsm_asc_6` | 国際交易網 | 航路＋コンテナ |
| `GFX_bsm_asc_7` | 人工進化計画 | DNA |
| `GFX_bsm_asc_8` | 精神的覚醒 | 光輪 |

- 推奨サイズ: 48×48。取得済/未取得/選択不可を表す 3フレームstrip 推奨。

---

## 4. 特性 アイコン（7種・任意）

`bsm_stellaris.gui` 右下。装備/解除ボタンのみで動作するため優先度低。アイコンを付ける場合:

`好戦的 / 平和的 / 拡張主義 / 孤立主義 / 霊主義的 / 唯物主義的 / 技術的に進歩している`
→ `GFX_bsm_trait_*` 32×32。

---

## 5. ウィンドウ装飾（任意）

- ヘッダー帯: 現状 `GFX_header_bg` 流用。専用 `GFX_bsm_stellaris_header`（920×40）／`GFX_bsm_AS_header`（840×40）を作ると統一感が出る。
- 背景: 両ウィンドウとも `GFX_tiled_window_1b_border`（EAと同じ）流用中。差し替え不要。

---

## 実装メモ

- 専用スプライトを追加する場合は新規 `.gfx`（例 `interface/bsm_stellaris.gfx`）を作り、`bsm_stellaris.gui` / `bsm_AS.gui` の `quadTextureSprite` / `spriteType` を差し替える。
- 素材未準備のうちはバニラ流用のままで動作する（プレースホルダ運用）。
