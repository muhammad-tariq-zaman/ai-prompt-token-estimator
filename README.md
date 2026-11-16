# ai-prompt-token-estimator

Estimate token counts and cost for a list of AI prompts: prompts.json is a JSON list of objects with id and text — tokens use the common rule of thumb that one token is about 4 characters of English text (tokens = ceil(chars / 4)), cost = tokens / 1000 × --price-per-1k (default $0.002). These are estimates only; use the provider's own tokenizer for exact counts before budgeting a real run.

Sample input is included (sample.json with three prompts).

## How to run

```sh
python3 main.py sample.json
```

## Example output

```
summarise-ticket: 47 chars, 7 words, ~12 tokens, ~$0.000024
draft-reply: 74 chars, 14 words, ~19 tokens, ~$0.000038
explain-dns: 46 chars, 9 words, ~12 tokens, ~$0.000024
Total: 3 prompt(s), ~43 tokens, ~$0.000086 at $0.002/1k tokens.
Note: token counts are estimates (1 token ≈ 4 characters); use the provider's tokenizer for exact counts.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
