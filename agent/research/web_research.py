from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from html import unescape
import re
from urllib import error, request
from urllib.parse import urlparse


@dataclass(frozen=True)
class ResearchSource:
    url: str
    title: str
    fetched_at: str
    content_sha256: str
    text: str


@dataclass(frozen=True)
class ResearchComparison:
    question: str
    sources: tuple[ResearchSource, ...]
    comparison: str


class WebResearch:
    """Safe known-URL research adapter.

    This intentionally fetches only explicitly supplied HTTP(S) URLs. It does
    not pretend to provide general web search. A search provider can be added
    later without changing the evidence model.
    """

    _MAX_BYTES = 2_000_000

    def fetch(self, url: str, *, timeout: float = 20.0) -> ResearchSource:
        parsed = urlparse(url.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Only absolute HTTP(S) URLs are allowed")
        if parsed.username or parsed.password:
            raise ValueError("Credential-bearing URLs are not allowed")

        req = request.Request(
            url,
            headers={"User-Agent": "AIAppBuilder-Research/1.0", "Accept": "text/html,text/plain;q=0.9,*/*;q=0.1"},
            method="GET",
        )
        try:
            with request.urlopen(req, timeout=timeout) as response:
                raw = response.read(self._MAX_BYTES + 1)
                final_url = response.geturl()
                content_type = response.headers.get("Content-Type", "")
        except error.HTTPError as exc:
            raise RuntimeError(f"Research source HTTP {exc.code}: {url}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Research source connection failed: {exc.reason}") from exc

        if len(raw) > self._MAX_BYTES:
            raise RuntimeError("Research source exceeded the maximum allowed response size")
        if "text/" not in content_type and "html" not in content_type and "json" not in content_type:
            raise RuntimeError("Research source is not a supported text response")

        text = self._clean_text(raw.decode("utf-8", errors="replace"))
        title = self._extract_title(raw.decode("utf-8", errors="replace")) or final_url
        return ResearchSource(
            url=final_url,
            title=title,
            fetched_at=datetime.now(timezone.utc).isoformat(),
            content_sha256=hashlib.sha256(raw).hexdigest(),
            text=text,
        )

    def compare(self, question: str, urls: list[str]) -> ResearchComparison:
        if not question.strip():
            raise ValueError("question must not be empty")
        if not urls:
            raise ValueError("at least one source URL is required")
        sources = tuple(self.fetch(url) for url in urls)
        comparison = "\n\n".join(
            f"SOURCE: {source.title}\nURL: {source.url}\nEVIDENCE: {source.text[:6000]}"
            for source in sources
        )
        return ResearchComparison(question=question.strip(), sources=sources, comparison=comparison)

    @staticmethod
    def _extract_title(html: str) -> str:
        match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
        return unescape(re.sub(r"\s+", " ", match.group(1))).strip() if match else ""

    @staticmethod
    def _clean_text(html: str) -> str:
        text = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = unescape(text)
        return re.sub(r"\s+", " ", text).strip()
