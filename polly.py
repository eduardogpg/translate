import logging

from AWS import polly_voices
from AWS import generate_video
from AWS import generate_audio

from AWS.common import get_bucket
from AWS.common import get_mediafile_key
from AWS.common import get_mediafile_name

logging.basicConfig(level=logging.WARNING, format="%(message)s")

if __name__ == '__main__':
    video_uri = input('Ingresa la URL del vídeo: ')
    str_uri = input('Ingresa la URL del archivo .srt: ')
    voice_id = input('Ingresa la voz polly a utulizar (Ejemplo: Mia) : ')

    video_bucket = get_bucket(video_uri)
    video_key = get_mediafile_key(video_uri)
    video_name = get_mediafile_name(video_uri)

    str_bucket = get_bucket(str_uri)
    str_key = get_mediafile_key(str_uri)
    
    voices = polly_voices(str_bucket, str_key, voice_id)
    video_local_path = generate_video(video_bucket, video_key, video_name, voices)

    generate_audio(video_local_path)

    