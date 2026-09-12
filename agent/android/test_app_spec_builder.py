from __future__ import annotations

import unittest

from agent.android.app_spec_builder import AndroidBuildIntentBuilder
from agent.planning import PlanningEngine
from agent.requirements import RequirementEngine


class AndroidBuildIntentBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.requirements = RequirementEngine()
        self.planning = PlanningEngine()
        self.builder = AndroidBuildIntentBuilder()

    def test_builds_valid_android_intent(self) -> None:
        requirements = self.requirements.analyze(
            "Create an accessible calculator app that works offline."
        )
        plan = self.planning.create_plan(requirements)
        intent = self.builder.build(plan)

        self.assertEqual(intent.family, "utility")
        self.assertEqual(intent.spec.mode, "offline")
        self.assertTrue(intent.spec.accessibility_required)
        self.assertTrue(intent.spec.package_name.startswith("com.aiappbuilder."))

    def test_api_request_selects_online_mode(self) -> None:
        requirements = self.requirements.analyze(
            "Create an app that reads data from an API."
        )
        plan = self.planning.create_plan(requirements)
        intent = self.builder.build(plan)
        self.assertEqual(intent.spec.mode, "online")
        self.assertEqual(intent.family, "api_client")

    def test_api_data_request_stays_api_client(self) -> None:
        requirements = self.requirements.analyze(
            "Create an online app that reads customer data from a server API."
        )
        plan = self.planning.create_plan(requirements)
        intent = self.builder.build(plan)
        self.assertEqual(intent.family, "api_client")

    def test_rejects_invalid_plan(self) -> None:
        with self.assertRaises(TypeError):
            self.builder.build(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
