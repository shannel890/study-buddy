import sys
from log_config import setup_logger

from auth import authorize
from google_api_tools import get_document_text, create_flashcard_deck
from gemini_processor import summarize_notes, generate_flashcards

logger = setup_logger('main')


def main(doc_id: str | None = None):
    logger.info("Study Buddy workflow initiated.")
    try:
        creds = authorize()
        if creds:
            logger.info("Authorization completed.")
        else:
            logger.info("Proceeding without valid credentials (using local fallbacks).")

        # Determine document source
        text = ""
        if doc_id:
            try:
                # pass credentials to allow API retrieval when possible
                text = get_document_text(doc_id, creds=creds)
                logger.info("Notes successfully fetched from document: %s", doc_id)
            except FileNotFoundError:
                logger.error("Document %s not found locally and API fetch failed.", doc_id)
                print(f"Error: The file '{doc_id}' was not found.")
                sys.exit(1)
            except Exception:
                logger.error("Unable to fetch notes for document_id=%s; aborting document step.", doc_id)
                raise
        else:
            # Try a local default file first
            try:
                text = get_document_text("sample_document.txt", creds=creds)
                logger.info("Notes successfully fetched from local sample_document.txt.")
            except Exception:
                logger.warning("No document provided and no local sample found; using placeholder notes.")
                text = "Placeholder notes: no document provided. Add a text file or pass a document id."

        # Summarize notes
        summary = summarize_notes(text)
        logger.info("Notes summarization complete.")

        # Generate flashcards
        flashcards = generate_flashcards(summary, n=10)
        logger.info("Generated %d flashcards.", len(flashcards))

        # Create a simple presentation locally
        presentation = create_flashcard_deck(flashcards)
        logger.info("Presentation created: %s", presentation.get("url"))
        print(f"Presentation created: {presentation.get('url')}")

        logger.info("Study Buddy process complete. Check the log file for details.")
        return presentation

    except Exception as e:
        logger.critical("Study Buddy script crashed: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
