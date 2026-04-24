from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OcrPage:
    page_number: int
    ocr_text: str
    confidence: float


class OcrProvider(Protocol):
    name: str

    def ocr(self, *, filename: str, mime_type: str, content: bytes) -> list[OcrPage]:
        """Return 1..N pages of OCR text. Must always return at least one page."""

