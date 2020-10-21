import logging

from AWS import polly_voices
from AWS import generate_audio

from AWS.common import get_bucket
from AWS.common import get_mediafile_key
from AWS.common import get_mediafile_name

logging.basicConfig(level=logging.WARNING, format="%(message)s")

if __name__ == '__main__':
    str_uri = input('Ingresa la URL del archivo .srt: ').strip()
    source = input('Idioma del archivo original: ')
    voice_id = input('Voz polly (Ejemplo: Mia): ')
    speed = input('Aplicar ducación máxma (si/no): ').lower() == 'si'

    bucket = get_bucket(str_uri)
    str_key = get_mediafile_key(str_uri)
    
    logging.warning('\n>>> Obteniendo archivo .srt')
    voices = polly_voices(bucket, str_key)
    
    logging.warning('\n>>> Generando archivo mp3`s')
    generate_audio(voices, voice_id, speed)
    logging.warning('\n>>> Archivos mp3`s. generados de forma exitosa.')
