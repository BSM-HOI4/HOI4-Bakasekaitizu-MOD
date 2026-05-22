# Repository Guidelines (HOI4-Bakasekaitizu-MOD)

## 目的 / Purpose
- 本ファイルはエージェント向けの作業指針です。
- HOI4 1.13.* 向けの総変換MOD開発を前提とします。
- 既存の `CLAUDE.md` と `.github/copilot-instructions.md` を統合・整理しています。

## リポジトリ構成
- `bakasekai/`: 主要コンテンツ（HOI4標準構造）
  - `common/`, `events/`, `history/`, `localisation/japanese/`, `gfx/`, `interface/`, `map/`
- `documents/00_coding_contexts/`: 効果・トリガー・スクリプト概念の参照資料
- `flags/00-03/`: 国旗アセットの分割保管
- `tests/`: 検証用シナリオ/デバッグ用コンテンツ

## 重要ドキュメント
- `CLAUDE.md`: AI向け全体ガイド
- `.github/copilot-instructions.md`: コーディング規約と構造
- `.github/CONTRIBUTING.md`: 開発/検証フロー
- `documents/onboarding_guide.md`: 新規参加者向け案内
- `documents/00_coding_contexts/*`: 効果/トリガー/変数の辞書

## ビルド/実行（実質の開発フロー）
- HOI4ランチャーでMODを有効化しプレイテストします。
- 依存MOD: Japanese Language mod
- バージョン: HOI4 1.13.*

## テスト/検証（単体テスト相当）
- 自動テスト/CI/リンタは基本的に存在しません。
- 単一テストは以下の手順で実施します。
  - `tests/` に検証シナリオを置く
  - コンソールで `event <event_id> <TAG>` を実行
  - 必要に応じて `reload interface` / `reload localisation`
- テスト用コンテンツは `_bsm_*_test.*` など明確に分離する
- 変更後は対象の国家/イベント/GUIに限定した最小検証を行う

## デバッグ/検証コマンド
- `tdebug`: デバッグ情報表示
- `event <event_id> <TAG>`: イベント実行
- `reload interface`: GUI反映
- `reload localisation`: ローカライズ反映（慎重に）
- `imgui show profiler`: Scriptタブで `hourly` の負荷を確認

## ファイル配置の原則
- 既存フォルダ構成を崩さない
- 新規ファイルは同系統の既存ファイルと並べる
- 既存のファイル名・IDプレフィックスに合わせる
- 目的別に小さく分割し、巨大ファイルを避ける

## コーディング規約（共通）
- インデントはスペース2個、タブ禁止
- 1行1命令（Paradox scriptの可読性維持）
- コメントは必要最低限、内容は日本語可
- 既存の並び順や構造を崩さない

## 命名規則
- 国別ファイル: 3文字タグ（例 `JPN.txt`, `USA.txt`）
- システム系: `_bsm_` 接頭辞（例 `_bsm_mine_system.txt`）
- 汎用: `generic.txt` 等のわかる名前
- GUI/Scripted: `_bsm_` + 機能名で統一
- 国旗: `flags/00-03/` で命名規則に合わせる

## イデオロギーキー（重要）
- 既存の置換キーを必ず使う
  - `communism_ideology`
  - `democratic_ideology`
  - `fascism_ideology`
  - `neutrality_ideology`

## ローカライズ規約
- 配置: `bakasekai/localisation/japanese/*.yml`
- `l_japanese:` ヘッダー必須
- エンコードは UTF-8 with BOM
- 変数表示は `[?variable_name]` を使用
- 追加キーは既存キーとの整合性を最優先
- Scripted localisation は既存の書式に合わせる
- キー名は機能・国・システム名で一意にする

## スクリプトの書式/構造
- 条件ブロックは軽い条件から先に記述
- `limit` や `trigger` のネストは最小限に保つ
- `any_state` など重いスコープは高頻度処理で避ける
- 同一効果の繰り返しはスクリプト化を検討

## 参照・再利用（imports相当）
- 既存の `scripted_effect` / `scripted_trigger` を優先再利用
- 共有処理は `_bsm_` 接頭辞で命名し再利用性を高める
- ローカライズは `scripted_localisation` を活用し重複を避ける
- 既存のキーやIDを上書きしない

## 変数・型（HOI4スクリプト）
- 変数は `set_variable`, `add_to_variable` 等の標準式で統一
- 比較は `check_variable` を使う
- 変数名は用途が明確な英語スネークケースで揃える
- スコープは明示し、`root/from` の取り違えを避ける

## エラー/検証の基本姿勢
- 仕様が曖昧な場合は既存実装に合わせる
- 変更後は必ず最小検証（イベント/国/GUI限定）
- ローカライズ欠落が起きるため追加キーは必ず確認
- 不具合があれば `tests/` の検証シナリオで再現性を確保
- テスト用変更は必ずクリーンアップ可能にする

## パフォーマンス指針
- 早期returnで軽い条件を先に書く
- 頻繁なスコープで `any_state` を避ける
- 高頻度処理はフラグ/変数でキャッシュ
- ミッション決定は重いので代替も検討

## イベント/国家方針/決定の作法
- IDは既存のプレフィックスに揃える
- トリガー・効果・説明は最小限で明確に
- オプションの結果はローカライズとセットで確認
- 検証用の決定やイベントは `_bsm_*_test` に分離

## GUI作業（参考）
- GUI作業は段階的に実装し、都度 `reload interface`
- 追加するGUIは `_bsm_` 系の命名を徹底
- Scripted GUIやlocalisation連携は既存実装に合わせる
- 画像差し替え時は最適化と命名統一を維持

## アセット規約
- `.wav` / `.ogg` は絶対に変更しない
- 画像は最適化を意識、命名は既存に合わせる
- 国旗は `flags/00-03/` の規則に従う

## 変更時のチェックリスト
- 影響範囲が `bakasekai/` 内に収まっているか
- ローカライズの追加/更新があるか
- 既存の命名規則を逸脱していないか
- パフォーマンスに悪影響がないか

## コミット/PRの方針
- コミットは命令形 + スコープ（例 `focus: Add ...`）
- PRには次を含める
  - 変更内容の要約
  - 影響パス
  - UI変更はスクショ
  - 追加/変更ローカライズキー
  - セーブ互換性
  - パフォーマンス観測

## 外部ツール/ルール
- Cursor ルール: 未検出（`.cursor/rules/`, `.cursorrules` なし）
- Copilot ルール: `.github/copilot-instructions.md` を参照

## 参照パス（頻出）
- `documents/00_coding_contexts/01_effects/effects.json`
- `documents/00_coding_contexts/04_triggers/triggers.json`
- `documents/00_coding_contexts/00_mod_optimization.md`
- `documents/00_coding_contexts/console_commands_documentation.md`

## 注意事項
- Workshop ID `2585391890` は公開フローのみで使用
- 既存の世界観/設定を尊重し、独自解釈は最小限
- 不明点は既存ファイルを優先して調査
