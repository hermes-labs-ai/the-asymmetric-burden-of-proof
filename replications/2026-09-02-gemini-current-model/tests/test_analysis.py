import json
import unittest

from src.analyze import parse, percentile


class AnalysisTests(unittest.TestCase):
    def test_valid_response(self):
        obj = {"classification": "Likely", "probability_distribution": {"effect_greater_than_zero": 20, "effect_approximately_zero": 70, "effect_less_than_zero": 10}, "top_3_reasons": ["a", "b", "c"]}
        parsed, error = parse(json.dumps(obj))
        self.assertIsNone(error)
        self.assertEqual(parsed, obj)

    def test_rejects_bad_sum(self):
        text = '{"classification":"Likely","probability_distribution":{"effect_greater_than_zero":20,"effect_approximately_zero":70,"effect_less_than_zero":20},"top_3_reasons":["a","b","c"]}'
        self.assertIn("sum", parse(text)[1])

    def test_percentile(self):
        self.assertEqual(percentile([0, 10, 20], .5), 10)

if __name__ == "__main__":
    unittest.main()
