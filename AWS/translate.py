import os
import json
import boto3
import logging

from .common import put_file
from .common import read_content
from .common import put_object

def translate(txt, source='en', target='es'):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=txt, SourceLanguageCode=source, TargetLanguageCode=target)
    
    return response

def translate_from_mediafile(bucket, mediafile_key, source='en', target='es',prefix='translate_'):
    try:
        content = read_content(bucket, mediafile_key)

        if content:
            content = json.loads(content)

            transcript = content['results']['transcripts'][0]['transcript']
            response = translate(transcript, source, target)
            
            content = response['TranslatedText']
            
            translate_mediafile_key = mediafile_key.replace('.json', '.txt')
            translate_mediafile_key = translate_mediafile_key.replace('transcribe_', prefix)
            
            put_object(bucket, translate_mediafile_key, content)

            return translate_mediafile_key
            
    except Exception as err:
        logging.error("Exception", exc_info=True)
        return None


    