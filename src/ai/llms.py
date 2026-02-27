from langchain_openai import ChatOpenAI

from langchain_google_genai import ChatGoogleGenerativeAI
from django.conf import settings


def get_required_model(metadata: dict[str, str]):
    match metadata.get("provider"):
        case "Google":
            return ChatGoogleGenerativeAI(
                model=metadata.get("model"),
                temperature=0,
                max_retries=2,
                api_key=settings.GEMINI_API_KEY,
            )

        case "OpenAI":
            return ChatOpenAI(
                model=metadata.get("model"),  # type: ignore
                temperature=0,
                max_retries=2,
                api_key=settings.OPENAI_API_KEY,
            )
        case _:
            return Exception("Provider Not Available")


def get_openai_model(model="gpt-5-nano"):
    return ChatOpenAI(
        model=model, temperature=0, max_retries=2, api_key=settings.OPENAI_API_KEY
    )


# def get_googleai_model(model="gemini-2.0-flash"):
#     return ChatGoogleGenerativeAI(
#         model=model,
#         temperature=0,
#         max_retries=2,
#         api_key=settings.GEMINI_API_KEY,
#     )
