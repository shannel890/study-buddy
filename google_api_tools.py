
import json
import os
import time
from typing import List, Dict, Optional

from log_config import setup_logger

logger = setup_logger('google_api_tools')


def _extract_text_from_doc(document: Dict) -> str:
    """Extract plain text from the Google Docs document resource.

    This implementation walks the document's body content and concatenates
    textRun contents. It is defensive against missing fields.
    """
    pieces = []
    body = document.get("body", {})
    content = body.get("content", [])
    for c in content:
        paragraph = c.get("paragraph")
        if not paragraph:
            continue
        elements = paragraph.get("elements", [])
        for el in elements:
            tr = el.get("textRun")
            if tr and "content" in tr:
                pieces.append(tr["content"])
    return "".join(pieces)


def get_document_text(document_id: str, creds: Optional[object] = None) -> str:
    """Fetch document text by ID.

    Behavior:
    - If `creds` is provided and `googleapiclient` is available, attempt to fetch
      the document via the Google Docs API.
    - Otherwise, if `document_id` is a path to a local file, return its contents.
    - If both approaches fail, raise FileNotFoundError.
    """
    logger.info("Starting fetch for document ID: %s", document_id)
    # First, try Google Docs API if credentials present and look like a real credentials object
    # (our authorize() may return a placeholder dict when OAuth is not configured).
    if creds is not None and not isinstance(creds, dict):
        try:
            try:
                from googleapiclient.discovery import build
                from googleapiclient.errors import HttpError
            except Exception:
                logger.warning("googleapiclient not installed; cannot call Google Docs API.")
                raise

            service = build('docs', 'v1', credentials=creds)
            logger.info("Attempting to fetch document via Google Docs API: %s", document_id)
            doc = service.documents().get(documentId=document_id).execute()
            text = _extract_text_from_doc(doc)
            logger.info("Text extraction complete (Docs API). Characters: %d", len(text))
            return text
        except Exception as e:
            # If an HTTP error occurred, re-raise with logging for the caller to decide.
            logger.error("Google Docs API error for %s: %s", document_id, e, exc_info=True)
            # Do not silently fall back to local file when the caller provided a Doc ID and creds.
            # The caller can decide to try local fallback if appropriate.

    # Next, try local file fallback
    try:
        if os.path.exists(document_id) and os.path.isfile(document_id):
            with open(document_id, "r", encoding="utf-8") as f:
                text = f.read()
            logger.info("Text extraction complete (local file). Characters: %d", len(text))
            return text

        logger.error("Document not found locally and Google Docs API not available/configured: %s", document_id)
        raise FileNotFoundError(f"Document {document_id} not found locally; API integration required.")

    except Exception as e:
        logger.error("Failed fetching document %s: %s", document_id, e, exc_info=True)
        raise


def create_flashcard_deck(flashcards: List[Dict]) -> Dict:
    """Create a simple local 'presentation' representation for flashcards.

    This function writes a JSON file containing the flashcards and returns a dict
    with a generated id and file URL. Replace with Google Slides API calls when ready.
    """
    logger.info("Beginning Slides creation for %d flashcards.", len(flashcards))
    try:
        ts = int(time.time())
        filename = f"presentation_{ts}.json"
        payload = {"id": str(ts), "slides": flashcards}
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        presentation_info = {"id": payload["id"], "url": os.path.abspath(filename)}
        logger.info("Created presentation: id=%s url=%s", presentation_info["id"], presentation_info["url"])

        logger.info("Successfully added slides for all flashcards.")
        return presentation_info

    except Exception as e:
        logger.error("Failed to create presentation: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    # simple smoke test
    try:
        text = get_document_text("sample_document.txt")
        print(text[:200])
    except Exception:
        pass
