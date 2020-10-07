import json
import logging

SUBTITLE_TEMPLATE = """{line}
{start_time} --> {end_time}
{sentence}\n"""

from .common import read_content
from .common import put_file

def generate_phrase():
    return { 'start_time': None, 'end_time': None, 'words': list() }

def get_time_code(seconds):
    t_hund = int(seconds % 1 * 1000)
    t_seconds = int( seconds )
    t_secs = ((float( t_seconds) / 60) % 1) * 60
    t_mins = int( t_seconds / 60 )
    
    return str( "%02d:%02d:%02d,%03d" % (00, t_mins, int(t_secs), t_hund ))

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
        logging.error("Exception", exc_info=True)

def generate_line(line, sentence, start_time, end_time):
    
    return SUBTITLE_TEMPLATE.format(
        line=line,
        sentence=sentence.strip(),
        start_time=start_time,
        end_time=end_time
    )


def subtitles_from_mediafile(bucket, medifile_key, prefix='subtitle_'):
    line = 0

    subtitle_mediafile_key = medifile_key.replace('translate_', prefix)
    response = generate_subtitles(bucket, medifile_key)
    
    subtitle_mediafile_key = medifile_key.replace('.json', 'srt')
    subtitle_mediafile_key = subtitle_mediafile_key.replace('transcribe_', prefix)

    local_path = f'tmp/{subtitle_mediafile_key}'

    try:

        with open(local_path, 'w') as file:
            for item in response:
                line += 1

                start_time = item['start_time']
                end_time = item['end_time']

                sentence = ' '.join(item['words'])
                sentence = sentence.replace(' ,', ',')
                sentence = sentence.replace(' .', '.')

                sentence = generate_line(line, sentence, start_time, end_time)
                file.write(sentence)

        put_file(bucket, subtitle_mediafile_key, local_path)

        return subtitle_mediafile_key

    except Exception as err:
        logging.error("Exception", exc_info=True)
        return None
