# Model Comparison

Run ID: `final-20260916`

Counts are reported with their denominators. Latency uses median and maximum rather than mean.

## Extraction

| Model | Prompt | Valid outputs | Metrics | Input tokens | Output tokens | Median latency | Max latency | n | Repairs | Retries | Final failures |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mistral | v2 | 12/12 | citation_correctness: 72/72<br>pii_leakage: 0/12 ↓<br>required_evidence_recall: 71/72<br>version_selection: 1/1 | 24503 | 5104 | 20395 ms | 22435 ms | 12 | 0/12 | 0 | 0 |
| qwen | v2 | 12/12 | citation_correctness: 66/72<br>pii_leakage: 0/12 ↓<br>required_evidence_recall: 71/72<br>version_selection: 1/1 | 20447 | 3452 | 15370.5 ms | 18509 ms | 12 | 0/12 | 0 | 0 |

## Summarization

| Model | Prompt | Valid outputs | Metrics | Input tokens | Output tokens | Median latency | Max latency | n | Repairs | Retries | Final failures |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mistral | v1 | 9/12 | citation_correctness: 6/48<br>pii_leakage: 0/12 ↓<br>required_evidence_recall: 46/60<br>version_selection: 0/1 | 14406 | 4263 | 12467 ms | 13547 ms | 16 | 4/12 | 0 | 3 |
| qwen | v1 | 12/12 | citation_correctness: 63/63<br>pii_leakage: 0/12 ↓<br>required_evidence_recall: 60/60<br>version_selection: 1/1 | 8031 | 2984 | 11989.5 ms | 14864 ms | 12 | 0/12 | 0 | 0 |

## Triage

| Model | Prompt | Valid outputs | Metrics | Input tokens | Output tokens | Median latency | Max latency | n | Repairs | Retries | Final failures |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mistral | v2 | 12/12 | escalation: 10/12<br>human_boundary: 12/12<br>missed_escalation: 1/12 ↓<br>pii_leakage: 0/12 ↓<br>queue: 10/12<br>unnecessary_escalation: 1/12 ↓ | 10846 | 2091 | 6606.5 ms | 9876 ms | 12 | 0/12 | 0 | 0 |
| qwen | v2 | 12/12 | escalation: 12/12<br>human_boundary: 12/12<br>missed_escalation: 0/12 ↓<br>pii_leakage: 0/12 ↓<br>queue: 12/12<br>unnecessary_escalation: 0/12 ↓ | 9667 | 2119 | 7743 ms | 11227 ms | 12 | 0/12 | 0 | 0 |

## Limits

- The Week 2 comparison uses a small fixed case set; report counts rather than treating one-case differences as precise production estimates.
- A row measures the model together with the prompt version shown in that row.
- A transferred prompt is evidence about that transferred configuration, not proof of the model's best achievable performance after adaptation.
- Local Ollama provider/API charge is `$0.00`; token usage and latency still represent real operational work.
- Fixed reasoning setting behind the adapter: qwen (qwen3:8b) thinking off.
