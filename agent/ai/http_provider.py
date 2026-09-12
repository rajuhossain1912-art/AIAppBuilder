from __future__ import annotations

import json
import os
from urllib import error, request


class HTTPAIProvider:
    """OpenAI-compatible HTTP provider using only the Python standard library.

    The endpoint and credential are supplied at runtime through environment
    variables; no secret is stored in source control.
    """

    name = "http"

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.base_url = (base_url or os.getenv("AIAPPBUILDER_AI_BASE_URL", "")).strip().rstrip("/")
        self.api_key = api_key if api_key is not None else os.getenv("AIAPPBUILDER_AI_API_KEY", "")
        self.model = (model or os.getenv("AIAPPBUILDER_AI_MODEL", "")).strip()
        self.timeout = timeout

    def _endpoint(self) -> str:
        if not self.base_url:
            raise RuntimeError("AIAPPBUILDER_AI_BASE_URL is not configured")
        if not self.model:
            raise RuntimeError("AIAPPBUILDER_AI_MODEL is not configured")
        return f"{self.base_url}/chat/completions"

    def complete(self, *, purpose: str, prompt: str) -> str:
        if not purpose.strip() or not prompt.strip():
            raise ValueError("purpose and prompt must not be empty")

        payload = json.dumps(
            {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": f"You are AIAppBuilder. Task purpose: {purpose.strip()}"},
                    {"role": "user", "content": prompt},
                ],
            }
        ).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = request.Request(self._endpoint(), data=payload, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:1000]
            raise RuntimeError(f"AI provider HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"AI provider connection failed: {exc.reason}") from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError("AI provider returned invalid JSON") from exc

        try:
            text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("AI provider response has no choices[0].message.content") from exc
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError("AI provider returned empty content")
        return text.strip()
