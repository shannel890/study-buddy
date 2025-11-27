Phase 1: Logging Utility (log_config.py)
Create a new file named log_config.py. This will set up the logger configuration, ensuring all files use the same format and log to the specified file.

Goal: Define a configuration function setup_logger() that initializes the logging system.

Define setup_logger():

Set the log file name to study_buddy.log.

Set the logging level to INFO.

Use a formatter to include the timestamp, severity level, module name, and the log message.

Add a file handler to write messages to the log file.

Return the configured logger instance.

Phase 2: Integrating Logging into Modules
Update the existing files (auth.py, google_api_tools.py, gemini_processor.py, and main.py) to import and use the logger for tracking key actions and outcomes.

A. Update auth.py
Goal: Log the start and success/failure of the authorization process.

Import: Import setup_logger from log_config.

Initialize: Add logger = setup_logger('auth') at the beginning of the file.

Log Points:

Log INFO when the authorization process begins.

Log INFO when credentials are successfully loaded from token.json or created via the browser.

Log ERROR if authorization fails or an exception occurs during the OAuth flow.

B. Update google_api_tools.py
Goal: Log the extraction of notes and the creation of the Slides deck.

Initialize: Add logger = setup_logger('google_api_tools') at the beginning of the file.

get_document_text Logs:

Log INFO when starting to fetch a document by ID.

Log INFO when text extraction is complete, including the number of characters extracted.

Log ERROR if the document is not found or the API call fails.

create_flashcard_deck Logs:

Log INFO when the Slides creation process begins.

Log INFO when the new presentation is created, including its ID and URL.

Log INFO after successfully adding slides for all flashcards.

C. Update gemini_processor.py
Goal: Log the input size and successful generation of AI content.

Initialize: Add logger = setup_logger('gemini_processor') at the beginning of the file.

summarize_notes Logs:

Log INFO when sending text to Gemini for summarization, noting the input token count (or approximate character length).

Log INFO when the summary is successfully generated.

Log ERROR if the Gemini API call fails.

generate_flashcards Logs:

Log INFO when requesting flashcards.

Log INFO when N flashcards (N being the count) are successfully parsed from the JSON output.

Log WARNING if the JSON parsing fails, indicating potential model hallucination in the output format.

Phase 4: Orchestration (main.py)
Goal: Ensure main.py is the driver, logging the start and end of the entire workflow.

Initialize: Add logger = setup_logger('main') at the beginning of the file.

Log Points:

Log INFO at the start of the main function (e.g., "Study Buddy workflow initiated.").

Log INFO as each module function completes successfully (e.g., "Notes successfully fetched from Google Docs.").

Log INFO at the end of the script (e.g., "Study Buddy process complete. Check the log file for details.").

Use a try...except block to catch general exceptions and log a critical ERROR if the script crashes.