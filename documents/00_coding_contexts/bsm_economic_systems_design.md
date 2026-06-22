# 経済系システム設計提案 — GDP / 資源先物 / 威信 / 少サイズ化

- **対象 mod**: HOI4-Bakasekaitizu-MOD（バカ世界地図MOD）
- **作成日**: 2026-06-19
- **ステータス**: 設計提案（未実装）。`every_collection` 数式集約は **実機検証済み（2026-06-19, §11）＝ 動作確認**。
- **根拠**: `Hearts of Iron IV/documentation/` の `script_math_functions.md` / `dynamic_variables_documentation.md` / `script_collection_input.md` / `script_collection_operator.md` を精読。演算子の正本は `script_math_functions.md`（`sqrt`/`exp` は無く `root=2`/`pow` で代用）。

---

## 1. 位置づけ（既存システムとの関係）

| 既存 | 役割 | 本提案との接続 |
|---|---|---|
| UC（統一通貨, `Unified_Currency`/`National_Unity_Power`） | 共通通貨・各種コスト | 先物決済・GDP建て換算の基軸 |
| NCS（国家通貨） | 為替 `bsm_nc_rate`・安定度・インフレ | スポット価格→交易条件→為替、名目GDP |
| EA（経済同盟） | sphere/議席/方針/目標/投資 | 統合度・投資スコアの分母にGDP、資源安全保障に価格 |
| AS（アノマリー）/ Tradition | ステラリス系内政 | 市場(B)がステラリス市場の役を兼ねる |
| 進行中計画 `ea_ncs_math_collections_implementation_plan.md` | EA/NCSの数式化・Collections化 | 本提案のGDP(A)を土台として F1/F5 に供給 |

**未実装で価値が高い3本**＝ **GDP / 資源スポット価格＋先物 / 威信**。本書はこの3本＋少サイズ化＋小品を扱う。

---

## 2. 土台プリミティブ

今回の鍵は2つ。両方とも「ループとtemp変数の山」を消す。

1. **`every_collection`（`value={}` 内の集約）** — コレクションを走査しアキュムレータに足し込む。
   全国 `resource_consumed@steel` 合計・同盟内GDP合計・Σ他国 `opinion@ROOT` を **1式** で。
   → **検証済✅（§11, 2026-06-19）**: `every_collection`（数式版）は動作（COUNT=98／SUM world_fac=2009 が反復版と一致、`@ROOT`解決も確認）。`every_collection_element` は effect 側で反復したい時のみ。
2. **比較演算子が 1.0/0.0 を返す** — `if/limit` ブロックを乗算に置換。
   例: 危機ペナルティ ＝ `max(0, 0.3 - stability) * 40`。

### 2.1 集約の2経路（設計上の分岐）

| 経路 | 構文 | 状態 | 用途 |
|---|---|---|---|
| 数式集約 | `value = { value=0  every_collection = { named_collection=X  add=… } }` | **検証済✅** | 1式でSUM/AVG/COUNT。最軽量。**第一候補** |
| エフェクト反復（フォールバック） | `every_collection_element = { input={…}  add_to_temp_variable=… }` | 実証済 | 数式集約が不可/制限時。確実 |

設計は数式集約を第一候補に書くが、各式に「不可ならエフェクト反復」の退避を併記する。

---

## 3. システムA — GDP（全体の分母ハブ）

**狙い**: GDPを1回キャッシュすれば、債務/GDP・赤字/GDP・1人当たり・成長率・順位、そして既存計画の統合度(F1)・投資必要度(F5)がすべて**比率で安定**する（0–100 / 0–1 に収まりオーバーフロー回避）。

### 3.1 実質GDP — 実装(2026-06-19, V1): 既存UC生産ベースを再利用

当初の「工場+max_manpower」案は人口proxyが破綻した（人員が巨大で人口がGDPの90%を支配）ため、既存UC月次式 `ucs_add_Unified_Currency_month` の**生産ベースを再利用**する形に変更（`bakasekai/common/scripted_effects/_bsm_econ_gdp.txt` の `bsm_econ_update_gdp`）。

```txt
output    = (num_of_civilian_factories + 1) × (0.4 + 0.6×stability + Cultural_Degree)
state_sum = Σ[owned_controlled_states] (state_population_k/1000)
            × max(1.0, infrastructure_level×1.25 + building_level@air_base×1.1 + building_level@naval_base×0.8)
bsm_gdp_real = output × state_sum / 10      # 除数10でGDPを3-4桁に。clamp[0,1e8]でoverflow保険
```

