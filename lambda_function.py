import os
from datetime import time as dtime
from gmail_utils import authenticate_gmail, fetch_emails_between, get_email_content, send_summary_email
from openai_utils import classify_and_summarize

SUMMARY_EMAIL = os.getenv("SUMMARY_EMAIL")
START_TIME = dtime(0, 0)
END_TIME = dtime(10, 0)


def job():
    service = authenticate_gmail()
    msgs = fetch_emails_between(service, START_TIME, END_TIME)
    if not msgs:
        return
    email_data = [get_email_content(service, m["id"]) for m in msgs]
    summary = classify_and_summarize(email_data)
    send_summary_email(service, SUMMARY_EMAIL, summary)


def lambda_handler(event, context):
    job()
    return {"statusCode": 200, "body": "Summary sent."}
