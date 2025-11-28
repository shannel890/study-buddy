from typing import Any, Dict, List
import json
from datetime import date

"""Templates module

Provides structured templates for notes, flashcards, quizzes, study plans,
document summaries, task lists, and research notes. Includes helpers to
instantiate templates with defaults and render them to Markdown or JSON.
"""


TEMPLATES: Dict[str, Dict[str, Any]] = {
    "note": {
        "title": "Topic / Title",
        "key_points": [],
        "summary": "",
        "definitions": [],
        "examples": [],
        "questions": [],
    },
    "flashcard": {
        "question": "",
        "answer": "",
        "hint": "",
        "difficulty": "Medium",
        "next_review_date": "",
    },
    "quiz": {
        "question": "",
        "options": ["", "", "", ""],
        "correct_answer": "A",
        "explanation": "",
    },
    "study_plan": {
        "weekly_goals": [],
        "subjects": [],
        "daily_targets": {
            "Mon": "",
            "Tue": "",
            "Wed": "",
            "Thu": "",
            "Fri": "",
            "Sat": "",
            "Sun": "",
        },
        "resources_needed": [],
        "progress_percent": 0,
        "notes": "",
    },
    "document_summary": {
        "document_title": "",
        "overview": "",
        "key_highlights": [],
        "important_terms": [],
        "action_items": [],
    },
    "task": {
        "task": "",
        "priority": "Med",
        "deadline": "",
        "status": "Not Started",
        "notes": "",
    },
    "research": {
        "topic": "",
        "objective": "",
        "sources": [],
        "findings": [],
        "conclusion": "",
        "references": [],
    },
}


def get_template(name: str) -> Dict[str, Any]:
    """Return a deep-ish copy of the template structure for `name`.

    Caller may modify the returned dict without altering the canonical template.
    """
    base = TEMPLATES.get(name)
    if base is None:
        raise KeyError(f"Unknown template: {name}")
    # shallow copy is sufficient because nested lists/dicts are intentionally simple
    return json.loads(json.dumps(base))


def instantiate(name: str, values: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Create a filled template by merging `values` into the template defaults."""
    tpl = get_template(name)
    if not values:
        return tpl
    for k, v in values.items():
        if k in tpl:
            tpl[k] = v
        else:
            # allow adding custom fields
            tpl[k] = v
    return tpl


def render_markdown(name: str, content: Dict[str, Any]) -> str:
    """Render the filled template as a Markdown string.

    The output is human-readable and structured for quick copying into notes.
    """
    lines: List[str] = []
    lines.append(f"# {name.replace('_', ' ').title()}")

    def add_section(title: str, body: Any):
        lines.append(f"\n**{title}**\n")
        if isinstance(body, list):
            if not body:
                lines.append("- ")
            for item in body:
                lines.append(f"- {item}")
        elif isinstance(body, dict):
            for subk, subv in body.items():
                lines.append(f"- **{subk}**: {subv}")
        else:
            lines.append(str(body) if body is not None else "")

    # rendering rules per template
    if name == "note":
        add_section("Topic / Title", content.get("title", ""))
        add_section("Key Points", content.get("key_points", []))
        add_section("Summary", content.get("summary", ""))
        add_section("Definitions", content.get("definitions", []))
        add_section("Examples", content.get("examples", []))
        add_section("Questions I Still Have", content.get("questions", []))

    elif name == "flashcard":
        add_section("Question", content.get("question", ""))
        add_section("Answer", content.get("answer", ""))
        add_section("Hint", content.get("hint", ""))
        add_section("Difficulty", content.get("difficulty", ""))
        add_section("Next Review Date", content.get("next_review_date", ""))

    elif name == "quiz":
        add_section("Question", content.get("question", ""))
        add_section("Options", content.get("options", []))
        add_section("Correct Answer", content.get("correct_answer", ""))
        add_section("Explanation", content.get("explanation", ""))

    elif name == "study_plan":
        add_section("Weekly Goals", content.get("weekly_goals", []))
        add_section("Subjects", content.get("subjects", []))
        add_section("Daily Targets", content.get("daily_targets", {}))
        add_section("Resources Needed", content.get("resources_needed", []))
        add_section("Progress (%)", content.get("progress_percent", 0))
        add_section("Notes", content.get("notes", ""))

    elif name == "document_summary":
        add_section("Document Title", content.get("document_title", ""))
        add_section("Overview", content.get("overview", ""))
        add_section("Key Highlights", content.get("key_highlights", []))
        add_section("Important Terms", content.get("important_terms", []))
        add_section("Action Items / To-Do", content.get("action_items", []))

    elif name == "task":
        add_section("Task", content.get("task", ""))
        add_section("Priority", content.get("priority", ""))
        add_section("Deadline", content.get("deadline", ""))
        add_section("Status", content.get("status", ""))
        add_section("Notes", content.get("notes", ""))

    elif name == "research":
        add_section("Topic", content.get("topic", ""))
        add_section("Objective", content.get("objective", ""))
        add_section("Sources", content.get("sources", []))
        add_section("Findings", content.get("findings", []))
        add_section("Conclusion", content.get("conclusion", ""))
        add_section("References", content.get("references", []))

    else:
        # generic dump
        lines.append("\n``json\n")
        lines.append(json.dumps(content, indent=2))
        lines.append("\n```")

    return "\n".join(lines)


def save_markdown(path: str, md: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)


def save_json(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)


if __name__ == "__main__":
    # Demo: create a note template and save as markdown
    note = instantiate("note", {"title": "Sample Topic", "key_points": ["A", "B"], "summary": "Short summary."})
    md = render_markdown("note", note)
    fname = f"note_{date.today().isoformat()}.md"
    save_markdown(fname, md)
    print(f"Wrote {fname}")
