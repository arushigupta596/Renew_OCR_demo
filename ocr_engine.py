"""
OCR Engine: Extracts text from PDF files using PyMuPDF (digital text)
with Tesseract fallback for scanned/image-only pages.

Optimized for large PDFs (300+ pages, 90MB+):
- Uses PyMuPDF native pixmap rendering (no pdf2image/poppler dependency)
- 150 DPI for OCR (4x faster than 300 DPI, sufficient for text)
- Parallel Tesseract OCR with ThreadPoolExecutor
- Only processes actual scanned pages (skips digital + blank pages)
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed


def _ocr_single_page(pdf_path: str, page_num: int, dpi: int = 150) -> tuple[int, str]:
    """
    Render a single page via PyMuPDF pixmap and OCR with Tesseract.

    Args:
        pdf_path: Path to the PDF file.
        page_num: 1-indexed page number.
        dpi: Resolution for rendering (default 150, good balance of speed vs quality).

    Returns:
        Tuple of (page_num, extracted_text).
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]  # 0-indexed
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()

    text = pytesseract.image_to_string(img, lang="eng")
    return page_num, text.strip()


def extract_text_from_pdf(
    pdf_path: str,
    progress_callback=None,
    ocr_progress_callback=None,
    ocr_dpi: int = 150,
    max_workers: int = 4,
) -> list[dict]:
    """
    Extract text from all pages of a PDF.

    Phase 1 (fast): PyMuPDF digital text extraction for all pages.
    Phase 2 (parallel): Tesseract OCR only for scanned/image pages.

    Args:
        pdf_path: Path to the PDF file.
        progress_callback: Optional callable(current_page, total_pages) for Phase 1.
        ocr_progress_callback: Optional callable(current, total, page_num) for Phase 2 OCR.
        ocr_dpi: DPI for Tesseract rendering (default 150).
        max_workers: Number of parallel OCR threads (default 4).

    Returns:
        List of dicts: [{"page_num": int, "text": str, "method": str}, ...]
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    results = []
    scanned_pages = []

    # ── Phase 1: Fast PyMuPDF digital text extraction ──
    for i in range(total_pages):
        page = doc[i]
        text = page.get_text("text")

        if len(text.strip()) >= 50:
            results.append({
                "page_num": i + 1,
                "text": text.strip(),
                "method": "pymupdf",
            })
        else:
            # Check if page has images (worth OCR-ing) vs truly blank
            has_images = len(page.get_images(full=False)) > 0
            if has_images:
                scanned_pages.append(i + 1)  # 1-indexed
                results.append({
                    "page_num": i + 1,
                    "text": "",
                    "method": "pending_ocr",
                })
            else:
                # Truly blank page — no text, no images
                results.append({
                    "page_num": i + 1,
                    "text": text.strip(),  # keep whatever little text there was
                    "method": "no_text",
                })

        if progress_callback:
            progress_callback(i + 1, total_pages)

    doc.close()

    # ── Phase 2: Parallel Tesseract OCR on scanned pages only ──
    # NOTE: Progress callback is called from the MAIN thread (via as_completed)
    # to avoid Streamlit thread-safety issues.
    if scanned_pages:
        total_ocr = len(scanned_pages)
        completed = 0

        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(_ocr_single_page, pdf_path, pn, ocr_dpi): pn
                    for pn in scanned_pages
                }

                for future in as_completed(futures):
                    page_num, ocr_text = future.result()
                    completed += 1

                    # Progress callback on MAIN thread (safe for Streamlit)
                    if ocr_progress_callback:
                        ocr_progress_callback(completed, total_ocr, page_num)

                    # Update the result for this page
                    for r in results:
                        if r["page_num"] == page_num:
                            r["text"] = ocr_text
                            r["method"] = "tesseract"
                            break

        except Exception as e:
            # If Tesseract fails, mark remaining pages as failed
            for r in results:
                if r["method"] == "pending_ocr":
                    r["method"] = f"ocr_failed: {str(e)}"

    # Mark any remaining pending pages
    for r in results:
        if r["method"] == "pending_ocr":
            r["method"] = "no_text"

    return results


def get_combined_text(pages: list[dict], max_chars_per_page: int = 3000) -> str:
    """
    Combine page texts into a single string with page markers.
    Truncates very long pages to avoid exceeding LLM context limits.

    Args:
        pages: Output from extract_text_from_pdf.
        max_chars_per_page: Max characters to keep per page.

    Returns:
        Combined text with page markers.
    """
    parts = []
    for p in pages:
        if not p["text"]:
            continue
        text = p["text"][:max_chars_per_page]
        parts.append(f"--- PAGE {p['page_num']} ---\n{text}")
    return "\n\n".join(parts)


def get_page_count(pdf_path: str) -> int:
    """Get total page count of a PDF."""
    doc = fitz.open(pdf_path)
    count = len(doc)
    doc.close()
    return count