= 資本(工場) × 生産性(安定度+文明度) × 発展度付き労働(人口×インフラ)。集約は `for_each_scope_loop`(owned_controlled_states) + `PREV` temp 蓄積（UCコードと同パターン）。

- **資源**: `bsm_resource_value`(6資源×固定単価)は別計上で保持するが、固定単価がGDPを歪める（露81%/仏42%）ため**コアから除外**。System B(§4)のスポット価格実装後に実勢で再加算する。
- **安定度**: UC式は素の `stability` だが、GDPは capacity 寄りにするため下限0.4(`0.4+0.6×stability`)。不安定国の過度な沈下を防ぐ（GDPとUCはここだけ意図的に乖離）。
- **文明度** `Cultural_Degree` は実測 ~0.05 の事実上スタブ（将来の拡張フック）。
- **成長率** `bsm_gdp_growth_pct` = 前月値 `bsm_gdp_last` との差分。名目/UC建ては NCS の物価・`bsm_nc_rate` で換算予定。
- 実測GDP(1936, 安定度下限適用後): 日本4806 / 仏2109 / 英1336 / 露714 / ヨーロッパ王国137。

### 3.2 派生指標（すべて比率＝安定）

```txt
debt_to_gdp        = bsm_debt / bsm_gdp_real
gdp_per_capita     = bsm_gdp_real / (max_manpower_k + 1)     # 0除算保険に +1
gdp_growth_pct     = (bsm_gdp_real - bsm_gdp_last) / (bsm_gdp_last + 1) * 100
```

---

## 4. システムB — 資源スポット価格 ＋ 先物市場

`資源の先物` と `ステラリス系（Galactic Market）` を1システムで両取り。global スコープで価格を持ち、各国が参照。

### 4.1 ワールド・スポット価格（供給/需要）

```txt
# 供給フロー = 累積の差分（global_resource_extracted@ は累積値なので必ず差分でフロー化）
set_variable = { var = t_supply
    value = global_resource_extracted@steel  subtract = bsm_steel_extracted_last }
set_variable = { var = bsm_steel_extracted_last  value = global_resource_extracted@steel }

# 需要 = 全国 resource_consumed@steel の合計
#   第一候補（数式集約・要検証）:
set_variable = { var = t_demand
    value = { value = 0
        every_collection = { named_collection = bsm_market_countries  add = resource_consumed@steel } } }
#   フォールバック（実証済エフェクト反復）:
#   set_temp_variable = { t_demand = 0 }
#   every_collection_element = { input = { input = game:all_countries name = MKT }
#       add_to_temp_variable = { t_demand = resource_consumed@steel } }

# 価格 = base × (需要/供給)^弾力性 をクランプ。価格は連続値なので round しない
set_variable = { var = bsm_price_steel
    value = {
        value = t_demand  divide = { value = t_supply  max = 1 }   # 0除算保険
        max = 0.1
        root = 2                          # 弾力性0.5。一般の e は pow = e（分数pow=近似）
        multiply = bsm_price_steel_base
        clamp = { min = 1 max = 999 }
    } }
```

- **景気循環**: `sin(num_days × 周期)` で決定論的な波。ショックは `set_variable_to_random`。RNG無しでも周期は作れる。
- **波及先**: NCS為替（資源輸出国＝交易条件改善で通貨高）／ GDPの資源項 ／ EA資源安全保障目標(F3)。

### 4.2 先物契約（本来の「先物」）

並列配列で複数契約を保持（`hoi4-advanced-arrays` の parallel arrays + FIFO）。

| 配列（country, 値=契約属性） | 内容 |
|---|---|
| `bsm_fut_strike^i` | 約定価格 |
| `bsm_fut_qty^i` | 数量 |
| `bsm_fut_expiry^i` | 満期（`num_days` + N） |
| `bsm_fut_res^i` | 対象資源トークン（または資源IDのフラット配列） |

満期決済（on_monthly、月次は全体1回発火なので非冪等でOK）:

```txt
# payoff = (満期スポット − 約定価格) × 数量。負＝損失
set_temp_variable = { var = t_payoff
    value = { value = bsm_price_steel  subtract = bsm_fut_strike^i  multiply = bsm_fut_qty^i } }
add_to_variable = { Unified_Currency = t_payoff }
```

