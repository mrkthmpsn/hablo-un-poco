"""
File for utils relating to using the Google Translate API
"""

import base64
import json
import os

from dotenv import load_dotenv
from google.cloud import translate
from google.oauth2.credentials import Credentials

load_dotenv()


# The ADC is somewhere locally now and I'm going to have to re-do the authentication process to push to streamlit which
# is going to be a nightmare because Google docs are so damn confusing
def print_supported_languages(display_language_code: str):
    client = translate.TranslationServiceClient(
        credentials=Credentials.from_authorized_user_file(
            os.getenv("GOOGLE_APP_CREDENTIALS_PATH")
        )
    )

    response = client.get_supported_languages(
        parent=os.getenv("GOOGLE_PROJECT_PARENT"),
        display_language_code=display_language_code,
    )

    languages = response.languages
    print(f" Languages: {len(languages)} ".center(60, "-"))
    for language in languages:
        language_code = language.language_code
        display_name = language.display_name
        print(f"{language_code:10}{display_name}")


def translate_text(text: str, target_language_code: str) -> translate.Translation:

    client = translate.TranslationServiceClient(
        credentials=Credentials.from_authorized_user_file(
            os.getenv("GOOGLE_APP_CREDENTIALS_PATH")
        )
    )

    response = client.translate_text(
        parent=os.getenv("GOOGLE_PROJECT_PARENT"),
        contents=[text],
        target_language_code=target_language_code,
    )

    return response.translations[0]
