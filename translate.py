import json
import boto3

from common import put_file
from common import read_content

BUCKET = 'pywombat'

def translate(txt, source='es', target='en'):
    translate = boto3.client('translate')

    response = translate.translate_text(Text=txt,
                                        SourceLanguageCode=source, 
                                        TargetLanguageCode=target)
    
    return response

def translate_from_mediafile(mediafile_key, source='es', target='en', save=True):
    try:
        content = read_content(BUCKET, mediafile_key)

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
                
                put_file(BUCKET, translate_mediafile_key, local_path)
                
                return translate_mediafile_key

            else:
                return response
    except:
        return None

if __name__ == '__main__':
    
    medifile = 'transcribe_f9b0f6252f354a9ba37f9e3b8820a219_my_custome_job.json'
    response = translate_from_mediafile(medifile)

    print(response)

    