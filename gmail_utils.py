# gmail_utils.py

import os
import base64
from datetime import datetime, time
import pytz
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes for reading and sending Gmail
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]
# Brussels timezone
BRUSSELS = pytz.timezone("Europe/Brussels")


def authenticate_gmail():
    """
    Load and refresh credentials; expects token.json pre-generated with offline access.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise RuntimeError("Missing valid Gmail credentials; generate token.json locally before deploying.")
    return build("gmail", "v1", credentials=creds)


def fetch_emails_between(service, start_time: time, end_time: time):
    """
    Return list of message IDs between start_time and end_time Brussels today.
    """
    today = datetime.now(BRUSSELS).date()
    dt_start = BRUSSELS.localize(datetime.combine(today, start_time))
    dt_end = BRUSSELS.localize(datetime.combine(today, end_time))
    after_ts = int(dt_start.astimezone(pytz.UTC).timestamp())
    before_ts = int(dt_end.astimezone(pytz.UTC).timestamp())
    query = f"after:{after_ts} before:{before_ts}"
    try:
        resp = service.users().messages().list(userId="me", q=query).execute()
        return resp.get("messages", [])
    except HttpError:
        return []


def get_email_content(service, message_id):
    """
    Return subject, sender, and body snippet for a message.
    """
    try:
        msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()
    except HttpError:
        return {}
    headers = msg.get("payload", {}).get("headers", [])
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "")
    body = ""
    for part in msg.get("payload", {}).get("parts", []):
        data = part.get("body", {}).get("data")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            break
    return {"subject": subject, "from": sender, "body": body}


def send_summary_email(service, to_address: str, summary: str):
    """
    Send the summary via Gmail API.
    """
    message = MIMEText(summary)
    message["to"] = to_address
    message["from"] = "me"
    message["subject"] = "Morning Email Summary"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
