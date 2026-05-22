# BSMmod システムドキュメント索引

本ドキュメントは、BSMmodの主要システムに関する詳細なドキュメントをまとめたものです。

## ドキュメント一覧

### 1. [文明度システム](./civilization_degree_system.md)

**変数**: `Cultural_Degree` (0-100%)

**概要**: 国家の文化的・技術的発展度を表すシステム

**主な機能**:
- 特性スロット解放（30%→1スロット、50%→3スロット、80%→5スロット、100%→6スロット）
- 国家統合力に毎週加算
- アノマリー研究の解禁条件と速度ボーナス
- 統一通貨獲得効率に影響

**主要な獲得要因**:
- アノマリー報酬
- 伝統・アセンションパーク
- 特性「文化的遺産」

**更新頻度**: 週次

---

### 2. [国家統合力システム](./national_unity_power_system.md)

**変数**: `National_Unity_Power` (0-∞)

**概要**: 国家の統合度を表すリソース。伝統取得、探検隊派遣などに使用

**主な機能**:
- 伝統取得（100統合力/伝統）
- 探検隊派遣（50統合力/探検隊）
- 経済同盟信頼度計算
- 軍事偵察隊成功率に影響

**主な獲得要因**:
- 毎日のmodifierによる獲得
- 文明度（毎週加算）
- アノマリー報酬
- 探検隊完了

**更新頻度**: 日次（modifier）、週次（文明度）

---

### 3. [統一通貨システム](./unified_currency_system.md)

**変数**: `Unified_Currency` (整数値)

**概要**: 国家の経済力を表すリソース。民需工場出力、安定度、文明度、人口、インフラなど様々な要因に基づいて計算

**計算式**:

```
[
    SUM{ 人口(m) × (インフラ×1.25 + 飛行場×1.1 + 港湾×0.8) }
    × 民需出力 × (安定度 + 文明度)
    - (徴兵(m) × ステート数)
] / 100 × 係数
```

**係数の構成**:
- 基本値(1)
- UC獲得補正(modifier@Unified_Currency_gain_factor)
- 生産効率ボーナス(production_factory_max_efficiency_factor × 0.5)
- 消費財係数(consumer_goods_factor × 0.5)
- 戦時ペナルティ(-1.5% × 月数 × (1 - 戦争支持率×0.5))
- 経済同盟ボーナス(同盟数×10%, 上限30%)
- 宗教係数(modifier@Unified_Currency_religion_factor)

**主な消費先**:
- 探検隊派遣
- 未知の解明
- 金への変換

**更新頻度**: 日次

---

### 4. [ステラリス要素システム](./stellaris_elements_system.md)

**主な変数**:
- 伝統: `bsm_stellaris_tradition_economy`, `bsm_stellaris_tradition_military`, `bsm_stellaris_tradition_society`, `bsm_stellaris_tradition_civilization` (0-5)
- 特性: `bsm_stellaris_trait_slots` (0-6), `bsm_stellaris_traits_equipped` (0-6)
- 探検隊: `bsm_stellaris_expedition_count`, `bsm_stellaris_expedition_active`
- アノマリー: `bsm_stellaris_anomaly_research_bonus` (0.01-0.5)

**概要**: Stellarisの要素を取り入れたシステム。伝統、特性、アセンションパーク、探検隊、アノマリーを管理

**主な機能**:
- 伝統取得（統合力消費）
- 特性装備（文明度連動）
- 探検隊派遣（統合力消費）
- アノマリー研究（文明度連動）

**システム構成**:
1. 伝統（Traditions）: 経済・軍事・社会・文明の4カテゴリ、各5レベル
2. 特性（Traits）: 固定特性6種、追加特性10種
3. アセンションパーク（Ascension Perks）: 8種、伝統10つ取得ごとに1スロット解放
4. 探検隊（Expeditions）: 学術・軍事・商業・科学の4タイプ
5. アノマリー（Anomalies）: 文明度に応じた難易度、研究速度は文明度と伝統に依存

**更新頻度**: 週次（特性スロット更新、アノマリー研究速度計算）

---

## システム間の関係

### 文明度 ↔ 統合力

- 文明度 → 統合力: 毎週、文明度の値が統合力に加算
- 文明度 → 特性スロット: 文明度に応じて特性スロット解放
- 統合力 → 文明度: アノマリー報酬からの統合力獲得チャンス（文明度も同時に獲得可能）

### 文明度 ↔ 統一通貨

- 文明度 → 統一通貨: 安定度と文明度の合計が民需出力に乗算される
- 文明度 → アノマリー: アノマリー研究の解禁条件と速度ボーナス

### 統合力 ↔ ステラリス要素

- 統合力 → 伝統: 100統合力/伝統で消費
- 統合力 → 探検隊: 50統合力/探検隊で消費
- 統合力 ← アノマリー: 報酬からの統合力獲得チャンス
- 統合力 → 経済同盟: 統合力 × 0.05 が信頼度に加算

