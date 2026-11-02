# 英国41国家方針 — SWE2実装引継ぎ

ユーザー指定：実装担当はSWE2。descはagy経由のGeminiで生成する。

- 仕様：`../../GBR_britain_three_sovereignties_focus_proposal.md`
- 41項目のID・名称・仕様：`focus_contract.json`
- 担当範囲と検証条件：`implementation_handoff.md`
- 既存シナリオの保全用ハッシュ：`preservation_baseline.json`
- 生成・実装経路の実測状況：`provenance.json`

現在はSWE2の実行コマンド／アプリ内の実行場所をユーザーへ確認中。利用可能なCLIとモデル一覧では実行先を特定できていない。実装を別モデルへ置き換えず、ゲーム用スクリプトは変更していない。

Geminiの国家方針desc 41件を `focus_desc_gemini.json` と `GBR_focus_desc_gemini_l_japanese.yml` に保存済み。JSON構造・41キー対応・キー一意性・BOMを検証済み。原出力とキー別モデル出典はrawファイル／provenanceに保存した。ゲーム側のlocalisationへはまだ配置していない。新設イベント・国民精神・決定のdescも、SWE2の出力する仕様からGeminiへ別途依頼する必要がある。国家方針のdescだけで全descを生成済みと扱わない。
