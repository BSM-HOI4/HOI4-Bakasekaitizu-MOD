# BSM 国家通貨システム (National Currency System)

最終更新: 2026-06-08

## 概要

各国・地域が独自のローカル通貨を持ち、統一通貨（UC）に対する為替レートが動的に変動するシステム。為替レートはUC獲得量に影響し、経済同盟の通貨同盟（Goal03）で統合可能。

## 通貨一覧（30通貨）

| ID | キー | 通貨名 | 記号 | 基軸国 | 初期レート(1UC=) |
|----|------|--------|------|--------|------------------|
| 0 | `nc_uc` | 統一通貨 | UC | — | 1.0 |
| 1 | `nc_usd` | 米ドル | $ | USA | 1.0 |
| 2 | `nc_eur` | ユーロ | € | EUR/FRA/DEU | 0.92 |
| 3 | `nc_gbp` | ポンド | £ | GBR | 0.79 |
| 4 | `nc_jpy` | 円 | ¥ | JPN | 149.0 |
| 5 | `nc_cny` | 人民元 | ¥ | CHI | 7.2 |
| 6 | `nc_rub` | ルーブル | ₽ | SOV | 92.0 |
| 7 | `nc_krw` | ウォン | ₩ | KOR | 1320.0 |
| 8 | `nc_inr` | ルピー | ₹ | IND | 83.0 |
| 9 | `nc_try` | リラ | ₺ | TUR | 27.0 |
| 10 | `nc_brl` | レアル | R$ | BRA | 5.0 |
| 11 | `nc_mxn` | メキシコペソ | Mex$ | MEX | 17.0 |
| 12 | `nc_ars` | アルゼンチンペソ | AR$ | ARG | 350.0 |
| 13 | `nc_sar` | サウジリアル | ﷼ | SAU | 3.75 |
| 14 | `nc_egp` | エジプスポンド | E£ | EGY | 31.0 |
| 15 | `nc_chf` | スイスフラン | Fr | SWI | 0.88 |
| 16 | `nc_sek` | クローナ | kr | SWE | 10.5 |
| 17 | `nc_aud` | 豪ドル | A$ | AST | 1.55 |
| 18 | `nc_idr` | ルピア | Rp | IDN | 15500.0 |
| 19 | `nc_thb` | バーツ | ฿ | SIA | 35.0 |
| 20 | `nc_ngn` | ナイラ | ₦ | NGA | 800.0 |
| 21 | `nc_zar` | ランド | R | ZAF | 19.0 |
| 22 | `nc_kes` | 東アフリカシリング | KSh | KEN | 150.0 |
| 23 | `nc_cop` | コロンビアペソ | Col$ | COL | 4000.0 |
| 24 | `nc_ils` | シェケル | ₪ | ISR | 3.7 |
| 25 | `nc_twd` | 台湾ドル | NT$ | TWN | 31.0 |
| 26 | `nc_php` | フィリピンペソ | ₱ | PHI | 56.0 |
| 27 | `nc_myr` | リンギット | RM | MAL | 4.7 |
| 28 | `nc_man` | 満州国円 | 滿 | MAN | 120.0 |
| 29 | `nc_generic` | 汎用通貨 | ¤ | — | 100.0 |

## 国変数

| 変数名 | 型 | 説明 |
|--------|-----|------|
| `bsm_nc_id` | int | 通貨ID（0-29） |
| `bsm_nc_rate` | float | 現在の為替レート（1UC = X NC） |
| `bsm_nc_base_rate` | float | 基準為替レート（初期値） |
| `bsm_nc_rate_prev` | float | 前月の為替レート |
| `bsm_nc_rate_delta` | float | 前月比変動量 |
| `bsm_nc_stability` | int | 通貨安定度（0-100） |
| `bsm_nc_inflation` | float | インフレ率（%） |
| `bsm_nc_original_id` | int | 初期通貨ID（Goal03解除時の復帰用） |
| `bsm_nc_filter_mode` | int | GUIフィルタ（0=同盟内, 1=世界） |

## 為替レート月次計算

