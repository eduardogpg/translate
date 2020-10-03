from project import put_file
from project import transcribe
from project import create_subtitle_file
from project import translate_from_mediafile

from project import get_name_medifile
from project import get_bucket_from_mediafile
from project import get_format_from_mediafile

if __name__ == '__main__':
    
    try:
        mediafile_uri = input('Ingresa la URL del vídeo: ')
        lenguage = input('Ingresa el lenguaje del vídeo (Ejemplo: en-US): ')

        lenguage_o = input('Ingrese el idioma original (Ejemplo: en): ')
        lenguage_d = input('Ingrese el idioma destion (Ejemplo: es): ')
        
        bucket = get_bucket_from_mediafile(mediafile_uri)
        name = get_name_medifile(mediafile_uri)
        format = get_format_from_mediafile(mediafile_uri)

        transcribe_path = transcribe(bucket, mediafile_uri, name=name, format=format, lenguage=lenguage)

        translate_from_mediafile(bucket, transcribe_path, source=lenguage_o, target=lenguage_d)

        subtitle_name = f'subtitle_{name}.srt'
        subtitle_path = create_subtitle_file(bucket, transcribe_path, subtitle_name)

        put_file(bucket, subtitle_name, subtitle_path)

    except Exception as err:
        print(err)