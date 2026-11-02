# SWE2 implementation handoff

User explicitly requests implementation by SWE2 and ALL desc text through agy/Gemini.
Repository: /Users/eightman/dev/hoi4/HOI4-Bakasekaitizu-MOD
Branch: feature/london_three_sovereignties (dirty shared checkout).
Specification: documents/GBR_britain_three_sovereignties_focus_proposal.md
Fixed focus contract: documents/implementation/GBR_swe2/focus_contract.json (41 IDs).

Implement all 41 focuses (5 common / 16 politics / 6 economy / 8 military / 6 diplomacy), not only the first phase. Politics has four exclusive policy roots. Construction, naval and diplomacy branches continue when LON rejects cooperation. Actual reciprocal diplomatic events must request consent; policy completion cannot auto-accept a treaty, annex foreign territory or roll back an existing LON outcome.

You are not alone in this checkout. Preserve all existing FRA/ESP/NSI/Win95/LON changes. Scope new files to GBR_* (national_focus/britain.txt, events, decisions/categories, scripted effects/triggers, ideas, Japanese localisation and scoped validator). Modify existing LON handlers only when an integration requires it, preserving namespaces, flags and legacy outcomes. Do not edit WAV/OGG/map/CSV/binary/real saves. No commit/push/deploy.

Read applicable AGENTS.md and required HOI4 implementation skills; use dictionary-supported scopes. Scripts use two spaces, one command per line. Country is GBR, not ENG. Japan localisation BOM/l_japanese; preserve original identifiers. set_capital = { state = ... } is required by the current game (scalar syntax is rejected). Territorial effects must recheck current ownership AND control, peace and individual consent when choices execute; consume pending/consent flags on refusal too.

Use the 41 fixed IDs exactly. Focus names are the approved Japanese names in the contract. Gemini-authored focus desc will be supplied separately as JSON mapping ID_desc to text, then converted mechanically to YML. You must not author any final desc yourself. For newly added event/idea/decision desc, emit a machine-readable manifest of key, title and actual effects so the parent can obtain them from agy/Gemini. Keep source/provenance explicit; no final TODO/placeholder text.

Validate unique references, event reachability, mutually exclusive roots, lack of deadlocks, foreign-state safety, callbacks after death/war, Japanese key uniqueness/BOM and all 41 focus geometry. Extend actual script-reading models similar to tools/verify_london_scenario.py rather than tests that merely repeat expected constants. Report PASS/FAIL/SKIP separately; static/model tests are not runtime campaign evidence. No all-repo cleanup.

Gemini focus descriptions are now ready in focus_desc_gemini.json and GBR_focus_desc_gemini_l_japanese.yml in this handoff directory. Preserve the 41 generated values; install mechanically after implementing the matching focus IDs. Every NEW event/idea/decision desc still needs a Gemini generation pass from your actual implementation manifest.
