from typing import List, Tuple

from google.cloud import translate_v2
from google.oauth2 import service_account


def translate(text, credentials):
    translate_client = translate_v2.Client(credentials=credentials)
    result = translate_client.translate(text, target_language='en', source_language='pl')
    return result["translatedText"]


def translate_list_of_chunks(chunks: List[Tuple[int, str]], apikey_path: str) -> List[Tuple[int, str]]:
    result_list = []
    credentials = service_account.Credentials.from_service_account_file(apikey_path)

    for chunk in chunks:
        translated = translate(chunk[1], credentials)
        result_list.append((chunk[0], translated))
    return result_list


if __name__ == '__main__':
    chunks_list = [(0, "Wszedł kotek na płotek. Lubię placki."), (1, "inny język"), (2, 'ostatnia partia')]
    translate_list_of_chunks(chunks_list, 'apikey.json')
