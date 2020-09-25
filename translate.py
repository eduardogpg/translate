import os
import json
import boto3

from common import put_file
from common import read_content

BUCKET = 'pywombat'

def translate(txt, source='es', target='en'):
    """
    Transcribe el parámetro txt de source a target utilizando el servicio de translate
    La función retorna el translate 
    """
    translate = boto3.client('translate')

    response = translate.translate_text(Text=txt,
                                        SourceLanguageCode=source, 
                                        TargetLanguageCode=target)
    
    return response

def translate_from_mediafile(mediafile_key, source='es', target='en', save=True):
    """
    Genera una traducción a partir de un archivo remoto (Archivo almacenado en el bucket)
    La función tiene la posibilidad de almacenar la traducción en el bucket, esto mediante un archivo .txt
    """
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
                
                os.remove(local_path)
                return translate_mediafile_key

            else:
                return response
    except:
        return None

if __name__ == '__main__':
    
    medifile = 'transcribe_a6cbfb90c3ac47219f3b380fbea344d5_my_custome_job.json'
    
    source_lenguage = 'es'
    target_lenguage = 'en'

    response = translate_from_mediafile(medifile, source_lenguage, target_lenguage, True)

    print(response)

    