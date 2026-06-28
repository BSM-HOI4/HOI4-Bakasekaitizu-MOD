# AIデバッグ リファレンス

AIが想定どおり動かないときの調査手順。コマンドの全リストは
`documents/00_coding_contexts/console_commands_documentation.md` を参照。

## 基本コマンド

| コマンド | 用途 |
|---|---|
| `human_ai` | プレイヤー国もAI操作にする(観戦しながらAI挙動を確認) |
| `aiview` | AIデバッグ表示を有効化。国を選択すると戦略値・態度・目標が見える |
| `tdebug` | デバッグ情報表示(state ID・国TAG等の確認に必須) |
| `tag <TAG>` | 操作国を切り替えて当事国の内部状態を直接確認 |
| `event <id> <TAG>` | flag切替イベント等を対象国に発火 |
| `fronts` / `debug_fronts` | 戦線の可視化 |
| `instantconstruction` | 建設即時完了(生産AIの確認を高速化) |
| `focus.autocomplete` / `focus.nochecks` | NF進行の高速確認 |
| `research_on_icon_click` | 研究即時完了 |
| `reload interface` / `reload localisation` | GUI/loc再読み込み(AIファイル自体はリロード不可、再起動が必要) |

**注意**: `common/ai_*` の変更はゲーム再起動が必要。`reload` 系では反映されない。

## 症状別チェックリスト

### AIが宣戦しない
1. 正当化(CB)はあるか — `ai_strategy` の `antagonize`/`declare_war` はCBがないと宣戦に至らない
2. `declare_war` / `conquer` の合計値を `aiview` か変数 `ai_strategy_declare_war@TAG` で確認
3. 陣営所属なら陣営リーダーの戦争許可ルールに阻まれていないか
4. 世界緊張度(threat)が宣戦要件を満たすか(国是・game ruleの確認)
5. `prepare_for_war` で準備だけして開戦値が足りないケースが多い — `declare_war` も併せて積む

### AIがNFを取らない
1. NF側 `ai_will_do` が `factor = 0` になっていないか
2. `ai_strategy_plans` の `focus_factors` で0にされていないか / `ai_national_focuses` リストの順序待ちでないか
3. NFの `available`/`prerequisite` を満たしているか(`focus.nochecks` で切り分け)
4. 歴史AI設定(`is_historical_focus_on`)とプランのenable条件の不一致

### AIがイベントで想定外の選択肢を選ぶ
1. 全optionに `ai_chance` が明示されているか(未指定optionが混ざると比率が崩れる)
2. modifierのトリガーがAI国で成立しているか `tag <TAG>` で確認

### AIが師団・装備を作らない
1. テンプレートに必要な研究をAIが終えているか(`ai_strategy_plans` の `research` 重み不足が典型)
2. `ai_templates` のグループ `role` と `ai_strategy` の `role_ratio`/`unit_ratio` の整合
3. 装備設計には XP が必要 — XPがゼロのまま停滞していないか
4. 海軍: taskforce要求艦種と `ai_equipment` の `roles` 供給の整合([ai_navy_reference.md](ai_navy_reference.md))

### AI戦略値の実値確認(localisationハック)

一時的にデバッグ用decisionやGUIテキストに変数を仮置きすると、aiviewより細かく追える:

```
# 任意の常時表示locに仮置き(検証後必ず除去)
DEBUG_AI_LINE:0 "conquer:[?ROOT.ai_strategy_conquer@ESP] befriend:[?ROOT.ai_strategy_befriend@ESP]"
```

利用可能な `ai_strategy_*` 変数一覧: `documents/00_coding_contexts/dynamic_variables_documentation.md`

## パフォーマンス調査

- `imgui show profiler` → Script タブ。`on_actions` の hourly/daily と decision のAI評価が主な負荷源
- `ai_strategy` の `enable` が重い場合もここに現れる。`original_tag`/flagチェックを先頭に置いて早期returnさせる

## テストシナリオ

- 観戦テスト: 新規ゲーム → `human_ai` → 速度5で対象年まで放置 → 対象国の挙動を記録
- 再現テスト: `tests/` に検証用イベント(`_bsm_*_test.*`)を置き、flag切替→AI挙動の変化を確認(AGENTS.mdのテスト方針準拠)
- 構文チェック: `mcp__hoi4__hoi4_cwtools_check` / `hoi4_lint` を変更ファイルに実行してから起動する
