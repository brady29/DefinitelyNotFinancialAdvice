# backend/gemini_client.py

import os
from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def genai_predict(system: str, user: str) -> tuple[str,str]:
    """
    Returns (prediction, explanation).
    prediction is the first line; explanation is the rest.
    """
    prompt = system + "\n\n" + user
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt
    )
    lines = response.text.strip().splitlines()
    pred = lines[0].strip()
    expl = "\n".join(lines[1:]).strip()
    return pred, expl
