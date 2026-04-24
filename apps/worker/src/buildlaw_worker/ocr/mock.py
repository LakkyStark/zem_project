from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader

from buildlaw_worker.ocr.base import OcrPage, OcrProvider


class MockOcrProvider:
    name = "mock"

    def ocr(self, *, filename: str, mime_type: str, content: bytes) -> list[OcrPage]:
        # Try text extraction for PDFs (best-effort)
        if mime_type in ("application/pdf",) or filename.lower().endswith(".pdf"):
            try:
                reader = PdfReader(BytesIO(content))
                pages: list[OcrPage] = []
                for i, p in enumerate(reader.pages, start=1):
                    text = (p.extract_text() or "").strip()
                    if text:
                        pages.append(OcrPage(page_number=i, ocr_text=text, confidence=0.95))
                if pages:
                    return pages
            except Exception:
                # fallback below
                pass

        # Fallback: single-page mock
        return [
            OcrPage(
                page_number=1,
                ocr_text=f"MOCK OCR RESULT for {filename}",
                confidence=0.85,
            )
        ]

