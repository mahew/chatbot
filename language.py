import uuid
import requests
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
import azure.cognitiveservices.speech as speech
from msrest.authentication import CognitiveServicesCredentials
from constants import COG_ENDPOINT, COG_KEY, COG_REGION

# Get a client for your text analytics cognitive service resource
TextClient = TextAnalyticsClient(endpoint=COG_ENDPOINT,
                credentials=CognitiveServicesCredentials(COG_KEY))

# Create a function that makes a REST request to the Text Translation service
def translate_text(text, to_lang='en', from_lang='en'):
    # Create the URL for the Text Translator service REST request
    path = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
    params = '&from={}&to={}'.format(from_lang, to_lang)
    constructed_url = path + params

    # Prepare the request headers with Cognitive Services resource key and region
    headers = {
        'Ocp-Apim-Subscription-Key': COG_KEY,
        'Ocp-Apim-Subscription-Region':COG_REGION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Add the text to be translated to the body
    body = [{
        'text': text
    }]

    # Get the translation
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response[0]["translations"][0]["text"]

def get_input_lang(text):
    try:
        language_analysis = TextClient.detect_language(documents=[{"id": 1, "text": text}])
        input_lang = language_analysis.documents[0].detected_languages[0].iso6391_name
    except Exception:
        input_lang = None
    return input_lang

def output_replys(replys, to_lang='en'):
    if to_lang != 'en':
        translated_replys = []
        for reply in replys:
            translated_replys.append(translate_text(reply, to_lang=to_lang))
        replys = translated_replys
    print_replys(replys)

def print_replys(replys):
    for reply in replys:
        print(reply)

def get_audio_input():
    """performs one-shot speech recognition from the default microphone with auto language detection"""
    speech_config = speech.SpeechConfig(subscription=COG_KEY, region=COG_REGION)

    # create the auto detection language configuration with the potential source language candidates
    auto_detect_source_language_config = \
        speech.languageconfig.AutoDetectSourceLanguageConfig(languages=["fr-FR", "en-GB"])
    speech_recognizer = speech.SpeechRecognizer(
        speech_config=speech_config, auto_detect_source_language_config=auto_detect_source_language_config)

    result = speech_recognizer.recognize_once()

    # Check the result
    if result.reason == speech.ResultReason.RecognizedSpeech:
        auto_detect_source_language_result = speech.AutoDetectSourceLanguageResult(result)
        print("Recognized: {} in language {}".format(result.text, auto_detect_source_language_result.language))
    elif result.reason == speech.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speech.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speech.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))   