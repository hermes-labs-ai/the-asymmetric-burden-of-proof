import json
import unittest

from src.analyze import EXPECTED_PAIR_LABELS, analyze_model, parse, percentile
from src.validate_run import EXPECTED_MODELS, expected_keys


class AnalysisTests(unittest.TestCase):
    def test_valid_response(self):
        obj = {"classification": "Likely", "probability_distribution": {"effect_greater_than_zero": 20, "effect_approximately_zero": 70, "effect_less_than_zero": 10}, "top_3_reasons": ["a", "b", "c"]}
        parsed, error = parse(json.dumps(obj))
        self.assertIsNone(error)
        self.assertEqual(parsed, obj)

    def test_rejects_bad_sum(self):
        text = '{"classification":"Likely","probability_distribution":{"effect_greater_than_zero":20,"effect_approximately_zero":70,"effect_less_than_zero":20},"top_3_reasons":["a","b","c"]}'
        self.assertIn("sum", parse(text)[1])

    def test_rejects_non_object_json_without_crashing(self):
        for text in ("[]", "null", '"text"', "1"):
            with self.subTest(text=text):
                parsed, error = parse(text)
                self.assertIsNone(parsed)
                self.assertEqual(error, "response must be a JSON object")

    def test_percentile(self):
        self.assertEqual(percentile([0, 10, 20], .5), 10)

    def test_analysis_rejects_missing_preregistered_pair(self):
        text = json.dumps({"classification": "Likely", "probability_distribution": {"effect_greater_than_zero": 60, "effect_approximately_zero": 30, "effect_less_than_zero": 10}, "top_3_reasons": ["a", "b", "c"]})
        rows = [
            {"pair_label": pair, "condition": condition, "run_number": 1, "status": "ok", "returned_model": "gemini-3.1-flash-lite", "output_text": text, "usage": {}}
            for pair in sorted(EXPECTED_PAIR_LABELS)[:-1]
            for condition in ("A", "B")
        ]
        with self.assertRaisesRegex(ValueError, "exactly the four"):
            analyze_model("gemini-3.1-flash-lite", rows)

    def test_analysis_rejects_pair_without_complete_unit(self):
        valid = json.dumps({"classification": "Likely", "probability_distribution": {"effect_greater_than_zero": 60, "effect_approximately_zero": 30, "effect_less_than_zero": 10}, "top_3_reasons": ["a", "b", "c"]})
        incomplete_pair = sorted(EXPECTED_PAIR_LABELS)[-1]
        rows = [
            {"pair_label": pair, "condition": condition, "run_number": 1, "status": "ok", "returned_model": "gemini-3.1-flash-lite", "output_text": "[]" if pair == incomplete_pair and condition == "B" else valid, "usage": {}}
            for pair in sorted(EXPECTED_PAIR_LABELS)
            for condition in ("A", "B")
        ]
        with self.assertRaisesRegex(ValueError, "every preregistered pair"):
            analyze_model("gemini-3.1-flash-lite", rows)

    def test_expected_keys_rejects_count_preserving_matrix_substitution(self):
        prompts = {"pairs": [{"label": pair} for pair in EXPECTED_PAIR_LABELS]}
        expected = expected_keys(prompts)
        self.assertEqual(len(expected), 80)
        manipulated = set(expected)
        manipulated.remove(next(iter(manipulated)))
        manipulated.add((next(iter(EXPECTED_MODELS)), next(iter(EXPECTED_PAIR_LABELS)), "A", 6))
        self.assertEqual(len(manipulated), 80)
        self.assertNotEqual(manipulated, expected)

if __name__ == "__main__":
    unittest.main()
