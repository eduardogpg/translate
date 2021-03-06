import logging

from datetime import datetime

from AWS import subtitles
from AWS import transcribe

from AWS import get_bucket
from AWS import get_mediafile_name
from AWS import get_mediafile_format

logging.basicConfig(level=logging.WARNING, format="%(message)s")

if __name__ == '__main__':
    
    video_uri = input('Ingresa la URL del vídeo: ').strip()
    lenguage = input('Ingresa el lenguaje del vídeo (Ejemplo: en-US): ').strip()

    source = input('Ingrese el idioma original (Ejemplo: en): ').strip()
    target = input('Ingrese el idioma destion (Ejemplo: es): ').strip()
    
    bucket = get_bucket(video_uri)
    video_name = get_mediafile_name(video_uri)
    video_format = get_mediafile_format(video_uri)

    logging.warning('\n>>> Generando transcribe.')
    transcribe_key = transcribe(bucket, video_uri, video_name, 
                                            format=video_format,
                                            lenguage=lenguage)
    logging.warning('>>> Transcribe generado.')
    
    logging.warning('\n>>> Generando subtitulos.')
    subtitles(bucket, transcribe_key, video_name, source, target)
    logging.warning('>>> Subtitulos generados.')
