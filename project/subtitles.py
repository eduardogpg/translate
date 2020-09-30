import json
from mutagen.mp3 import MP3

SUBTITLE_TEMPLATE = """{line}
{start_time} --> {end_time}
{sentence}\n"""

from .common import read_content

def generate_phrase():
    return {
        'start_time': None,
        'end_time': None,
        'words': list()
    }

def get_time_code(seconds):
    t_hund = int(seconds % 1 * 1000)
    t_seconds = int( seconds )
    t_secs = ((float( t_seconds) / 60) % 1) * 60
    t_mins = int( t_seconds / 60 )
    
    return str( "%02d:%02d:%02d,%03d" % (00, t_mins, int(t_secs), t_hund ))

def generate_subtitles(bucket, medifile_key):
    try:
        content = read_content(bucket, medifile_key)
        content = json.loads(content)

        items = content['results']['items']

        phrases = list()
        new_phrase = True
        phrase = generate_phrase()

        for item in items:
            
            if new_phrase:
                if item['type'] == 'pronunciation':
                    phrase['start_time'] = get_time_code(float(item['start_time']))
                    new_phrase = False
                
            else:
                if item['type'] == 'pronunciation':
                    phrase['end_time'] = get_time_code(float(item['end_time']))

            phrase['words'].append(
                item['alternatives'][0]['content']
            )

            if len(phrase['words']) == 10:
                new_phrase = True
                phrases.append(phrase)
                phrase = generate_phrase()

        return phrases

    except Exception as err:
        print(err)

def get_duration_from_mp3_file(local_path):
    audio = MP3(local_path)

    return audio.info.length

def get_seconds_from_translation(text, target, file_name, local_path='temp/voices.mp3'):
    client = boto3.client('polly')

    response = client.synthesize_speech(OutputFormat="mp3",
                                        SampleRate="22050",
                                        Text=text,
                                        VoiceId='Amy')


    body = response['AudioStream'].read()
    
    with open(local_path, 'wb') as file:
        file.write(body)

    duration = get_duration_from_mp3_file(local_path)
    
def generate_translated_subtitles(bucket, medifile_key):
    try:
        seconds = 0
        phrases = list()
        new_phrase = True
        phrase = generate_phrase()

        translation = read_content(bucket, medifile_key)
        words = str(translation).split(' ')
        

    except Exception as err:
        print(err)

def generate_line(line, sentence, start_time, end_time):
    
    return SUBTITLE_TEMPLATE.format(
        line=line,
        sentence=sentence.strip(),
        start_time=start_time,
        end_time=end_time
    )

def create_subtitle_file(bucket, medifile_key):
    response = generate_subtitles(bucket, medifile_key)

    line = 0
    
    try:
        print('>>> Generando subtitulos')

        file_path = 'subtitle.srt'
        with open(file_path, 'w') as file:
            for item in response:
                
                start_time = item['start_time']
                end_time = item['end_time']

                sentence = ''
                
                for word in item['words']:
                    div = '' if word in ['.', ',', '!', '?'] else ' '
                    sentence = sentence + div + word

                line += 1

                new_sentence = generate_line(line, sentence, start_time, end_time)
                file.write(new_sentence + '\n')
        
        print(f'>>> Subtitulos generados: {file_path}')
        return file_path
        
    except Exception as err:
        print(err)