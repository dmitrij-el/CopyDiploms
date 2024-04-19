import logging
import requests

from tele_bot.config.config import API_KEY_RAPID, API_HOST_RAPID_MICROSOFT_AZURE


def microsoft_translation(text: str, from_lang: str = "ru", to_lang: str = "en") -> str:
    """
    Функция с помощью MICROSOFT_AZURE переводит текст. Хост - RapidAPI.

    param text: Текст для перевода.
    param from_lang: Язык с которого переводится текст.
    param to_lang: Язык на который переводится текст.

    return:  Переведенный текст.



    """

    try:
        url = "https://microsoft-translator-text.p.rapidapi.com/translate"

        querystring = {
            "from": f"{from_lang}",
            "to[0]": f"{to_lang}",
            "api-version": "3.0",
            "profanityMarker": "Asterisk",
            "profanityAction": "NoAction",
            "textType": "plain"
        }

        payload = [{'Text': text}]
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": API_KEY_RAPID,
            "X-RapidAPI-Host": API_HOST_RAPID_MICROSOFT_AZURE
        }

        response = requests.post(url, json=payload, headers=headers, params=querystring)
        resp_json = response.json()
        answer = resp_json[0]['translations'][0]['text']
        return answer
    except Exception as exp:
        logging.error(exp)
