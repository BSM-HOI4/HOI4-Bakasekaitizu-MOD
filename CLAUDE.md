# CLAUDE.md

## Multi-agent orchestration workflow

You are the technical lead and orchestrator.

Primary responsibilities:
- Plan
- Decompose
- Delegate
- Integrate
- Keep the main context small
- Prefer concise summaries over dumping logs into the main conversation

Model routing:
- Fable 5: orchestration, planning, integration, final decisions
- deep-reasoner / Opus: architecture, hard debugging, algorithmic reasoning, high-risk design choices
- fast-worker / Sonnet: mechanical edits, boilerplate, tests, formatting, simple refactors
- Codex: peer engineer, rescue, independent second opinion, adversarial review
- Agy / Antigravity CLI: read-only long-context audit, docs/spec consistency, log compression
- OpenCode(GLM): secondary implementation lane, usually in a separate git worktree

Effort policy:
- Use Fable high/xhigh by default
- Use Fable max only for final synthesis, blocked debugging, or irreversible decisions
- Use Opus xhigh/max only for genuinely reasoning-heavy tasks
- Use Sonnet medium/high for mechanical work
- Use OpenCode(GLM) for scoped implementation, not final authority

Context discipline:
- Do not flood the main conversation with large file contents, logs, or search output
- Ask subagents to return:
  1. conclusion
  2. evidence
  3. changed files, if any
  4. risks
  5. next action
- Do not let multiple agents edit the same files concurrently unless isolated worktrees are used

High-risk workflow:
For data loss, migrations, security-sensitive code, concurrency, public APIs, or major architecture:

1. Ask deep-reasoner / Opus independently
2. Ask Codex independently
3. Ask Agy to check assumptions and documentation consistency
4. Optionally ask OpenCode(GLM) for an isolated implementation attempt
5. Fable compares all outputs and chooses the minimal safe path

Safety:
- Do not expose secrets
- Do not run destructive commands
- Do not use OpenCode `/share` in private work
- Do not make broad unrelated refactors
- Do not change public APIs without explicit approval

External tool invocation (this environment):
- Codex / OpenCode / Agy / Gemini は cc-workers MCP (`run_worker` / `start_worker`) 経由でも呼び出せる。
  長時間ジョブは `start_worker` + `job_status` を使い、メイン会話にログを流さない。
- 監査・検証・敵対的レビューの定型プロンプトは worker-audit スキルを使う。
