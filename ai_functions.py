import os
from openai import OpenAI

client = OpenAI(
    api_key="Your API Key Here"
)

# =====================
# Generate Summary
# =====================
def generate_summary(document_text):
    prompt = f"""
You are an AI document assistant.

Read the document and create a professional business summary.

Use this exact structure:

Short Summary:
- 3 to 5 concise bullet points

Detailed Summary:
- Main topic
- Important details
- Risks or concerns
- Decisions mentioned
- Action items mentioned

Document:
{document_text[:12000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# =====================
# Extract Key Data
# =====================
def extract_key_data(document_text):
    prompt = f"""
You are an AI assistant that extracts structured business information.

Extract the following information from the document.

Use this exact structure:

Key Dates:
- ...

Names / Organizations:
- ...

Risks:
- ...

Action Items:
- ...

Decisions:
- ...

Important or Unusual Content:
- ...

If something is missing, write:
"Not mentioned"

Document:
{document_text[:12000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# =====================
# Q&A
# =====================
def answer_question(document_text, question):
    prompt = f"""
You are an AI document assistant.

Answer the user's question ONLY using the document below.

If the answer is not found in the document, say:
"I cannot find that information in the document."

Document:
{document_text[:12000]}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content