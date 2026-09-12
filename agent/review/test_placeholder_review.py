import tempfile
import unittest
from pathlib import Path

from agent.review import ReviewEngine, ReviewStatus


class PlaceholderReviewTests(unittest.TestCase):
    def test_placeholder_is_release_blocking(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "MainActivity.java"
            source.write_text(
                "TextView status = label(\"Project shell ready.\");\n",
                encoding="utf-8",
            )
            report = ReviewEngine().review_paths("demo", root, ["MainActivity.java"])
            self.assertTrue(report.blocking)
            self.assertEqual(report.blocking[0].category, "FUNCTIONALITY")
            self.assertEqual(report.blocking[0].status, ReviewStatus.PARTIALLY_IMPLEMENTED)


if __name__ == "__main__":
    unittest.main()
