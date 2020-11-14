from google.cloud import translate_v2
from google.oauth2 import service_account


def translate(text):
    my_credentials = service_account.Credentials.from_service_account_file('apikey.json')
    translate_client = translate_v2.Client(credentials=my_credentials)
    result = translate_client.translate(text, target_language='en', source_language='pl')

    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    return result["translatedText"]


def translate_list_of_chunks(chunks: list) -> list:
    """ Accepts list of tuples like [(int, string), ...]"""
    result_list = []
    for chunk in chunks:
        translated = translate(chunk[1])
        result_list.append((chunk[0], translated))
    return result_list


if __name__ == '__main__':
    chunks_list = [(0, "Wszedł kotek na płotek. Lubię placki."), (1, "inny język"), (2, 'ostatnia partia')]
    translate_list_of_chunks(chunks_list)
