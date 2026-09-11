# Day 2 model comparison

Generated from `docs/day2-run.jsonl`. `cost_usd` is 0.0 for both configured models; this is not a dollar-cost race and no cost winner is named.

## mistral (`mistral:7b`)

- Attempts: 12
- Successes: 12
- Truncations: 0
- Other errors: 0
- Input tokens: sum=2775, mean=231.25
- Output tokens: sum=1318, mean=109.83
- Latency (ms): mean=4508.58, max=9881
- cost_usd: 0.0

## qwen (`qwen3:8b`)

- Attempts: 12
- Successes: 0
- Truncations: 12
- Other errors: 0
- Input tokens: sum=2427, mean=202.25
- Output tokens: sum=3072, mean=256.00
- Latency (ms): mean=11121.58, max=14320
- cost_usd: 0.0
