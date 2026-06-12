# BSM Stellaris Tradition GUI Assets

## 目的

伝統GUIを、単なる進行ボタン列ではなく、Stellaris本家の伝統カテゴリ画面に近い「カード内ツリー」形式へ寄せるためのグラフィック管理メモ。

## 作成済み

配置先: `bakasekai/gfx/interface/GUI/bsm_stellaris/`

| ファイル | 用途 | `.gfx` スプライト |
| --- | --- | --- |
| `tradition_card.png` | 伝統カテゴリカード背景 | `GFX_bsm_stellaris_tradition_card` |
| `tradition_connector.png` | ノード間の横発光接続線 | `GFX_bsm_stellaris_tradition_connector` |
| `tradition_connector_v.png` | ノード間の縦発光接続線 | `GFX_bsm_stellaris_tradition_connector_v` |
| `tradition_node_adopt.png` | 採用ノード | `GFX_bsm_stellaris_tradition_node_adopt` |
| `tradition_node.png` | 通常伝統ノード | `GFX_bsm_stellaris_tradition_node` |
| `tradition_node_finish.png` | 完成ノード | `GFX_bsm_stellaris_tradition_node_finish` |
| `tradition_node_done.png` | 取得済みノードの点灯オーバーレイ | `GFX_bsm_stellaris_tradition_node_done` |
| `tradition_icon_exploration.png` | 探索カテゴリ見出しアイコン | `GFX_bsm_stellaris_tradition_icon_exploration` |
| `tradition_icon_expansion.png` | 拡張カテゴリ見出しアイコン | `GFX_bsm_stellaris_tradition_icon_expansion` |
| `tradition_icon_prosperity.png` | 繁栄カテゴリ見出しアイコン | `GFX_bsm_stellaris_tradition_icon_prosperity` |
| `tradition_icon_armaments.png` | 軍備カテゴリ見出しアイコン | `GFX_bsm_stellaris_tradition_icon_armaments` |
| `tradition_icon_diplomacy.png` | 外交カテゴリ見出しアイコン | `GFX_bsm_stellaris_tradition_icon_diplomacy` |
| `tradition_icon_governance.png` | 統治カテゴリ見出しアイコン | `GFX_bsm_stellaris_tradition_icon_governance` |
| `tradition_icon_harmony.png` | 調和カテゴリ見出しアイコン | `GFX_bsm_stellaris_tradition_icon_harmony` |

定義ファイル: `bakasekai/interface/bsm_stellaris.gfx`

## 追加で作る価値があるもの

必須ではないが、さらに本家Stellaris風に寄せるなら以下を作成する。

| 優先度 | グラフィック | 用途 |
| --- | --- | --- |
| 中 | ロック済みノード用スプライト | 未来段階を暗色で表示し、クリック不可状態を視覚的に分ける |
| 中 | 接続線の取得済み/未取得バリエーション | ツリーの進捗を線の点灯で見せる |
| 低 | アセンションパーク用大型スロット | 右側パーク欄もStellarisのスロットUIへ寄せる |
| 低 | 特性欄の小アイコン | 特性一覧の可読性を上げる |

## 注意

Stellaris本家ファイルからの直接コピーは避ける。必要な場合も、配布権限やMOD利用条件を確認してから判断する。現状の素材はローカル生成のオリジナルUI部品。
