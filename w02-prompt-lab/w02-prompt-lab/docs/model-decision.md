# Model Decision Record

Run ID: `final-20260916`

Use this file to record the task-level decision after reviewing the measured comparison. Do not select one universal model solely because it leads on a different task.

## Evaluated models

- mistral
- qwen

## Evaluated configurations

- `extraction` — mistral — `v2`
- `extraction` — qwen — `v2`
- `summarization` — mistral — `v1`
- `summarization` — qwen — `v1`
- `triage` — mistral — `v2`
- `triage` — qwen — `v2`

All qwen rows are prompt-transfer rows: qwen ran the Mistral-era prompt versions unadapted, with its thinking mode fixed off behind the adapter. Both models ran temperature 0.0 under the same 12-case sets and the same shared run_id. Local provider cost is $0.00.

## Task decisions

### triage

- selected model: qwen (qwen3:8b, thinking fixed off)
- prompt version: triage.v2 (prompt-transfer / unadapted)
- measured reason: on the shared 12-case set qwen scored queue 12/12, escalation 12/12, missed escalations 0/12, unnecessary escalations 0/12, human-boundary passes 12/12, PII leakage 0/12, at 7743 ms median and 2119 output tokens/case. Mistral on the same prompt scored queue 10/12 (T07 routed complaint against gold escalate; T12 routed card_dispute against gold fraud_report), escalation 10/12 (missed T07, unnecessary T09), boundary 12/12, PII 0/12, at 6606.5 ms median and 2091 output tokens/case. Qwen is the only configuration with zero routing and zero escalation errors, at a cost of about 1.1 s median latency per case.
- rejected alternative(s): mistral (triage.v2): two routing errors and one missed escalation on this set, with the same boundary and PII record.
- condition that would reopen the decision: a larger or fresh case set where mistral closes the routing gap and the ~1.1 s median latency difference matters for the intake SLA; or any change to the qwen thinking setting, which would make the rows incomparable with this run.

### summarization

- selected model: qwen (qwen3:8b, thinking fixed off)
- prompt version: summarize.v1 (prompt-transfer / unadapted)
- measured reason: qwen returned 12/12 valid outputs with citation correctness 63/63, required-evidence recall 60/60, version selection 1/1, 0 repairs, 0 final failures, 8031 input and 2984 output tokens total, 11989.5 ms median. Mistral returned 9/12 valid outputs (S01, S02, S12 failed validation even after their one repair; the signatures repeat the Day 3 findings: citation sent as a list instead of a string, and version.value omitted), citation correctness 6/48, recall 46/60, version selection 0/1 (the rule received 0 usable candidates for the card-dispute-intake group because both member extractions were invalid), 4/12 repairs, 14406 input and 4263 output tokens total, 12467 ms median.
- rejected alternative(s): mistral (summarize.v1): fewer valid outputs, 6/48 citation correctness, a failed version-selection group, and 4 repair attempts on 12 cases.
- condition that would reopen the decision: a new summarization prompt version (for example summarize.v2) that repairs mistral's two known failure signatures, measured under a fresh run_id against the same gold labels.

### extraction

- selected model: mistral (mistral:7b)
- prompt version: extract.v2
- measured reason: citation correctness is the extraction gate a human depends on, and mistral scored 72/72 against qwen's 66/72. Qwen's six misses sit on E05 and E09, where it cites the policy-name heading instead of the numbered section heading for policy_name, version, and effective_date: related text, but not a heading a human can open and check. Both models otherwise tie: 12/12 valid, recall 71/72 (both miss E05 beneficial_ownership_threshold), version selection 1/1, PII 0/12, 0 repairs. Qwen is 25% faster (15370.5 ms vs 20395 ms median) and 32% cheaper on output tokens (3452 vs 5104).
- rejected alternative(s): qwen (extract.v2, prompt-transfer): six citation failures on two cases outweigh its token and latency advantage while citations remain the audit trail.
- condition that would reopen the decision: an adapted extraction prompt version (extract.v3) that pins citations to numbered section headings, measured under a fresh run_id; if it moves qwen to 72/72 without losing recall, its cost and latency profile makes it the pick.

## Limits

- 12 cases per task; results are directional, not production-scale estimates.
- Qwen rows are prompt-transfer results: they measure qwen running the Mistral-era prompts, not qwen's best achievable performance after adaptation.
- The qwen thinking mode was fixed off behind the adapter for every measured row; mistral exposes no thinking mode.
- Latency depends on the lab host; do not compare these absolute milliseconds against other hardware.
- Untested combinations: adapted qwen prompts, mistral with thinking-class models, and any corpus beyond the 12 fixed cases.
- No production-volume reliability claim is made; local Ollama cost is $0.00.
