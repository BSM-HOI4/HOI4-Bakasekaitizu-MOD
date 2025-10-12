# Generic National Focus Tree Implementation

## 概要 (Overview)

`generic2.txt`に全22のイデオロギーに対応したNational Focusツリーを実装しました。

## 実装内容

### 基本構造

- **ルートフォーカス**: `generic_political_awakening` (x=-10, y=0)
  - すべてのイデオロギーフォーカスの起点
  - 政治力+150を付与

### イデオロギー別フォーカスツリー (22種類)

各イデオロギーには以下の特徴があります：

1. **エントリーフォーカス** (`generic_[ideology]_path`)
   - `allow_branch`条件により、該当イデオロギーの国のみ表示
   - `ai_will_do`で、AIは初期イデオロギーと同じものを優先

2. **ユニークフォーカス数**: 各イデオロギー12個
   - 合計フォーカス数: 260個 (1ルート + 22エントリー + 237ユニーク)

3. **必須属性**:
   - ✓ `cost = 10` (すべて10以下)
   - ✓ `relative_position_id` (位置関係を明確化)
   - ✓ `ai_will_do` (AI挙動制御)
   - ✓ `search_filters = { FOCUS_FILTER_POLITICAL }`
   - ✓ `available_if_capitulated = yes`

### イデオロギー配置 (X座標)

各イデオロギーツリーは4マス間隔で横に配置されています：

| イデオロギー | X座標 | 特徴 |
|------------|------|------|
| democratic_ideology | 0 | 民主主義 - 選挙、自由、権利重視 |
| communism_ideology | 4 | 共産主義 - 革命、計画経済、赤軍 |
| fascism_ideology | 8 | ファシズム - 独裁、軍国主義、拡張主義 |
| neutrality_ideology | 12 | 中立 - 孤立、安定、伝統 |
| civilism | 16 | 市民主義 - 都市開発、地方自治 |
| conservative_democracy | 20 | 保守民主主義 - 伝統、制度、安定 |
| constitutional_monarchy | 24 | 立憲君主制 - 王冠、憲法、議会 |
| direct_democracy | 28 | 直接民主制 - 参加、国民投票、透明性 |
| futurism | 32 | 未来主義 - 技術、自動化、進歩 |
| intellectualism | 36 | 知識主義 - 研究、教育、知恵 |
| mythologicalism | 40 | 神話主義 - 信仰、神殿、聖地 |
| rightneutrality | 44 | 右派中立 - 階層、貴族、帝国 |
| anarchism | 48 | アナーキズム - 国家廃止、労働者評議会 |
| stupidism | 52 | 愚鈍主義 - カオス、不条理、創造的狂気 |
| technicalism | 56 | 技術至上主義 - テクノクラシー、自動化 |
| philanthropy | 60 | 博愛主義 - 慈善、人道支援、平和 |
| transformationism | 64 | 変革主義 - 加速的変化、芸術革命 |
| ruinism | 68 | 破滅主義 - 破壊、原始主義、ニヒリズム |
| longitudinalism | 72 | 縦方向主義 - 垂直階層、命令系統 |
| horizontalism | 76 | 横方向主義 - 平等分配、協力ネットワーク |
| hinnulism | 80 | ヒンヌリズム - 文化洗練、美的価値 |
| kyonulism | 84 | キョヌリズム - 文化的魅力、保護本能 |

## フォーカス構造例

### democratic_ideology (民主主義)

```
generic_political_awakening (ルート)
    ↓
generic_democratic_path (民主主義の道)
    ↓
generic_democratic_consolidation (民主主義の強化)
    ├── generic_democratic_elections (選挙)
    ├── generic_democratic_freedoms (自由)
    └── generic_democratic_rights (権利)
        └── ... (計12フォーカス)
```

## AI挙動

各イデオロギーパスフォーカスには以下のAI設定があります：

```
ai_will_do = {
    factor = 10
    modifier = {
        factor = 0
        NOT = { has_government = [ideology] }
    }
}
```

これにより：
- AIは自国の現在のイデオロギーに対応するツリーのみを選択
- 他のイデオロギーツリーは選択しない (factor = 0)

## allow_branch条件

各イデオロギーツリーは`allow_branch`により、該当イデオロギーの国のみ表示：

```
allow_branch = {
    has_government = [ideology]
}
```

※4大イデオロギー（democratic, communist, fascist, neutrality）は、
他の4大イデオロギーを持たない国も選択可能なOR条件を含む。

## 報酬の種類

フォーカス完了時の報酬：
- 政治力 (political_power): 50-150
- 安定度 (stability): 0.05-0.15
- 戦争協力度 (war_support): ±0.05-0.15
- 研究スロット (research_slot): +1
- アイデア追加
- イデオロギー人気度増加

## 検証結果

✓ 括弧のバランス: 1513組 (完全一致)
✓ 総フォーカス数: 260個
✓ すべてのフォーカスにcost=10設定済み
✓ すべてのフォーカスにai_will_do設定済み (ルート除く)
✓ すべてのフォーカスにrelative_position_id設定済み (ルート除く)
✓ 22イデオロギーすべてに対応

## ファイル情報

- **ファイルパス**: `bakasekai/common/national_focus/generic2.txt`
- **総行数**: 4505行
- **総フォーカス数**: 260個
- **イデオロギー数**: 22種類

## 今後のテスト項目

ゲーム内で以下を確認する必要があります：

1. フォーカスツリーが正しく表示されるか
2. イデオロギーに応じて適切なブランチのみが表示されるか
3. AIが正しくフォーカスを選択するか
4. 報酬が正しく付与されるか
5. prerequisiteチェーンが正しく機能するか
6. フォーカス完了時にエラーが発生しないか

## 注意事項

- このフォーカスツリーは`generic_focus`として定義されており、専用NFツリーを持たない国が使用します
- `has_country_flag = management_system`を持つ国は使用しません (factor = 0)
- すべてのフォーカスは降伏後も使用可能 (`available_if_capitulated = yes`)

## 作成方法

1. 手動実装: democratic, communist, fascist, neutrality, civilism, conservative_democracy, constitutional_monarchy, direct_democracy, futurism, intellectualism (10種類)
2. Python自動生成: 残り12種類のイデオロギー
3. 構文検証と修正

---

実装完了日: 2025-10-12
