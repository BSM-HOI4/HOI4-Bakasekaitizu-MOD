# 外交AI・講和AI リファレンス

## ai_attitudes(態度の枠組み)

配置: `common/ai_attitudes.txt`

AIが他国に対して取る「態度」の定義。態度の割り当て自体はエンジン(脅威評価・イデオロギー・ai_strategy値)が行い、
態度ごとの行動フラグをここで定義する。

```
# ROOT = 自国, FROM = 対象国
attitude_neutral = {
}
```

態度が持てる行動フラグ(ファイル冒頭のコメントに準拠):

| フラグ | 意味 |
|---|---|
| `antagonize` | 戦争の潜在的標的とみなす |
| `annex` | 完全征服を望む |
| `weaken` | 弱体化(周辺国の同盟・保障等)を狙う |
| `coalition` | 対抗連合を作りたい |
| `vassalize` | 傀儡化したい |
| `ally` | 同盟を積極的に望む |
| `befriend` | 関係改善したい |
| `protect` | 保護したい |
| `threat` | 脅威として備える |
| `ignore` | 意図的に無視 |
| `warn` | 警告を送る |

### 態度を読む(トリガー)

```
has_attitude = {
  who = GER
  attitude = attitude_hostile
}
```

態度を直接セットする効果はない。動かしたいときは `ai_strategy`(antagonize/befriend等)の値を盛って間接的に誘導する。
→ [ai_strategy_reference.md](ai_strategy_reference.md)

## opinion(関係値)との関係

- opinion modifierは `common/opinion_modifiers/` で定義し、`add_opinion_modifier` で付与(詳細は `hoi4-opinion-modifiers-helper` スキル)
- opinionは同盟参加・通行許可などのAI判断の入力の1つ。ただし**opinionだけでは同盟しない**。`alliance`/`befriend` のai_strategy値とイデオロギー一致が支配的
- 「AIに同盟させたい」最短ルート: 双方向に `ai_strategy = { type = alliance id = X value = 200 }` + opinionを正に + 同陣営障害(既存陣営・中立国是)を除去

## 講和会議AI(peace_conference/ai_peace)

配置: `common/peace_conference/ai_peace/*.txt`(1.12+の新講和システム。**旧 `common/ai_peace/` ではない**)

`peace_ai_desires` ブロック内に「desire(欲求)」を列挙する。各desireは特定の講和アクションへの加点/減点。

```
peace_ai_desires = {

  take_our_cores = {                       # desire名(一意)
    peace_action_type = { take_states }    # 対象アクション(複数可)
    enable = {
      # スコープ連鎖に注意:
      # ROOT = 評価中のAI, ROOT.FROM = 交渉主体,
      # ROOT.FROM.FROM.FROM = 対象state(take_states系の場合)
      ROOT = { tag = ROOT.FROM }                          # 自国のための交渉
      ROOT.FROM.FROM.FROM = { is_core_of = ROOT.FROM }    # 自国コアのstate
    }
    ai_desire = 100                        # 正で促進、大きな負値(-1000)で事実上禁止
  }
}
```

- `peace_action_type`: `take_states`, `puppet`, `force_government`, `liberate`, `annex` など(vanillaの documentation.info 参照)
- スコープ連鎖(`ROOT.FROM.FROM.FROM`)が複雑なので、**必ずmod内の既存desireをコピーして改変する**
- ファイルは番号プレフィックスで整理されている: `00_misc.txt`(共通)→ `0_*`(シナリオ/デフォルト)→ `1_<イデオロギー>` → `2_<国・地域>`
- BSM注意: イデオロギー名は `democratic_ideology` / `communism_ideology` 等の改名済みトークンを使う

### 新しい講和挙動を足す手順

1. 対象がイデオロギー共通なら `1_*.txt`、特定国・地域なら `2_*.txt` 系に追記(または新規 `2_TAG.txt`)
2. 似た既存desireを探してコピー(特に enable のスコープ連鎖)
3. 抑制は `ai_desire = -1000` 級、優先は +50〜+200 が既存ファイルの相場
4. 検証: 講和まで進めるのは重いので、`teleport`/`instantconstruction` 等で戦争を速攻終結させてテスト

## mod内実例

- `bakasekai/common/ai_attitudes.txt`
- `bakasekai/common/peace_conference/ai_peace/00_misc.txt` — コア回収・影響圏カットオフ等の共通ルール
- `bakasekai/common/peace_conference/ai_peace/1_fascist.txt` 等 — イデオロギー別
- `bakasekai/common/peace_conference/ai_peace/0_battle_america.txt` 等 — BSMシナリオ別
- `bakasekai/common/peace_conference/categories/`, `cost_modifiers/` — アクション定義とコスト側
