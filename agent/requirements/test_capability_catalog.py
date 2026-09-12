from agent.requirements import RequirementEngine, classify_capabilities


def test_mixed_media_business_app_is_composable():
    request = "Create a Bangla AI voice video maker for a business with image and audio features"
    matches = classify_capabilities(request)
    keys = {match.key for match in matches}
    assert {"business", "video", "audio", "image"}.issubset(keys)


def test_common_app_families_are_not_limited_to_one_template():
    engine = RequirementEngine()
    requests = [
        "scholarship education app",
        "sports score app",
        "personal profile app",
        "online newspaper news app",
        "merchant business app",
        "calculator and Bengali calendar app",
    ]
    for request in requests:
        result = engine.analyze(request)
        assert result.capabilities
        assert result.functional


def test_unknown_app_idea_is_preserved_as_general():
    result = RequirementEngine().analyze("Build a new kind of community utility app")
    assert result.capabilities[0].key == "general"
    assert "new kind of community utility app" in result.normalized_request
