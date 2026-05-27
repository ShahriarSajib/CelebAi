from app.services.gemini_service import ask_gemini


def rewrite_query(query: str):

    prompt = f"""
Rewrite this user query into a highly specific search query for a celebrity database.

Rules:
- Add full names if possible
- Add context (football, actor, etc.)
- Make it suitable for semantic search

User Query:
{query}

Return ONLY rewritten query.
"""

    return ask_gemini(prompt)