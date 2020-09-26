import os
import json
import boto3

from common import put_file
from common import read_content

def translate(txt, source='es', target='en'):
    translate = boto3.client('translate')

    response = translate.translate_text(Text=txt,
                                        SourceLanguageCode=source, 
                                        TargetLanguageCode=target)
    
    return response

def translate_from_mediafile(bucket, mediafile_key, source='es', target='en', save=True):
    try:
        content = read_content(bucket, mediafile_key)

        if content:
            content = json.loads(content)

            transcript = content['results']['transcripts'][0]['transcript']
            response = translate(transcript, source, target)

            if save:
                translate_mediafile_key = mediafile_key.replace('json', 'txt').replace('transcribe', '')
                translate_mediafile_key = f'translate{translate_mediafile_key}'
                local_path = 'temp/' + translate_mediafile_key

                with open(local_path, 'w') as file:
                    file.write(response['TranslatedText'])
                
                put_file(bucket, translate_mediafile_key, local_path)
                
                os.remove(local_path)
                return translate_mediafile_key

            else:
                return response
    
    except Exception as err:
        print(err)
        return None


    