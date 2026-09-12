from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch
from urllib.error import URLError

from .http_provider import HTTPAIProvider
from .provider_factory import create_ai_provider


class _Response:
    def __init__(self, payload: dict) -> None:
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return self.payload


class HTTPAIProviderTests(unittest.TestCase):
    def test_missing_configuration_fails_closed(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            provider = HTTPAIProvider()
            with self.assertRaises(RuntimeError):
                provider.complete(purpose="review", prompt="test")

    def test_openai_compatible_response_is_extracted(self) -> None:
        provider = HTTPAIProvider(
            base_url="https://example.test/v1",
            model="test-model",
            api_key="secret",
        )
        payload = {"choices": [{"message": {"content": "  approved  "}}]}
        with patch("agent.ai.http_provider.request.urlopen", return_value=_Response(payload)) as mocked:
            result = provider.complete(purpose="review", prompt="test")
        self.assertEqual(result, "approved")
        req = mocked.call_args.args[0]
        self.assertEqual(req.full_url, "https://example.test/v1/chat/completions")
        self.assertEqual(req.get_header("Authorization"), "Bearer secret")

    def test_connection_error_is_reported(self) -> None:
        provider = HTTPAIProvider(base_url="https://example.test", model="m")
        with patch(
            "agent.ai.http_provider.request.urlopen",
            side_effect=URLError("offline"),
        ):
            with self.assertRaisesRegex(RuntimeError, "connection failed"):
                provider.complete(purpose="review", prompt="test")


class ProviderFactoryTests(unittest.TestCase):
    def test_mock_requires_explicit_opt_in(self) -> None:
        with patch.dict(os.environ, {"AIAPPBUILDER_AI_PROVIDER": "mock"}, clear=True):
            with self.assertRaises(RuntimeError):
                create_ai_provider()
            self.assertEqual(create_ai_provider(allow_mock=True).name, "mock")

    def test_unknown_provider_fails(self) -> None:
        with patch.dict(os.environ, {"AIAPPBUILDER_AI_PROVIDER": "unknown"}, clear=True):
            with self.assertRaises(RuntimeError):
                create_ai_provider()


if __name__ == "__main__":
    unittest.main()