```
new_rate = base_rate / factor

factor構成:
  基本ファクター: 1.0
  + 安定度寄与: (stability - 0.5) × 0.1
  × 戦争ペナルティ: ×0.95 (長期戦: 追加×0.92, ×0.95)
  × UC余剰ボーナス: ×1.02
  × UC債務ペナルティ: ×0.93
  × EA Goal03: ×1.05
  × 文明度高: ×1.01 (>0.5), ×1.01 (>0.8)
  × 従属国: ×0.96

クランプ: base_rate × 0.3 〜 base_rate × 3.0
```

## UC獲得への影響

既存のUC月次計算（`_bsm_Unified_Currency.txt`）の`temp_factor`に為替補正を加算:

```
t_nc_uc_mod = (base_rate / current_rate - 1.0) × 0.3
temp_factor += t_nc_uc_mod
temp_factor = clamp(temp_factor, min=0.05)
```

- 通貨が強い（rate < base）→ UC獲得ボーナス
- 通貨が弱い（rate > base）→ UC獲得ペナルティ

## 通貨強弱判定

| 段階 | 条件 | 表示 |
|------|------|------|
| 強い | rate < base × 0.9 | §G▲ 強い§! |
| 普通 | base×0.9 ≤ rate ≤ base×1.1 | §Y― 普通§! |
| 弱い | rate > base × 1.1 | §R▼ 弱い§! |

## EA Goal03（通貨同盟）統合

Goal03発動時:
- 全メンバーの`bsm_nc_id`を盟主の通貨に統一
- `bsm_nc_rate` / `bsm_nc_base_rate`も盟主に同期
- 月次計算で×1.05ボーナス
- `bsm_nc_union_convergence`（収斂度）と`bsm_nc_union_exit_pressure`（離脱圧力）を初期化

Goal03月次処理:
- 加盟国は盟主通貨ID/base_rateを継続的に同期
- 収斂度60以上で盟主通貨レートを直接流通
- 通貨安定度・低インフレ・UC黒字で収斂度が上昇
- 低安定度・高インフレ・UC赤字・戦争で収斂度が低下し、離脱圧力が上昇
- 収斂度80以上で`bsm_nc_union_converged_modifier`
- 離脱圧力50以上で`bsm_nc_union_strain_modifier`
- 離脱圧力80以上で`nc.5`（通貨同盟の離脱危機）を発火

Goal03解除時:
- `bsm_nc_original_id`から元の通貨に復帰
- `bsm_nc_assign_currency`でbase_rateを再設定
- 通貨同盟関連変数・動的補正をクリア

## 通貨危機イベント

| イベントID | トリガー | 効果 | クールダウン |
|------------|----------|------|-------------|
| `nc.1` | インフレ>20% | レート+50、安定度-30 | 180日 |
| `nc.2` | UC<0 | レート×1.5、安定度-40 | 360日 |
| `nc.3` | 安定度>90% | レート×0.95、安定度+10 | 365日 |
| `nc.4` | Goal03達成 | ニュースイベント | — |
| `nc.5` | Goal03中かつ離脱圧力>80 | 安定化/資本規制/通貨同盟離脱を選択 | 180日 |
| `nc.6` | `nc.5`で通貨同盟離脱 | ニュースイベント | — |

## Dynamic Modifier

- `bsm_nc_crisis_modifier`: 安定度<30%時
  - 安定度 -5%、戦争支持率 -3%、政治力 -10%
- `bsm_nc_union_converged_modifier`: Goal03中かつ収斂度80以上
  - UC獲得 +5%、貿易評価 +5%、政治力 +5%
- `bsm_nc_union_strain_modifier`: Goal03中かつ離脱圧力50以上
  - 安定度 -3%、戦争支持率 -2%、政治力 -5%

## ファイル構成

### 新規ファイル
| パス | 役割 |
|------|------|
| `common/scripted_effects/_bsm_national_currency.txt` | 初期化・月次計算・データ準備・イベント発火 |
| `common/scripted_triggers/_bsm_national_currency_triggers.txt` | 通貨判定トリガー |
| `common/scripted_localisation/_bsm_national_currency_sloc.txt` | 動的ローカライズ |
| `common/dynamic_modifiers/_bsm_national_currency_modifiers.txt` | 通貨危機modifier |
| `events/_bsm_national_currency_events.txt` | 通貨イベント |
| `interface/_bsm_national_currency.gfx` | スプライト定義（30通貨×3段階=90） |
| `localisation/japanese/_bsm_national_currency_l_japanese.yml` | ローカライズ |
| `gfx/currency/` | 通貨アイコン画像（75×40px PNG） |

