from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.6
)


def ask_gemini(prompt: str):

    response = llm.invoke(prompt)

    return response.content