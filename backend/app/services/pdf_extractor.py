import logging
import os
import tempfile
from pathlib import Path

logger = logging.getLogger("aduanflow")


def _find_tesseract_cmd() -> str:
    """Locate the Tesseract OCR engine binary across common install paths."""
    env_cmd = os.getenv("TESSERACT_CMD")
    if env_cmd and os.path.exists(env_cmd):
        return env_cmd
    candidates = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Tesseract-OCR", "tesseract.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Tesseract-OCR", "tesseract.exe"),
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
    ]
    for p in candidates:
        if p and os.path.exists(p):
            return p
    return ""


def _ocr_pdf_via_image(doc) -> str:
    """Render each PDF page to an image and run Tesseract OCR.

    Used as a fallback when a PDF has no extractable text layer (e.g. scanned
    statements). Returns the concatenated OCR text, or '' on any failure so the
    pipeline never hard-crashes on a scanned/unsupported file.
    """
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        return ""

    tesseract_cmd = _find_tesseract_cmd()
    if not tesseract_cmd:
        logger.warning("[PdfExtractor] Tesseract engine not found; OCR skipped for scanned PDF.")
        return ""
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    pages = []
    for page_idx in range(len(doc)):
        page = doc.load_page(page_idx)
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        pages.append(pytesseract.image_to_string(img))
    return "\n".join(p for p in pages if p).strip()


def pdf_text_from_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF document using PyMuPDF.
    Falls back to Tesseract OCR for scanned/image-based PDFs.
    Exposed as a tool that the LLM agent may call (the 'PDF/OCR' Pdf skill).
    """
    if not pdf_bytes:
        return ""
    try:
        import fitz  # PyMuPDF
    except ImportError as exc:
        logger.error(f"[PdfExtractor] PyMuPDF not available: {exc}")
        return ""

    tmp_path = None
    try:
        # Write to a temp file so PyMuPDF can open it reliably
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name

        doc = fitz.open(tmp_path)
        pages_text = []
        for page_idx in range(len(doc)):
            page = doc.load_page(page_idx)
            pages_text.append(page.get_text("text"))
        text = "\n".join(pages_text).strip()
        if not text:
            logger.info("[PdfExtractor] No text layer; falling back to Tesseract OCR for scanned PDF.")
            text = _ocr_pdf_via_image(doc)
        doc.close()
        return text
    except Exception as exc:
        logger.warning(f"[PdfExtractor] Failed to parse PDF: {exc}")
        return ""
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass