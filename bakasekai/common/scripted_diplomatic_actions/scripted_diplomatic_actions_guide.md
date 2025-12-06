# Scripted Diplomatic Actions Guide

Hearts of Iron IVの `common/scripted_diplomatic_actions` で定義される外交アクションの構造と作成方法についての解説です。

## 基本構造

ファイルパス: `common/scripted_diplomatic_actions/YOUR_FILE_NAME.txt`

外交アクションは、最上位レベルでユニークなID（アクション名）を持ち、そのブロック内にプロパティを記述します。
**注意:** `scripted_diplomatic_actions = { ... }` というラッパーが必要です。

```pdx
scripted_diplomatic_actions={
    action_unique_id = {
        name = "LOC_KEY_NAME"          # アクション名のローカライゼーションキー
        icon = "GFX_icon_name"         # 表示されるアイコン

        # このアクションがリストに表示される条件
        visible = {
            NOT = { has_war_with = FROM }
        }

        # このアクションが実行可能（クリック可能）になる条件
        allowed = {
            # 必要な条件を記述
            # カスタムツールチップを使って条件を説明することが推奨されます
            custom_trigger_tooltip = {
                tooltip = "LOC_KEY_Req_Tooltip"
                check_variable = { ROOT.political_power > 10 }
            }
        }

        # 実行コスト（主に政治力）
        cost = 25
        
        # コストの表示用テキスト（必須ではないが、カスタムコストの場合などに使用）
        cost_string = "LOC_KEY_COST_STRING"

        # アクション実行時の効果
        complete_effect = {
            # sender (ROOT) と receiver (FROM) のスコープで効果を記述
            FROM = {
                country_event = { id = my_event.1 }
            }
        }

        # AIがこのアクションを実行する頻度・確率
        ai_desire = {
            base = 0 # デフォルトでは実行しない
            
            modifier = {
                factor = 10
                # AIが実行したくなる条件
            }
        }
    }
}
```

## キーワード解説

| キーワード | 説明 | 注記 |
| :--- | :--- | :--- |
| `name` | 外交画面に表示される名前のLocキー | |
| `icon` | アイコンのGFX参照名 | `interface/*.gfx` で定義されている必要があります |
| `visible` | 外交アクション一覧に表示されるかどうかのトリガー | 満たさない場合はリストに表示されません |
| `allowed` | アクションボタンが有効化されるかどうかのトリガー | `visible` は満たすが `allowed` を満たさない場合、グレーアウトして表示されます |
| `cost` | 実行に必要なコスト | 通常は `political_power` です |
| `complete_effect` | アクション完了時に実行される効果 | 即時効果を書きます |
| `ai_desire` | AIの実行意欲 | 高いほど実行されやすくなります。`base` や `modifier` で調整します |

## ローカライゼーション

`localisation/japanese/YOUR_LOC_l_japanese.yml` などに記述します。

```yaml
l_japanese:
 ACTION_ID_NAME:0 "アクション名"
 ACTION_ID_DESC:0 "アクションの説明文（外交画面で選択時に表示）"
 ACTION_ID_IS_VALID:0 "実行条件の説明"
```
