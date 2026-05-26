import wikipedia


def get_wikipedia_summary(query: str):

    try:
        summary = wikipedia.summary(query, sentences=5)

        page = wikipedia.page(query)

        return {
            "summary": summary,
            "url": page.url
        }

    except Exception as e:

        return {
            "summary": "No Wikipedia data found.",
            "url": None
        }