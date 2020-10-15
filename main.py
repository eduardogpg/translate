import logging

from AWS import subtitles
from AWS import transcribe

from AWS import get_bucket_from_mediafile
from AWS import get_format_from_mediafile

logging.basicConfig(level=logging.WARNING, format="%(message)s")

if __name__ == '__main__':
    
    try:
        mediafile_uri = input('Ingresa la URL del vídeo: ')
        lenguage = input('Ingresa el lenguaje del vídeo (Ejemplo: en-US): ')

        source = input('Ingrese el idioma original (Ejemplo: en): ')
        target = input('Ingrese el idioma destion (Ejemplo: es): ')
        
        bucket = get_bucket_from_mediafile(mediafile_uri)
        format = get_format_from_mediafile(mediafile_uri)

        logging.warning('>>> Generando transcribe.')
        transcribe_mediafile_key = transcribe(
            bucket, mediafile_uri, format=format,
            lenguage=lenguage,
        )
        logging.warning('>>> Transcribe generado.')
        
        logging.warning('>>> Generando Subtitulos.')
        subtitle_mediafile_key = subtitles(
            bucket, transcribe_mediafile_key,
            source, target
        )
        logging.warning('>>> Subtitulos generados.')

    except Exception as err:
        print(err)