### 既存ファイル追記
| パス | 変更内容 |
|------|----------|
| `common/on_actions/_bsm_system.txt` | startup: `bsm_nc_init_currency`, monthly: `bsm_nc_monthly_update` |
| `common/scripted_effects/_bsm_Unified_Currency.txt` | UC計算に為替補正統合 |
| `common/modifier_definitions/_bsm_core.txt` | `NC_exchange_factor` 追加 |
| `common/scripted_effects/bsm_ea_goals_effects.txt` | Goal03通貨統合・解除時復帰 |
| `interface/bsm_economic_alliance.gui` | 5タブ化 + Tab5通貨レートパネル |
| `common/scripted_guis/bsm_economic_alliance_sgui.txt` | Tab5可視性・フィルタ・動的リスト |
| `interface/BSM_topbar.gui` | 75×40通貨アイコン表示欄追加 |

## GUI: EA Tab5 通貨レート

EA画面に5番目のタブ「通貨レート」を追加。

### レイアウト
- タブボタン: `GFX_sort_button_140x29` ×5（全タブを140px幅に変更）
- リスト: `nc_rate_list`（`global.bsm_nc_rate_display_list`配列）
- エントリ: `nc_rate_entry`（780×40、行高=アイコン高）

### エントリ表示内容
| 列 | 位置 | 内容 |
|----|------|------|
| 国旗 | x=4 | `[THIS.GetFlag]` |
| 通貨記号 | x=38 | `[THIS.GetNCSymbol]` |
| 段階 | x=38 y=24 | `[THIS.GetNCTier]` |
| 国名 | x=120 | `[THIS.GetName]` |
| レート | x=440 | `[?bsm_nc_rate\|2]` |
| 前月比 | x=555 | `[?bsm_nc_rate_delta\|2+]` |
| 安定度 | x=670 | `[?bsm_nc_stability\|0]%` |

### フィルタ
- 同盟内のみ（`bsm_nc_filter_mode = 0`）: 現在のEAメンバー + 自国
- 世界全体（`bsm_nc_filter_mode = 1`）: UC直結以外の全国

## Scripted Localisation一覧

| 名前 | 用途 |
|------|------|
| `GetNCName` | 通貨フルネーム（例: "米ドル ($)"） |
| `GetNCSymbol` | 通貨記号のみ（例: "$"） |
| `GetNCTier` | 段階テキスト（強/普通/弱） |
| `GetNCIcon` | 状態アイコン（`£nc_*`）。画像未作成の通貨は記号+段階色にフォールバック |
| `GetNCExchangeRate` | 為替レート表示 |
| `GetNCInflation` | インフレ状況表示 |
| `GetNCStability` | 通貨安定度表示 |

## 画像アセット

### 配置場所
`bakasekai/gfx/currency/`

### 命名規則
```
{CURRENCY}.png          # 通常
{CURRENCY}_strong.png   # 強い
{CURRENCY}_weak.png     # 弱い
```

### 仕様
- サイズ: 75×40 px
- フォーマット: PNG
- 通貨コード大文字（例: `USD.png`, `EUR.png`, `JPY.png`）

### 作成済み
- USD, EUR, GBP, JPY, CNY, RUB, KRW, INR, TRY（通常/強/弱）

### 未作成
UC, BRL, MXN, ARS, SAR, EGP, CHF, SEK, AUD, IDR, THB, NGN, ZAR, KES, COP, ILS, TWD, PHP, MYR, MAN, GENERIC（各3枚）

## 拡張方法

新通貨追加手順:
1. `_bsm_national_currency.txt` の`bsm_nc_assign_currency`にタグブロック追加
2. `_bsm_national_currency_sloc.txt` の`GetNCName`/`GetNCSymbol`に1行追加
3. `_bsm_national_currency_l_japanese.yml` にローカライズ追加
4. `_bsm_national_currency.gfx` にスプライト定義追加
5. `gfx/currency/` に画像3枚配置
