import os
import requests

API_KEY = os.getenv("OPENAI_API_KEY")
ENDPOINT = "https://api.openai.com/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def classify_and_summarize(email_list):
    """
    Classify emails as Personal/Marketing/Important and return grouped summary.
    """
    system = (
        "You are an email assistant. Given a list of emails, classify each as Personal, Marketing, or Important, "
        "then produce a short summary for each category."
    )
    user_prompt = ""
    for e in email_list:
        snippet = e.get("body", "").replace("\n", " ")[:300]
        user_prompt += (
            f"---\nFrom: {e.get('from')}\nSubject: {e.get('subject')}\n"
            f"Body Snippet: {snippet}\n"
        )
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3
    }
    resp = requests.post(ENDPOINT, headers=HEADERS, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]
