import logging

from AWS import subtitles
from AWS import transcribe

from AWS import get_mediafile_key
from AWS import get_bucket_from_mediafile
from AWS import get_format_from_mediafile

from AWS import generate_polly_voices
from AWS import generate_video_speech

logging.basicConfig(level=logging.WARNING, format="%(message)s")

if __name__ == '__main__':
    
    try:
        mediafile_uri = input('Ingresa la URL del vídeo: ')
        lenguage = input('Ingresa el lenguaje del vídeo (Ejemplo: en-US): ')

        source = input('Ingrese el idioma original (Ejemplo: en): ')
        target = input('Ingrese el idioma destion (Ejemplo: es): ')
        
        mediafile_key = get_mediafile_key(mediafile_uri)
        bucket = get_bucket_from_mediafile(mediafile_uri)
        format = get_format_from_mediafile(mediafile_uri)

        logging.warning('>>> Generando transcribe.')
        transcribe_mediafile_key = transcribe(
            bucket, mediafile_uri, format=format,
            lenguage=lenguage,
        )
        logging.warning('>>> Transcribe generado.')
        
        logging.warning('>>> Generando Subtitulos.')
        _, srtfile_path = subtitles(
            bucket, transcribe_mediafile_key,
            source, target
        )
        logging.warning('>>> Subtitulos generados.')

        # logging.warning('>>> Generando aúdio.')
        # voices = generate_polly_voices(srtfile_path)
        # generate_video_speech(bucket, mediafile_key, voices)
        # logging.warning('>>> Aúdio generados.')

    except Exception as err:
        print(err)