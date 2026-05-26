def build_celebrity_prompt(query: str, wiki_summary: str, wiki_url: str):

    return f"""
You are a celebrity intelligence system.

Use ONLY the provided verified data.

Wikipedia Summary:
{wiki_summary}

Source:
{wiki_url}

User Query:
{query}

Return structured response:

1. Name
2. Biography
3. Career
4. Achievements
5. Notable Works
6. Fun Facts
7. Summary Insight
"""