from googleapiclient.discovery import build
# You would need to load your credentials here using `google-auth-oauthlib`

def get_document_text(doc_id, credentials):
    """Extracts all text from a Google Doc using the Docs API."""
    try:
        service = build('docs', 'v1', credentials=credentials)
        document = service.documents().get(documentId=doc_id).execute()

        # Simplified logic to combine all text from paragraphs
        text_content = ""
        for element in document.get('body').get('content'):
            if 'paragraph' in element:
                for elem in element.get('paragraph').get('elements'):
                    if 'textRun' in elem:
                        text_content += elem.get('textRun').get('content')

        return text_content
    except Exception as e:
        print(f"Error accessing Google Doc: {e}")
        return None

# --- Full Workflow ---
# 1. Authenticate and get 'credentials' object
# 2. Get the raw text
# raw_notes = get_document_text('YOUR_DOCUMENT_ID', credentials)

# 3. If raw_notes is not None:
#    summary = summarize_notes(raw_notes)
#    print(summary)