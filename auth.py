import json
import os
from typing import Optional

from log_config import setup_logger

logger = setup_logger('auth')

TOKEN_PATH = "token.json"
CLIENT_SECRETS = "client_secrets.json"
SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/presentations",
]


def authorize() -> Optional[object]:
    """Obtain Google credentials if possible.

    Behavior:
    - If `token.json` exists and google-auth is available, load credentials from it.
    - If credentials are missing or invalid and `client_secrets.json` is present,
      run the local OAuth flow to obtain new credentials and save them to `token.json`.
    - If google-auth libraries are not installed or client secrets are missing,
      fall back to a placeholder token (keeps the app runnable).

    Returns a credentials object when google-auth is used, otherwise returns a simple dict placeholder.
    """
    logger.info("Starting authorization process.")
    try:
        try:
            # Attempt to use google-auth libraries if available
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
        except Exception:
            logger.warning("Google auth libraries not available; using placeholder credentials.")
            # fallback placeholder
            return _write_placeholder_token()

        creds = None
        if os.path.exists(TOKEN_PATH):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
                logger.info("Loaded credentials from %s.", TOKEN_PATH)
            except Exception:
                logger.warning("Failed to load credentials from %s; will attempt refresh or new flow.", TOKEN_PATH)

        # If no valid creds, and client_secrets available, run flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("Refreshed expired credentials.")
                except Exception as e:
                    logger.warning("Failed to refresh credentials: %s", e)

            if not creds or not creds.valid:
                if os.path.exists(CLIENT_SECRETS):
                    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
                    creds = flow.run_local_server(port=0)
                    # save for next run
                    with open(TOKEN_PATH, "w", encoding="utf-8") as token:
                        token.write(creds.to_json())
                    logger.info("Obtained new credentials via OAuth and saved to %s.", TOKEN_PATH)
                else:
                    logger.warning("%s not found; cannot run OAuth flow. Using placeholder credentials.", CLIENT_SECRETS)
                    return _write_placeholder_token()

        return creds

    except Exception as e:
        logger.error("Authorization failed: %s", e, exc_info=True)
        return _write_placeholder_token()


def _write_placeholder_token() -> dict:
    token = {"access_token": "placeholder", "created": True}
    try:
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            json.dump(token, f, indent=2)
        logger.info("Created placeholder credentials and saved to %s.", TOKEN_PATH)
    except Exception:
        logger.warning("Could not write placeholder %s.", TOKEN_PATH)
    return token


if __name__ == "__main__":
    authorize()
