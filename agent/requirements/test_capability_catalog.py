import unittest

from agent.requirements import RequirementEngine, classify_capabilities


class CapabilityCatalogTests(unittest.TestCase):
    def test_mixed_media_business_app_is_composable(self):
        request = "Create a Bangla AI voice video maker for a business with image and audio features"
        matches = classify_capabilities(request)
        keys = {match.key for match in matches}
        self.assertTrue({"business", "video", "audio", "image"}.issubset(keys))

    def test_common_app_families_are_not_limited_to_one_template(self):
        engine = RequirementEngine()
        requests = [
            "scholarship education app",
            "sports score app",
            "personal profile app",
            "online newspaper news app",
            "merchant business app",
            "calculator and Bengali calendar app",
            "guitar and tabla music instrument app",
            "Bangla English typing keyboard app",
        ]
        for request in requests:
            with self.subTest(request=request):
                result = engine.analyze(request)
                self.assertTrue(result.capabilities)
                self.assertTrue(result.functional)

    def test_accessible_media_and_accessibility_tools_are_recognized(self):
        request = (
            "Build an accessible audio editor and accessible video editor with "
            "a screen reader accessibility utility and voice studio"
        )
        keys = {match.key for match in classify_capabilities(request)}
        self.assertTrue(
            {"audio_editor", "video_editor", "accessibility_utility", "audio"}.issubset(keys)
        )

    def test_unknown_app_idea_is_preserved_as_general(self):
        result = RequirementEngine().analyze("Build a new kind of community utility app")
        self.assertEqual(result.capabilities[0].key, "general")
        self.assertIn("new kind of community utility app", result.normalized_request)


if __name__ == "__main__":
    unittest.main()
