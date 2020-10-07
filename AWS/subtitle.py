import json
import logging

SUBTITLE_TEMPLATE = """{line}
{start_time} --> {end_time}
{sentence}\n\n"""

from .common import read_content
from .common import put_file

from .translate import translate

def generate_phrase():
    return { 'start_time': None, 'end_time': None, 
            'words': list(), 
            'sentence': '' }

def get_time_code(seconds):
    t_hund = int(seconds % 1 * 1000)
    t_seconds = int( seconds )
    t_secs = ((float( t_seconds) / 60) % 1) * 60
    t_mins = int( t_seconds / 60 )
    
    return str( "%02d:%02d:%02d,%03d" % (00, t_mins, int(t_secs), t_hund ))

def generate_subtitles_from_transcribe(bucket, medifile_key, limit=15):
    
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

        for item in phrases:
            sentence = ' '.join(item['words'])
            sentence = sentence.replace(' ,', ',').replace(' .', '.')

            item['sentence'] = sentence
            
        return phrases

    except Exception as err:
        logging.error("Exception", exc_info=True)

def generate_line(line, sentence, start_time, end_time):
    
    return SUBTITLE_TEMPLATE.format(
        line=line,
        sentence=sentence.strip(),
        start_time=start_time,
        end_time=end_time
    )

def generate_line_translated(line, timer, sentence):
    
    return SUBTITLE_TEMPLATE_TRANSLATED.format(
        line=line,
        sentence=sentence.strip(),
        timer=timer
    )

def get_timer(sentence):
    return sentence.split(' --> ')

def generate_subtitles_from_str(bucket, local_path):
    
    sentence = ''
    current_line = 0
    
    current_phrase = generate_phrase()
    phrases = list()

    with open(local_path, 'r') as file:
        for line in file.readlines():
            
            current_line += 1                
            line = line.replace('\n', '')
            
            if current_line == 2:
                start_time, end_time = get_timer(line)

                if current_phrase.get('start_time') is None:
                    current_phrase['start_time'] = start_time
                
                current_phrase['end_time'] = end_time

            elif current_line == 3:

                sentence = sentence + line

                if '.' in line or '?' in line or '!' in line:

                    current_phrase['sentence'] = translate(sentence)['TranslatedText']

                    sentence = ''
                    phrases.append(current_phrase)
                    current_phrase = generate_phrase()

            elif current_line == 4:
                current_line = 0
    
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

def subtitles_from_mediafile(bucket, medifile_key, prefix='subtitle_'):
    
    response = generate_subtitles_from_transcribe(bucket, medifile_key)
    
    subtitle_mediafile_key = medifile_key.replace('.json', '.srt')
    subtitle_mediafile_key = subtitle_mediafile_key.replace('transcribe_', prefix)

    local_path = f'tmp/{subtitle_mediafile_key}'

    generate_subtitle_file(response, local_path)
    put_file(bucket, subtitle_mediafile_key, local_path)

    return subtitle_mediafile_key

def subtitle_from_str_file(bucket, local_path):

    response = generate_subtitles_from_str(bucket, local_path)

    generate_subtitle_file(response, local_path)
