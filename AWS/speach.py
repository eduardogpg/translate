import os
import boto3

from pathlib import Path

from .common import download_file
from .common import read_content
from .common import get_seconds_duration

from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.editor import concatenate_videoclips

SYNTHESIZE_SPEECH = '''aws polly synthesize-speech \
--text-type ssml \
--text '<speak><prosody amazon:max-duration="{duration}s">{sentence}</prosody></speak>' \
--output-format mp3 \
--voice-id {voice_id} \
{voice_local_path}'''

def play_sound(text, voice_id, local_path):
    try:
        client = boto3.client('polly')

        response = client.synthesize_speech(OutputFormat="mp3",
                                            SampleRate="22050",
                                            Text=text,
                                            VoiceId=voice_id)

        with open(local_path, 'wb') as file:
            file.write(response['AudioStream'].read())

        return local_path
    
    except Exception as err:
        print(err)
        return None

def aws_polly(sentence, duration, voice_id, voice_local_path):
    os.system(SYNTHESIZE_SPEECH.format(
        duration=duration,
        sentence=sentence,
        voice_id=voice_id,
        voice_local_path=voice_local_path
    ))

def polly_voices(local_path):
    audio = dict()
    audios = list()

    current_line = 0
    start_time, end_time = None, None

    with open(local_path, 'r') as file:

        for line in file.readlines():
            
            line = str(line).strip()
            current_line += 1

            if current_line == 2:
                
                audio['start_time'], audio['end_time'] =  line.split(' --> ')
                audio['duration'] = get_seconds_duration(audio['start_time'], audio['end_time'])

            elif current_line == 3:
                audio['sentence']  = line

            elif current_line == 4:
                audios.append(audio)
                
                audio = dict()
                current_line = 0
                start_time, end_time = None, None

        return audios

def generate_audio(response, voice_id, speed):
    voices_local_path = 'tmp/voices/'
    Path(voices_local_path).mkdir(parents=True, exist_ok=True)

    for pos, item in enumerate(response):

        local_path = f'{voices_local_path}{pos + 1}.mp3'
        
        if speed:
            aws_polly(item['sentence'], item['duration'], voice_id, local_path)
        else:
            play_sound(item['sentence'], voice_id, local_path)
