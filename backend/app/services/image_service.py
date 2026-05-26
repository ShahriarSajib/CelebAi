import wikipedia


def get_celebrity_image(query: str):

    try:
        page = wikipedia.page(query)

        images = page.images

        if images:
            return images[0]

        return None

    except Exception:
        return None