### 文明度 ↔ ステラリス要素

- 文明度 → 特性スロット: 文明度に応じてスロット解放
- 文明度 → アノマリー: 解禁条件と研究速度ボーナス
- 文明度 ← 伝統: 文明伝統で文明度獲得
- 文明度 ← 特性: 「文化的遺産」で文明度獲得

## 関連ファイル

### 共通スクリプト効果
- `common/scripted_effects/_bsm_stellaris_effects.txt` - ステラリス要素システム
- `common/scripted_effects/_bsm_stellaris_anomaly_integration.txt` - アノマリー報酬・研究速度
- `common/scripted_effects/_bsm_stellaris_anomaly_mapping.txt` - アノマリーカテゴリマッピング
- `common/scripted_effects/_bsm_anomaly_system.txt` - アノマリーデータベース
- `common/scripted_effects/_bsm_anomaly_effects.txt` - アノマリー研究進行
- `common/scripted_effects/_bsm_Unified_Currency.txt` - 統一通貨計算
- `common/scripted_effects/bsm_ea_goals_effects.txt` - 経済同盟信頼度計算

### 共通トリガー
- `common/scripted_triggers/_bsm_stellaris_triggers.txt` - アノマリー解禁判定

### 共通決定
- `common/decisions/_bsm_stellaris_decisions.txt` - 伝統取得決定

### 共通GUI
- `common/scripted_guis/bsm_stellaris.txt` - 研究・発見画面

### 共通アイデア
- `common/ideas/_bsm_stellaris_traits_detailed.txt` - 伝統・特性アイデア
- `common/ideas/_bsm_system.txt` - modifierを持つアイデア

### 共通オンアクション
- `common/on_actions/_bsm_system.txt` - 週次処理（文明度・統合力・特性スロット・アノマリー研究速度）
- `common/on_actions/_bsm_system.txt` - 日次処理（統一通貨）

### 共通modifier定義
- `common/modifier_definitions/_bsm_core.txt` - modifier定義

### 共通ローカライズ
- `localisation/japanese/bakasekai/_bsm_stellaris_l_japanese.yml` - ステラリス要素ローカライズ
- `localisation/japanese/bakasekai/bsm_system_l_japanese.yml` - システムローカライズ

## 効率的な運用方法

### 初期〜中期

1. **文明度の優先**:
   - 特性スロットを解放（30%を目標）
   - アノマリー研究を可能にする（20%以上）

2. **統合力の確保**:
   - 毎日のmodifierを最大化
   - 文明度を上げて毎週の獲得量を増やす

3. **統一通貨の増加**:
   - 民需工場の増設
   - インフラの整備（特に道路）
   - 安定度と文明度の向上

### 中期〜後期

1. **伝統の取得**:
   - 経済・軍事・社会・文明伝統をバランスよく取得
   - 特に文明伝統は文明度獲得効果があるため優先

2. **特性の装備**:
   - プレイスタイルに合わせて特性を選択
   - 文明度が高いほど多くの特性を装備可能

3. **アセンションパークの取得**:
   - 伝統10つ取得ごとに1スロット解放
   - 効果的なパークを優先して取得

4. **アノマリー研究**:
   - 報酬からの文明度・統合力獲得を狙う
   - 高難易度のアノマリーは文明度が上がってから研究

5. **探検隊の派遣**:
   - 新特性やアノマリーを発見
   - 軍事偵察隊は統合力が高いほど成功率が高い

### 終盤

1. **文明度の最大化**:
   - 100%を目標に特性スロットを最大解放

2. **伝統の完成**:
   - 全ての伝統をレベル5まで取得

3. **アセンションパークの完成**:
   - 8スロットすべてを埋める

4. **特性の最適化**:
   - プレイスタイルに最適な6つの特性を装備

## 注意事項

1. **初期化**: ゲーム開始時、全ての変数が0からスタート
2. **文明度の重要性**: 文明度は多くのシステムに影響するため、最優先で向上させる
3. **統合力の計画**: 伝統と探検隊のバランスを考慮して消費を計画
4. **統一通貨の計算**: 計算式が複雑なので、人口・インフラ・民需工場・安定度・文明度のバランスを考慮
5. **従属国の影響**: 自治度が低い従属国は、経済力が大幅に制限される
6. **戦争の影響**: 戦争が長引くと、統一通貨に大きな負担がかかる
7. **週次処理**: 多くの変数が毎週更新されるため、変更が反映されるまで1週間待つ必要がある

## チート用決定

デバッグ用として、以下の決定が存在します：

- `debug_cd_set`: 文明度を80%に設定
- `debug_po_set`: 統合力を80に設定
- `debug_ucs_on_monthly`: 統一通貨の日次獲得を実行

これらは `common/decisions/_debug_decisions.txt` に定義されています。

## 更新履歴

- 2026-04-10: 初版作成
