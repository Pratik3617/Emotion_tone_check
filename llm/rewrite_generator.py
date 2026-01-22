from llm.client import get_llm_client

SYSTEM_PROMPT = """
You are rewriting messages for professional workplace communication.

Your primary goal is to REDUCE emotional intensity while preserving intent.

Rules:
- Preserve the original meaning and request.
- Do NOT introduce blame, judgment, or accusation.
- Do NOT amplify negative emotions.
- If the message expresses frustration or disappointment, soften it into a calm, constructive tone.
- Prefer collaborative, solution-oriented language.
- Avoid emotionally charged words (e.g., disappointed, unacceptable, frustrated).
- Keep the rewrite suitable for workplace communication.
- Keep it concise (1–2 sentences).
"""


def generate_rewrite(text: str) -> str:
    """
    Generate the rewrite for the input text.
    """
    client = get_llm_client()

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Rewrite the following message so it sounds calm, professional, "
                    "and collaborative without increasing emotional intensity:\n\n"
                    f"{text}"
                ),
            },
        ],
        temperature = 0.2,
        max_tokens = 60
    )

    rewrite = response.choices[0].message.content.strip()

    # reject emotionally negative rewrites
    BLOCKED_WORDS = [
        "disappointed",
        "unacceptable",
        "frustrated",
        "angry",
        "upset",
    ]

    if any(word in rewrite.lower() for word in BLOCKED_WORDS):
        raise ValueError("Rewrite still emotionally charged")

    return rewrite