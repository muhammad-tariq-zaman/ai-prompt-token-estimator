"""Estimate token counts and cost for a list of AI prompts.

Usage: python3 main.py prompts.json [--price-per-1k 0.002]
prompts.json is a JSON list of objects with id and text.
Token estimate uses the common rule of thumb that one token
is about 4 characters of English text: tokens = ceil(chars / 4).
Cost = tokens / 1000 * price-per-1k. These are estimates only;
use the provider's own tokenizer for exact counts before
budgeting a real run.
"""
import argparse, json, math, sys

def estimate(text):
    chars = len(text)
    words = len(text.split())
    tokens = math.ceil(chars / 4) if chars else 0
    return chars, words, tokens

def estimate_all(prompts, price_per_1k=0.002):
    out = []
    for prompt in prompts:
        chars, words, tokens = estimate(prompt["text"])
        cost = tokens / 1000 * price_per_1k
        out.append((prompt["id"], chars, words, tokens, cost))
    return out

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--price-per-1k", type=float, default=0.002)
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        prompts = json.load(f)
    results = estimate_all(prompts, args.price_per_1k)
    for prompt_id, chars, words, tokens, cost in results:
        print(f"{prompt_id}: {chars} chars, {words} words, "
              f"~{tokens} tokens, ~${cost:.6f}")
    total_tokens = sum(r[3] for r in results)
    total_cost = sum(r[4] for r in results)
    print(f"Total: {len(results)} prompt(s), ~{total_tokens} tokens, "
          f"~${total_cost:.6f} at ${args.price_per_1k}/1k tokens.")
    print("Note: token counts are estimates (1 token ≈ 4 characters); "
          "use the provider's tokenizer for exact counts.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
