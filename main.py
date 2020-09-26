from transcribe import transcribe
from subtitles import create_subtitle_file

def get_bucket_from_mediafile(mediafile_uri):
    return mediafile_uri.split('//')[1].split('.')[0]

def format_from_mediafile(mediafile_uri):
    return mediafile_uri.split('.')[-1]

if __name__ == '__main__':
    
    try:
        mediafile_uri = input('Ingresa la URL del vídeo: ')
        lenguage = input('Ingresa el lenguaje del vídep (Ejemplo: en-US): ')
        
        bucket = get_bucket_from_mediafile(mediafile_uri)
        format = format_from_mediafile(mediafile_uri)

        #source_lenguage = input('Ingresa el lenguage del vídeo: (es): ')
        #target_lenguage = input('Ingresa el lenguage a traducir: (en): ')

        transcribe_path = transcribe(bucket, mediafile_uri, format, lenguage)

        create_subtitle_file(bucket, transcribe_path)

    except Exception as err:
        print(err)