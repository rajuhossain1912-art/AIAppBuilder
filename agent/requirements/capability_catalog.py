from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapabilityMatch:
    """A capability inferred from the client's natural-language app idea."""

    key: str
    label: str
    evidence: tuple[str, ...]
    confidence: str = "HIGH"


# This is a capability vocabulary, not a list of app templates. Multiple
# capabilities can be composed for one app, and unknown ideas remain valid.
_CAPABILITIES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("education", "Education and scholarship", ("education", "school", "college", "university", "scholarship", "student", "admission", "course")),
    ("sports", "Sports", ("sport", "sports", "football", "soccer", "cricket", "tennis", "match", "score", "league", "tournament")),
    ("profile", "Personal or profile", ("profile", "portfolio", "personal", "cv", "resume", "biography")),
    ("news", "News and online newspaper", ("news", "newspaper", "online newspaper", "breaking news", "article", "journal")),
    ("video", "Video creation and playback", ("video", "movie", "reel", "short video", "video maker", "video editor")),
    ("audio", "Audio and voice", ("audio", "voice", "podcast", "sound", "tts", "text to speech", "voice maker", "voice studio")),
    ("audio_editor", "Accessible audio editing", ("audio editor", "sound editor", "accessible audio editor", "অডিও এডিটর", "অডিও সম্পাদক")),
    ("video_editor", "Accessible video editing", ("video editor", "movie editor", "accessible video editor", "ভিডিও এডিটর", "ভিডিও সম্পাদক")),
    ("accessibility_utility", "Accessibility and screen-reader utilities", ("accessibility", "accessibility service", "screen reader", "talkback utility", "assistive technology", "অ্যাক্সেসিবিলিটি", "স্ক্রিন রিডার")),
    ("text_content", "Text and content generation", ("text generation", "content", "writing", "article generator", "script", "caption")),
    ("business", "Business and merchant", ("business", "merchant", "shop", "store", "inventory", "product catalog", "customer", "order")),
    ("image", "Image creation and processing", ("image", "photo", "picture", "image generation", "poster", "thumbnail")),
    ("calculator", "Calculator and computation", ("calculator", "calculation", "math", "loan calculator", "bmi")),
    ("calendar", "Calendar", ("calendar", "english calendar", "bengali calendar", "bangla calendar", "date", "holiday")),
    ("forms_data", "Forms, records and catalogs", ("form", "forms", "database", "record", "catalog", "directory", "registration", "search")),
    ("online_service", "Online services and API content", ("online", "api", "website", "web service", "server", "cloud", "live data")),
    ("music", "Music and composition", ("music", "musical", "song", "melody", "rhythm", "beat", "chord", "note", "সঙ্গীত", "গান", "সুর", "তাল")),
    ("instrument", "Virtual musical instruments", ("instrument", "guitar", "harmonium", "tabla", "flute", "piano", "violin", "drum", "percussion", "বাদ্যযন্ত্র", "গিটার", "হারমোনিয়াম", "তবলা", "বাঁশি", "পিয়ানো")),
    ("typing_keyboard", "Typing and input keyboard", ("typing keyboard", "input keyboard", "onscreen keyboard", "software keyboard", "bangla keyboard", "english keyboard", "টাইপিং কিবোর্ড", "লেখার কিবোর্ড", "বাংলা কিবোর্ড")),
)


def classify_capabilities(request: str) -> list[CapabilityMatch]:
    """Infer composable capabilities while preserving unknown app ideas."""
    lowered = request.casefold()
    matches: list[CapabilityMatch] = []
    for key, label, hints in _CAPABILITIES:
        evidence = tuple(hint for hint in hints if hint.casefold() in lowered)
        if evidence:
            matches.append(CapabilityMatch(key=key, label=label, evidence=evidence))
    if not matches:
        matches.append(
            CapabilityMatch(
                key="general",
                label="General-purpose application",
                evidence=("No predefined capability matched; preserve the complete client brief for planning.",),
                confidence="MEDIUM",
            )
        )
    return matches
