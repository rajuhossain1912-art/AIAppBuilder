from __future__ import annotations

from dataclasses import dataclass

from agent.requirements import RequirementEngine, RequirementSet


@dataclass(frozen=True)
class ClientOrderBrief:
    """A structured, reviewable brief collected from a client order."""

    requirements: RequirementSet
    questions: tuple[str, ...]
    ready_for_approval: bool


class ClientOrderIntake:
    """Turn a client message into a conservative order brief and targeted questions."""

    def __init__(self, requirements_engine: RequirementEngine | None = None) -> None:
        self.requirements_engine = requirements_engine or RequirementEngine()

    def start(self, client_message: str) -> ClientOrderBrief:
        requirements = self.requirements_engine.analyze(client_message)
        questions = self._questions(requirements)
        return ClientOrderBrief(
            requirements=requirements,
            questions=tuple(questions),
            ready_for_approval=not questions,
        )

    @staticmethod
    def _questions(requirements: RequirementSet) -> list[str]:
        text = requirements.normalized_request.casefold()
        questions: list[str] = []

        if len(text.split()) < 5:
            questions.append(
                "What is the app's main purpose and the most important task users must be able to complete?"
            )

        if any(token in text for token in ("youtube", "facebook", "video", "channel", "page")):
            questions.append(
                "Which channel, page, or content source should the app use, and what public links or identifiers should be connected?"
            )

        if any(token in text for token in ("api", "server", "endpoint", "online", "internet", "cloud")):
            if not any(token in text for token in ("http://", "https://", "endpoint", "api url", "api link")):
                questions.append(
                    "What approved API, website, or server endpoint should the app use, and what data should it read or send?"
                )

        if any(token in text for token in ("login", "account", "register", "sign in")):
            questions.append(
                "Is user login required? If yes, what account fields and approved authentication method are required?"
            )

        if not any(token in text for token in ("offline", "online", "internet", "api", "server", "cloud")):
            questions.append("Should the app work fully offline, online, or use a hybrid approach?")

        # These are not blockers unless the client request is too vague to implement.
        # Branding, optional features, and device-specific details can be collected
        # after the core brief is approved instead of blocking every order.
        return list(dict.fromkeys(questions))
