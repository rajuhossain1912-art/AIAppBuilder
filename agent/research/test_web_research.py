from __future__ import annotations

import unittest
from unittest.mock import patch
from urllib.error import URLError

from .web_research import WebResearch


class _Headers:
    def get(self, name: str, default: str = "") -> str:
        return "text/html; charset=utf-8" if name == "Content-Type" else default


class _Response:
    headers = _Headers()

    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self, size: int = -1) -> bytes:
        return self.body if size < 0 else self.body[:size]

    def geturl(self) -> str:
        return "https://example.test/final"


class WebResearchTests(unittest.TestCase):
    def test_fetch_extracts_title_and_hashes_raw_content(self) -> None:
        body = b"<html><head><title>Example</title></head><body>Hello <b>world</b></body></html>"
        with patch("agent.research.web_research.request.urlopen", return_value=_Response(body)):
            result = WebResearch().fetch("https://example.test")
        self.assertEqual(result.title, "Example")
        self.assertEqual(result.text, "Hello world")
        self.assertEqual(len(result.content_sha256), 64)
        self.assertEqual(result.url, "https://example.test/final")

    def test_rejects_credential_bearing_url(self) -> None:
        with self.assertRaises(ValueError):
            WebResearch().fetch("https://user:pass@example.test")

    def test_connection_failure_is_reported(self) -> None:
        with patch("agent.research.web_research.request.urlopen", side_effect=URLError("offline")):
            with self.assertRaisesRegex(RuntimeError, "connection failed"):
                WebResearch().fetch("https://example.test")

    def test_compare_requires_sources(self) -> None:
        with self.assertRaises(ValueError):
            WebResearch().compare("Which is better?", [])


if __name__ == "__main__":
    unittest.main()
