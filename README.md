# Study Buddy (minimal scaffolding)

This repository contains a minimal implementation of the Study Buddy project focusing on logging scaffolding and safe local fallbacks.

Files created:
- `log_config.py` — centralized logger configuration.
- `auth.py` — placeholder authorization that reads/writes `token.json`.
- `google_api_tools.py` — local-first document text extraction and a local "presentation" writer.
- `gemini_processor.py` — deterministic summarizer and flashcard generator (no external LLM calls by default).
- `main.py` — orchestration script that ties everything together.
- `requirements.txt` — packages to install when integrating real APIs.

Quick run (uses local fallbacks):
```bash
python main.py            # will try sample_document.txt, otherwise use placeholder text
python main.py mydoc.txt  # pass a path to a local text file
```

Logs are written to `study_buddy.log`.

To integrate real Google APIs or Gemini, replace the placeholder areas in `auth.py`, `google_api_tools.py`, and `gemini_processor.py` with real client calls and follow the respective client library guides.
