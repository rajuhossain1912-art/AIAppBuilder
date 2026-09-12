import unittest

from agent.quality import PerformancePolicy


class PerformancePolicyTests(unittest.TestCase):
    def test_normal_source_passes(self):
        PerformancePolicy().require_clean(
            'Button button = new Button(this);\nsetContentView(root);\n'
        )

    def test_blocking_sleep_fails(self):
        findings = PerformancePolicy().validate_source('Thread.sleep(5000);')
        self.assertTrue(findings)

    def test_infinite_loop_fails(self):
        findings = PerformancePolicy().validate_source('while (true) { doWork(); }')
        self.assertTrue(findings)

    def test_repeated_content_reset_is_flagged(self):
        findings = PerformancePolicy().validate_source(
            'setContentView(a);\nsetContentView(b);\n'
        )
        self.assertTrue(findings)


if __name__ == '__main__':
    unittest.main()
