import json
import subprocess
import sys
import unittest
from pathlib import Path

from engine import evaluate


def example():
    return json.loads(Path(__file__).with_name("example.json").read_text(encoding="utf-8"))


class AcceptanceTests(unittest.TestCase):
    def test_example_cli(self):
        proc = subprocess.run([sys.executable, "cli.py", "example.json"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), evaluate(example()))

    def test_partial_and_complete_snapshots(self):
        data = example()
        partial = evaluate(data)
        self.assertEqual(partial["delete"], [])
        self.assertEqual(partial["upsert"], {"a": {"price": 5}})
        self.assertEqual(partial["missing_pages"], [2])
        data["pages"].append({"number": 2, "rows": {"c": {"price": 1}}})
        self.assertEqual(evaluate(data)["delete"], ["b"])
        data["max_delete_fraction"] = 0.3
        self.assertEqual(evaluate(data)["reason"], "deletion_limit")

    def test_cross_page_duplicate_invalidates_batch(self):
        data = example()
        data["pages"].append({"number": 2, "rows": {"a": {}}})
        with self.assertRaisesRegex(ValueError, "repeated SKU"):
            evaluate(data)
