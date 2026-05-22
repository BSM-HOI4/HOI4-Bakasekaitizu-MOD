# 経済同盟 (Economic Alliance) 仕様書

## 1. 概要
経済同盟は、軍事的な陣営（Faction）とは独立して存在できる、国家間の経済的な協力関係を表すシステムです。
加盟国は、同盟全体の対する自国の経済規模の割合に応じた政治力のボーナスを得ることができます。

## 2. 基本構造
*   **構造**: 1つの「盟主 (Leader)」と複数の「加盟国 (Member)」で構成されます。
*   **重複参加**: 現行の仕様では、1国につき1つの経済同盟にのみ参加可能です（変数は配列で管理されていますが、アクションなどでは単一同盟への参加を前提とした挙動となっています）。
*   **陣営との関係**: 軍事同盟（Faction）とは別枠です。陣営に所属していても経済同盟に参加可能です。

## 3. 恩恵（ボーナス）
### 政治力増加 (Political Power Gain)
経済同盟に参加している全国家（盟主含む）は、以下の計算式に基づき政治力獲得補正を得ます。

*   **計算式**: `(自国のIC / 同盟全体の総IC)`
*   **更新頻度**: 毎週 (Weekly Pulse)
*   **上限キャップ**: 最大 **5%** (+0.05)
*   **実装**: 動的補正 `bsm_economic_alliance_pp_buff` が付与されます。

## 4. 外交アクション (Scripted Diplomatic Actions)
以下の外交アクションが実装されています。

| アクション名 | 実行者 | 対象 | コスト (PP) | 条件概要 |
| :--- | :--- | :--- | :--- | :--- |
| **加盟申請 (Join)** | 非加盟国 | 盟主 | 25 | 戦争中でない、対象が盟主である |
| **脱退 (Leave)** | 加盟国 | 盟主 | 50 | 戦争中でない、自分が加盟国で対象が盟主 |
| **追放 (Kick)** | 盟主 | 加盟国 | 100 | 自同盟の加盟国である |
| **勧誘 (Invite)** | 盟主 | 非加盟国 | 25 | 友好関係 > 0 |
| **結成 (Create)** | 非加盟国 | 非加盟国 | 50 | 双方が未加盟、友好関係 > 0 |

※ いずれも承認制であり、対象国にイベントが送られ、受諾されると効果が発揮されます。

## 5. ディシジョン (Decisions)
外交アクションを補完、またはAI向けの挙動として以下のディシジョンが存在します。

*   **汎用経済同盟の結成**: 隣国に対して結成を打診します。
*   **汎用経済同盟への加盟**: 隣国の盟主に対して加盟を打診します。
*   **脱退**: 特定の同盟ID（EU, Allies, GEACPS）や汎用同盟からの脱退を行います。

## 6. 技術仕様 (Technical Details)
### 主要フラグ・変数
*   `is_economic_alliance_leader`: 盟主であることを示す国フラグ。
*   `economic_alliance_ids`: その国が所属している同盟IDを格納する配列。
*   `global.economic_alliance_leader^ID`: 特定の同盟IDの盟主の国ID（Global変数）。
*   `economic_alliance_members`: （計算処理内などで使用）同盟メンバーのリスト。

### 関連ファイル
*   **アクション定義**: `common/scripted_diplomatic_actions/BSM_economic_alliance_actions.txt`
*   **イベント**: `events/bsm_economic_alliance_events.txt`
*   **効果（ロジック）**: `common/scripted_effects/bsm_economic_alliance_*`
*   **計算ロジック**: `common/scripted_effects/bsm_economic_alliance_calculations.txt`
*   **ディシジョン**: `common/decisions/bsm_economic_alliance_decisions.txt`
