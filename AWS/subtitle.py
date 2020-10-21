import json
import logging

from pathlib import Path
from datetime import datetime
from datetime import timedelta

from .common import put_file
from .common import read_content
from .common import get_seconds_duration

from .translate import translate

SUBTITLE_TEMPLATE = """{line}
{start_time} --> {end_time}
{sentence}\n\n"""

PUNCTUATION_MARKS = ('.', '?', '!')
MAX_WORDS = 15

def generate_phrase():
    return { 
            'start_time': None,
            'end_time': None, 
            'words': list(), 
            'sentence': '' 
        }

def get_time_code(seconds):
    t_hund = int(seconds % 1 * 1000)
    t_seconds = int( seconds )
    t_secs = ((float( t_seconds) / 60) % 1) * 60
    t_mins = int( t_seconds / 60 )
    
    return str( "%02d:%02d:%02d.%03d" % (00, t_mins, int(t_secs), t_hund ))

def generate_line(line, sentence, start_time, end_time):
    return SUBTITLE_TEMPLATE.format(
        line=line,
        sentence=sentence.strip(),
        start_time=start_time,
        end_time=end_time
    )

def subtitles_from_transcribe(bucket, transcribe_key):

    content = read_content(bucket, transcribe_key)
    content = json.loads(content)

    phrases = list()
    new_phrase = True
    phrase = generate_phrase()

    for item in content['results']['items']:
        
        word = item['alternatives'][0]['content']
        phrase['words'].append(word)

        if new_phrase:
            if item['type'] == 'pronunciation':
                new_phrase = False
                
                phrase['start_time'] = get_time_code(float(item['start_time']))
                phrase['end_time'] = get_time_code(float(item['end_time']))

            elif item['type'] == 'punctuation':
                
                phrase['words'].pop()
                phrases[-1]['words'].append(word)
        
        else:
            
            if item['type'] == 'pronunciation':
                phrase['end_time'] = get_time_code(float(item['end_time']))

            elif item['type'] == 'punctuation':
                new_phrase = word in PUNCTUATION_MARKS

        if len(phrase['words']) >= MAX_WORDS or new_phrase:

            if len(phrase['words']) <= 2:
                last_phrase = phrases.pop()

                last_phrase['words'].extend(phrase['words'])
                last_phrase['end_time'] = phrase['end_time'] or last_phrase['end_time']

                phrase = last_phrase

            new_phrase = True
            phrases.append(phrase)
            phrase = generate_phrase()

    for phrase in phrases:
        sentence = ' '.join(phrase['words'])
        phrase['sentence'] = sentence.replace(' ,', ',').replace(' .', '.')

    return phrases

def transcribe_subtitles(response, source, target):
    sentence = ''
    phrases = list()
    phrase = generate_phrase()

    for item in response:
        
        if phrase['start_time'] is None:
            phrase['start_time'] = item['start_time']
        
        phrase['end_time'] = item['end_time']
        
        sentence = sentence + item['sentence'] + ' '

        if any(punctuation in sentence for punctuation in PUNCTUATION_MARKS):
            translated = translate(sentence, source, target)

            phrase['sentence'] = translated['TranslatedText']
            
            sentence = ''
            phrases.append(phrase)
            phrase = generate_phrase()

    return phrases

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def divide_phrase(item):
    phrases = list()

    sentence = item['sentence'].split(' ')
    
    start_time = datetime.strptime(item['start_time'], '%H:%M:%S.%f')
    end_time = datetime.strptime(item['end_time'], '%H:%M:%S.%f')
    seconds = get_seconds_duration(item['start_time'], item['end_time']) / len(sentence)

    for words in chunks(sentence, MAX_WORDS):
        end_time = start_time + timedelta(seconds=(seconds * len(words)) + 0.05)

        phrases.append({
                'start_time': start_time.strftime('%H:%M:%S.%f')[:-3],
                'end_time': end_time.strftime('%H:%M:%S.%f')[:-3],
                'sentence': ' '.join(words),
            }
        )
        start_time = end_time
    
    return phrases

def sanitaize_subtitles(response):
    phrases = list()

    for item in response:
        
        if len(item['sentence'].split(' ')) > MAX_WORDS:
            phrases.extend(divide_phrase(item))
        
        else:
            phrases.append(item)
        
    return phrases

def generate_subtitle_file(response, local_path):
    line = 0

    with open(local_path, 'w') as file:
        for item in response:
            line += 1

            start_time = item['start_time']
            end_time = item['end_time']

            sentence = generate_line(line, item['sentence'], start_time, end_time)
            file.write(sentence)

def subtitles(bucket, transcribe_key, str_name, source, target):
    now = datetime.now().strftime('%Y_%m_%d')
    
    subtitles_local_path = f'tmp/subtitles/'
    Path(subtitles_local_path).mkdir(parents=True, exist_ok=True)
    
    subtitle_key =  f'{source}_{str_name}_{now}.srt'
    subtitle_local_path = f'{subtitles_local_path}{subtitle_key}'

    translate_subtitle_key = f'{target}_{str_name}_{now}.srt'
    translate_subtitle_local_path = f'{subtitles_local_path}{translate_subtitle_key}'

    response = subtitles_from_transcribe(bucket, transcribe_key)
    generate_subtitle_file(response, subtitle_local_path)

    response = transcribe_subtitles(response, source, target)
    response = sanitaize_subtitles(response)
    generate_subtitle_file(response, translate_subtitle_local_path)
    
    put_file(bucket, subtitle_key, subtitle_local_path)
    put_file(bucket, translate_subtitle_key, translate_subtitle_local_path)

    return subtitle_key, translate_subtitle_key
