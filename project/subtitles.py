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

def get_milliseconds(seconds):
    return float(seconds.split(':')[-1].replace(',', '.'))

def seconds_to_float(seconds):
    return float(seconds.split(':')[-1].replace(',', '.'))

def generate_subtitles(bucket, medifile_key, limit=15):
    
    try:
        content = read_content(bucket, medifile_key)
        content = json.loads(content)

        items = content['results']['items']

        phrases = list()
        new_phrase = True
        phrase = generate_phrase()

        for item in items:
            
            word = item['alternatives'][0]['content']
            
            if new_phrase:
                
                if item['type'] == 'pronunciation':
                    new_phrase = False
                    
                    phrase['words'].append(word)
                    
                    phrase['start_time'] = get_time_code(float(item['start_time']))
                    phrase['end_time'] = get_time_code(float(item['end_time']))

                elif item['type'] == 'punctuation':
                    new_phrase = True

                    last_phrase = phrases[-1]
                    last_phrase['words'].append(word)
                    phrases[-1] = last_phrase

            else:
                if item['type'] == 'pronunciation':
                    
                    phrase['words'].append(word)
                    phrase['end_time'] = get_time_code(float(item['end_time']))

                elif item['type'] == 'punctuation':
                    
                    if word in ('.', '?', '!'):
                        new_phrase = True
                    
                    phrase['words'].append(word)
            

            if phrase['words'] and ( len(phrase['words']) == limit or new_phrase):
                
                if len(phrase['words']) <= 2:
                    
                    last_phrase = phrases[-1]
                    
                    last_phrase['words'].extend(phrase['words'])
                    last_phrase['end_time'] = phrase['end_time']

                    phrases[-1] = last_phrase

                else:
                    phrases.append(phrase)
                
                new_phrase = True
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
    
def generate_line(line, sentence, start_time, end_time):
    
    return SUBTITLE_TEMPLATE.format(
        line=line,
        sentence=sentence.strip(),
        start_time=start_time,
        end_time=end_time
    )

def create_subtitle_file(bucket, medifile_key, local_path='subtitles.srt'):
    response = generate_subtitles(bucket, medifile_key)

    line = 0
  
    try:
        print('>>> Generando subtitulos')
        
        file_path = local_path
        
        with open(file_path, 'w') as file:
            for item in response:
                line += 1

                start_time = item['start_time']
                end_time = item['end_time']

                sentence = ' '.join(item['words'])

                sentence = sentence.replace(' ,', ',')
                sentence = sentence.replace(' .', '.')

                new_sentence = generate_line(line, sentence, start_time, end_time)
                file.write(new_sentence + '\n')

        print(f'>>> Subtitulos generados: {file_path}')
        return file_path
        
    except Exception as err:
        print(err)
