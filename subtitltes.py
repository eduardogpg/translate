import json

BUCKET = 'pywombat'
SUBTITLE_TEMPLATE = """{line}
{start_time} --> {end_time}
{sentence}\n"""

from common import read_content

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

def generate_subtitles(medifile_key):
    content = read_content(BUCKET, medifile_key)
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

def generate_line(line, sentence, start_time, end_time):
    return SUBTITLE_TEMPLATE.format(
        line=line,
        sentence=sentence,
        start_time=start_time,
        end_time=end_time
    )

def create_subtitle_file(medifile):
    response = generate_subtitles(medifile)

    line = 0
    
    with open('temp/subtitle.srt', 'w') as file:
        for item in response:
            
            start_time = item['start_time']
            end_time = item['end_time']
            sentence = ' '.join(item['words'])
            line += 1

            new_sentence = generate_line(line, sentence, start_time, end_time)
            file.write(new_sentence + '\n')

if __name__ == '__main__':
    medifile = 'transcribe_a6cbfb90c3ac47219f3b380fbea344d5_my_custome_job.json'
    create_subtitle_file(medifile)