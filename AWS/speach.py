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

def polly_voices(bucket, str_key):
    content = read_content(bucket, str_key)
    content = content.decode()
    
    audio = dict()
    audios = list()

    current_line = 0
    start_time, end_time = None, None

    for line in content.split('\n'):
        
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
    
# def generate_video(bucket, video_key, video_name, voices):
#     videos_local_path = 'tmp/videos/'
#     Path(videos_local_path).mkdir(parents=True, exist_ok=True)

#     videos = list()
#     video_local_path = f'{videos_local_path}{video_name}'
#     video_translate_local_path = f'{videos_local_path}translate_{video_name}.mp4'

#     download_file(bucket, video_key, video_local_path)

#     for item in voices:
#         video = VideoFileClip(video_local_path).subclip(item['start_time'], item['end_time'])
#         video.audio = AudioFileClip(item['voice_local_path'])

#         videos.append(video)
    
#     concatenate_videoclips(videos).write_videofile(video_translate_local_path)
    
    # voice_local_path = video_local_path.replace('.mp4', '.mp3')

    # video = VideoFileClip(video_local_path)
    # video.audio.write_audiofile(voice_local_path)

    # return voice_local_path

    # return video_translate_local_path
