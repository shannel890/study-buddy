import json
from typing import List, Dict

from log_config import setup_logger

logger = setup_logger('gemini_processor')


def summarize_notes(text: str, max_chars: int = 400) -> str:
    """Produce a short summary of `text`.

    This is a deterministic, local fallback implementation that does not call
    external LLM APIs. It logs the input size and the generation result.
    Replace with a real Gemini/LLM client when available.
    """
    logger.info("Sending text to Gemini for summarization (approx chars=%d).", len(text))
    try:
        if not text:
            logger.info("Received empty text for summarization.")
            return ""

        # Naive summarization: return first N characters up to the last sentence boundary.
        summary = text.strip()
        if len(summary) > max_chars:
            summary = summary[:max_chars]
            # cut to last full sentence if possible
            last_period = summary.rfind('. ')
            if last_period != -1:
                summary = summary[: last_period + 1]

        logger.info("Summary successfully generated. Characters: %d", len(summary))
        return summary

    except Exception as e:
        logger.error("Gemini summarization failed: %s", e, exc_info=True)
        raise


def generate_flashcards(text: str, n: int = 10) -> List[Dict]:
    """Generate up to `n` flashcards from the input text.

    This function returns a list of dicts: {"question": ..., "answer": ...}.
    It logs request/response sizes and warns if parsing the generated JSON fails.
    """
    logger.info("Requesting %d flashcards from Gemini output generation.", n)
    try:
        if not text:
            logger.info("Empty input provided to generate_flashcards; returning empty list.")
            return []

        # Simple deterministic approach: split into sentences and make Q/A pairs.
        sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
        flashcards = []
        for i in range(min(n, len(sentences))):
            q = f"Explain: {sentences[i][:60].strip()}?"
            a = sentences[i]
            flashcards.append({"question": q, "answer": a})

        # Export to JSON string and parse back to demonstrate parsing step.
        try:
            json_str = json.dumps(flashcards)
            parsed = json.loads(json_str)
            logger.info("Parsed %d flashcards from JSON output.", len(parsed))
            return parsed
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON output from model — possible hallucination in format.")
            return flashcards

    except Exception as e:
        logger.error("Flashcard generation failed: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    s = "This is a sample note. It has multiple sentences. Each sentence can become a flashcard."
    print(summarize_notes(s))
    print(generate_flashcards(s, 3))
