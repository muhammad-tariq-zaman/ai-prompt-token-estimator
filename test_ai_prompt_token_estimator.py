import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import estimate, estimate_all

PROMPTS = [
    {"id": "summarise-ticket", "text": "Summarise this support ticket in two sentences."},
    {"id": "draft-reply", "text": "Draft a polite reply to a customer whose laptop will not connect to Wi-Fi."},
    {"id": "explain-dns", "text": "Explain DNS in simple words for a new starter."},
]

class TestTokenEstimator(unittest.TestCase):
    def test_token_estimate(self):
        chars, words, tokens = estimate("Summarise this support ticket in two sentences.")
        self.assertEqual((chars, words, tokens), (47, 7, 12))

    def test_four_chars_is_one_token(self):
        self.assertEqual(estimate("abcd")[2], 1)

    def test_five_chars_is_two_tokens(self):
        self.assertEqual(estimate("abcde")[2], 2)

    def test_empty_text(self):
        self.assertEqual(estimate(""), (0, 0, 0))

    def test_word_count(self):
        self.assertEqual(estimate("one two three")[1], 3)

    def test_cost_calculation(self):
        results = estimate_all(PROMPTS, price_per_1k=0.002)
        self.assertEqual([r[3] for r in results], [12, 19, 12])
        self.assertAlmostEqual(sum(r[4] for r in results), 0.000086, places=6)

    def test_total_tokens(self):
        results = estimate_all(PROMPTS)
        self.assertEqual(sum(r[3] for r in results), 43)

    def test_custom_price(self):
        results = estimate_all([{"id": "p1", "text": "abcd"}], price_per_1k=1.0)
        self.assertAlmostEqual(results[0][4], 0.001)

    def test_empty_prompts(self):
        self.assertEqual(estimate_all([]), [])
