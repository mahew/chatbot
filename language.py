import uuid
import requests
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
import azure.cognitiveservices.speech as speech
from msrest.authentication import CognitiveServicesCredentials

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes

from array import array
import os
import sys
import time


from constants import COG_ENDPOINT, COG_KEY, COG_REGION, CV_KEY, CV_ENDPOINT

# Get a client for your text analytics cognitive service resource
text_client = TextAnalyticsClient(endpoint=COG_ENDPOINT,
                credentials=CognitiveServicesCredentials(COG_KEY))

# Get a client for your cv analytics cognitive service resource
computervision_client = ComputerVisionClient(CV_ENDPOINT, 
                            CognitiveServicesCredentials(CV_KEY))

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

    try:
        text = response[0]["translations"][0]["text"]
    except Exception:
        text = None

    return text

def get_input_lang(text):
    try:
        language_analysis = text_client.detect_language(documents=[{"id": 1, "text": text}])
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
    return replys

def print_replys(replys):
    for reply in replys:
        print(reply)

def read_text(image_path):
    local_image_handwritten = open(image_path, "rb")
    # Call API with image and raw response (allows you to get the operation location)
    recognize_handwriting_results = computervision_client.read_in_stream(local_image_handwritten, raw=True)
    # Get the operation location (URL with ID as last appendage)
    operation_location_local = recognize_handwriting_results.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id_local = operation_location_local.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        recognize_handwriting_result = computervision_client.get_read_result(operation_id_local)
        if recognize_handwriting_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    full_text = ""
    # Print results, line by line
    if recognize_handwriting_result.status == OperationStatusCodes.succeeded:
        for text_result in recognize_handwriting_result.analyze_result.read_results:
            for line in text_result.lines:
                full_text = full_text + line.text + " "

    return full_text