- **ヘッジ用途**: 資源輸入国が価格固定で戦時予算安定／輸出国が収入固定。AIにも「危機国はヘッジ」と意味を持たせられる。
- **UCシンク/ソース**として優秀（EA準備金・AS解析コストと並ぶ）。マージン/レバレッジも `clamp`/乗算で数式化。

---

## 5. システムC — 威信（Prestige）

国家の格を表す横断スコア。外交AI・EA加盟誘致・大国判定の共通ドライバ。

```txt
set_variable = {
    var = bsm_prestige
    value = {
        value = bsm_prestige  multiply = 0.98                          # 月次減衰
        add = { value = num_researched_technologies  multiply = 0.5 }  # 科学
        add = { value = bsm_gdp_real  divide = 50 }                    # 経済力
        add = { value = num_subjects  multiply = 3 }                   # 覇権
        add = bsm_world_respect                                        # Σ他国 opinion（下記）
        subtract = { value = bsm_recent_capitulation  multiply = 30 }  # days_since_capitulated で判定
        clamp = { min = 0 max = 1000 }
    }
}

# 世界からの敬意（数式集約・要検証）: 他国が自国(ROOT)に抱く opinion の合計
# bsm_world_respect = { value=0  every_collection={ named_collection=bsm_market_countries  add=opinion@ROOT } }
#   ※ @ROOT が集約の内側で正しく解決するかは §11 の最重要検証項目
```

- 使える素材が豊富: `num_researched_technologies` / `total_constructed_nuclear_reactor` / `convoys_destroyed` / `pc_total_score` / `num_faction_members`。
- 順位は collection の argsort（`hoi4-advanced-arrays`）。
- 出力先: EA加盟バイアス `bsm_ea_join_bias`（威信高い盟主は人気）、`add_ai_strategy` の重み、大国閾値。

---

## 6. システムD — 既存システムの少サイズ化

新機能ではなく**回収**。§2 のプリミティブで実コードを縮める。

| 既存の重い書き方 | 置換 | 効果 |
|---|---|---|
| NCS `bsm_nc_prepare_rate_list` の地域別 `every_country` 分岐 | 地域 collection ＋ 数式集約/反復 | 分岐・temp変数の消滅 |
| EA平均/危機カウントの `for_each_loop`+temp加算 | `value={ every_collection … }` 1式 | 計画 F1/F2 がそのまま短縮 |
| `if={limit={check_variable…}}` の分岐の山 | `max(0, 閾値 - x) * 係数` の乗算分岐 | if ブロック消滅 |
| 各システムが工場/資源を個別再計算 | §3 のGDPを1回算出して共有 | 重複計算の削減 |

NCSは既に「計算の数式化」を開始済（直近コミット）なので、その延長。効果は `imgui show profiler` の Script タブで月次負荷を実測しながら確認する。

---

## 7. システムE — その他ステラリス系（小品）

AS・Tradition が既にあるため、**重複しない**追加候補のみ。

- **交易価値＋海賊**: `convoy_threat` / `mine_threat`（共に0–1で読める）で交易価値が目減り、護衛で回復。Bと地続き。
- **勅令(Edicts)**: UCを払い帝国全体に時限 dynamic modifier。軽量・即実装可。
- **メガストラクチャ**: 多段建造を進捗変数で追い、段階で逓増modifier＋威信。
- **経済Traditionツリー**: 既存Tradition基盤に GDP/威信で解放する経済枝を追加。

---

## 8. 全体接続（マクロループ）

```
資源産出(global_resource_extracted) ─→ スポット価格(B) ─→ 先物/ヘッジ(B, UC決済)
        │                                  │
        ▼                                  ▼
   GDP(A) ◀── 工場/人口/技術           NCS為替(交易条件)・インフレ
        │
        ├─→ 威信(C) ─→ 外交AI / EA加盟誘致 / 大国判定
        └─→ EA(統合度F1・準備金拠出F4・投資F5・資源安全保障F3)
```

すべて**GDPを分母**に正規化 → 比率が 0–1 / 0–100 に収まり、オーバーフロー＆クランプ地獄を回避。資源→価格→交易→GDP→通貨→威信→外交がドキュメントの数式＋変数だけで閉じる。

---

## 9. 技術的注意（落とし穴）

