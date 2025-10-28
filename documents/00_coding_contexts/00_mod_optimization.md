
# HOI4 MOD軽量化ガイド（Y式植林装置解説）

## MODの軽量化とは？

NSBアップデート以降、Paradox公式からMODのパフォーマンス解析ツールが提供されています。以下はその利用方法とMOD軽量化の具体例についての解説です。

---

## パフォーマンスプロファイラの使い方

### ステップ1: 開発者モードで起動
- HOI4を開発者モードで起動
- コンソールで以下を入力：
  ```
  imgui show profiler
  ```

### ステップ2: プロファイラ画面
- 最初はグラフ表示用画面が表示される
- `Enable Collection` を押すと各処理の重さがグラフ化される

### ステップ3: Scriptタブを開く
- 上部タブの `Script` をクリック
- `Start` を押して時間を進め、一定時間経過後に `Stop` を押すと処理時間が一覧表示される

### 各項目の見方
- `ms`：各処理にかかったミリ秒
- `non_assigned`：かかった時間順に処理を分類
- `gamestate.hourly` / `daily` / `weekly`：時間単位で実行されるスクリプト
  - `hourly` の処理が最も頻繁に実行され、パフォーマンスに大きな影響を与える

---

## 軽量化の実例：hourly処理の最適化

### 問題点
- ミッション型ディシジョンの有効化判定が `hourly` 処理に含まれている
- `any_state` は非常に重い処理で、毎時間判定されるとゲームが重くなる

### 対策1: ミッション型を他の実装に変更
- 必要ないものは通常ディシジョンやイベントに切り替える

### 対策2: 早期リターンの活用

#### 重い判定コード例
```hoi4
trigger = {
  any_state = {
    is_controlled_by = ITA
  }
  has_war_with = ITA
}
```
- すべての州を確認してから、戦争状態を確認する流れ → 非効率

#### 最適化コード
```hoi4
trigger = {
  has_war_with = ITA
  any_state = {
    is_controlled_by = ITA
  }
}
```
- `has_war_with` がfalseなら、それ以降の判定を行わず中断する → 高速化

### 対策3: キャッシュの利用

#### 状態変更時のみ判定を有効にする例
```hoi4
on_actions = {
  on_state_control_changed = {
    set_country_flag = {
      flag = should_check_decision
      days = 1
      value = 1
    }
  }
}

trigger = {
  has_war_with = ITA
  has_country_flag = should_check_decision
  any_state = {
    is_controlled_by = ITA
  }
}
```
- 州支配が変わったときのみ判定を行うようにフラグを設定
- 判定回数を大幅に削減し、高速化可能

---

## まとめ

- `imgui show profiler` を使って処理の重さを視覚的に把握する
- `hourly` 処理の削減が鍵
- 判定順序の工夫（早期リターン）とキャッシュによる最適化が有効
- 特に `any_state` の使用には注意し、必要に応じて他の手段に置き換える

効率的なMOD開発のために、これらの軽量化手法をぜひ活用してください。
