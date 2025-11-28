import sys
from log_config import setup_logger

from auth import authorize
from google_api_tools import get_document_text, create_flashcard_deck
from gemini_processor import summarize_notes, generate_flashcards
from templates import instantiate, render_markdown, save_markdown, save_json
from datetime import date

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
                raise
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

        # Prepare container for highlight-created flashcards
        highlight_cards = []

        # Populate and save a document summary using templates
        try:
            doc_title = doc_id if doc_id else "local_sample"
            doc_summary = instantiate("document_summary", {
                "document_title": doc_title,
                "overview": summary,
                # simple heuristic: use first 3 sentences as key highlights
                "key_highlights": [s.strip() for s in summary.split('.') if s.strip()][:3],
                "important_terms": [],
                "action_items": [],
            })

            md = render_markdown("document_summary", doc_summary)
            md_fname = f"document_summary_{doc_title}_{date.today().isoformat()}.md"
            json_fname = f"document_summary_{doc_title}_{date.today().isoformat()}.json"
            save_markdown(md_fname, md)
            save_json(json_fname, doc_summary)
            logger.info("Saved document summary: %s and %s", md_fname, json_fname)

            # Create flashcards directly from highlights
            highlights = doc_summary.get("key_highlights", [])
            for i, h in enumerate(highlights, start=1):
                try:
                    # Attempt to generate a better-formulated flashcard from the highlight
                    generated = generate_flashcards(h, n=1)
                    if generated and isinstance(generated, list) and len(generated) > 0:
                        # Merge generated flashcard into the flashcard template to ensure fields
                        card = instantiate("flashcard", generated[0])
                    else:
                        # Fallback simple phrasing
                        q = f"Explain: {h[:60].strip()}?"
                        a = h
                        card = instantiate("flashcard", {
                            "question": q,
                            "answer": a,
                            "hint": "Review the document highlights",
                            "difficulty": "Medium",
                            "next_review_date": "",
                        })
                    highlight_cards.append(card)
                except Exception:
                    logger.warning("generate_flashcards failed for highlight #%d; using fallback card.", i, exc_info=True)
                    q = f"Explain: {h[:60].strip()}?"
                    a = h
                    card = instantiate("flashcard", {
                        "question": q,
                        "answer": a,
                        "hint": "Review the document highlights",
                        "difficulty": "Medium",
                        "next_review_date": "",
                    })
                    highlight_cards.append(card)

            if highlight_cards:
                highlights_fname = f"flashcards_from_highlights_{doc_title}_{date.today().isoformat()}.json"
                save_json(highlights_fname, highlight_cards)
                logger.info("Saved %d highlight-derived flashcards to %s", len(highlight_cards), highlights_fname)

        except Exception as e:
            logger.error("Failed to create/save document summary: %s", e, exc_info=True)

        # Generate flashcards (LLM/deterministic) and combine with highlight-derived cards
        generated_cards = generate_flashcards(summary, n=10)
        # combine: give precedence to highlight-derived cards first
        final_flashcards = highlight_cards + generated_cards
        logger.info("Generated %d flashcards (including %d from highlights).", len(final_flashcards), len(highlight_cards))

        # Create a simple presentation locally
        presentation = create_flashcard_deck(final_flashcards)
        logger.info("Presentation created: %s", presentation.get("url"))

        logger.info("Study Buddy process complete. Check the log file for details.")
        return presentation

    except Exception as e:
        logger.critical("Study Buddy script crashed: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