1. **`sqrt`/`exp` は存在しない** → √は `root = 2`、指数は `pow`（底2.71828）。どちらも近似なので整数が要る所だけ `round = yes`。**価格など連続値は round しない**。
2. **パーサーのカスケード破損** — 未知演算子が1個あると同ファイルの**それ以降の全 `value={}` が黙って0化**。新規数式ファイルは必ず `search_defs.py --check` → cwtools 検証。
3. **固定小数オーバーフロー** — GDP/価格はスケール必須（`_k` 変数を使う・単位を大きく取る・`clamp` で蓋）。`pow` は特に危険。
4. **`global_resource_extracted@` は累積値** → フロー化は前月との差分。
5. **`every_collection`(数式) は検証済✅(2026-06-19)** — COUNT=98 / SUM `world_fac`=2009 が反復版と一致し、per-element 変数の直読も可。`every_collection_element`+temp フォールバックは不要（effect 側で反復したい時のみ）。
6. **`@ROOT` の集約内スコープ解決も検証済✅** — `sum_opinion@ROOT=-490`(非0)。威信の Σopinion が成立。なお `element_value` は scope コレクションでは 0（値コレクション用と思われる→使わない）。
7. **on_monthly/on_weekly は全体で1回発火**（EA文書§11）→ 先物満期決済など非冪等処理は1回で正しく動く。

---

## 10. 推奨実装順

1. **GDP(A)** — 最優先。F1/F5 の精度と安定を底上げする最小コストの土台。
2. **スポット価格→先物(B)** — 新規性最大。UCシンク・NCS為替・ステラリス市場を一気に賄う。
3. **威信(C)** — 外交/EA誘致と接続して旨味を出す。
4. **少サイズ化(D)** — B/C 実装中に「ついで」に集約化していく。

**着手前の必須ゲート**＝ §11 の数式集約検証。これが通れば A・B・C が一気に書ける。

---

## 11. 検証（実施済み ✅ 2026-06-19）

`bsm_test`（別repo）に**集約検証ディシジョン** `bsm_mt_agg_probe_run`（Decisions → 数式テスター → 「集約検証ログを出力」）を追加済み。GUIのACC目視ではなく、結果を **`game.log`** に出力して正確な数値を取得する（`scripted_effects/_bsm_mathtest_agg_probe.txt`）。プローブは専用ファイルに隔離し、最も怪しい `element_value` を最後に置く（カスケード破損の封じ込め）。

| 検証項目 | 式 | 期待 / 判定 |
|---|---|---|
| 集約が回るか（COUNT） | `value=0 every_collection={named_collection=bsm_mt_all_countries add=1}` | `[BSM_MT_AGG] math count` が `[BSM_MT_AGG_FB] count`（実証済反復）と一致すればOK |
| 要素スコープの変数直読 | `… add=num_of_factories` | `math world_fac` が `FB world_fac` と一致すればSUM可 |
| `@ROOT` の内側解決 | `… add=opinion@ROOT` | `math sum_opinion@ROOT` が非0ならプレステージ式が成立 |
| `element_value` の正体 | `… add=element_value` | 何が足されるか観察（最後・最も怪しい） |

### 検証結果（大日本帝国・1936）✅ 数式集約は動作する

| 項目 | FB(反復) | math(`every_collection`) | 判定 |
|---|---:|---:|---|
| count | 98 | 98 | ✅ 一致 |
| world_fac | 2009 | 2009 | ✅ 一致＝**per-element 変数の直読が可能** |
| sum_opinion@ROOT | — | -490 | ✅ 非0＝**@ROOT が集約内で解決**（威信式が成立） |
| element_value | — | 0.00 | scope コレクションでは 0（値コレクション用→不要） |

- **結論**: `every_collection` 数式集約は本ビルドで動作。GDP・資源需要合計・威信の Σopinion はすべて **1式** で書ける。`every_collection_element`+蓄積のフォールバックは**不要**（effect 側で反復したい場合のみ使用）。
- これにより §10 の A/B/C と §6 の少サイズ化は全面 GO。`[BSM_MT_AGG_FB]`（反復）行は「正解値」の照合用として残してよい。

### ゲーム内テスト（実装後）

| テスト | 手順 | 確認 |
|---|---|---|
| GDP | 月次更新 | `bsm_gdp_real` が妥当値・成長率が出る |
| スポット価格 | 産出/消費を変動 | 価格が需給で動き clamp 内 |
| 先物 | 契約→満期送り | payoff が UC に反映（損益両方向） |
| 威信 | 技術/従属/opinion 変動 | 威信が動き 0–1000 内 |
| 少サイズ化 | profiler Script タブ | 月次負荷が悪化しない |
