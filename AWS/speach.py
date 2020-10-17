import boto3

from pathlib import Path

from .common import download_file

from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.editor import concatenate_videoclips

def play_sound(text, local_path, voice='Mia'):
    try:
        client = boto3.client('polly')

        response = client.synthesize_speech(OutputFormat="mp3",
                                            SampleRate="22050",
                                            Text=text,
                                            VoiceId=voice)

        with open(local_path, 'wb') as file:
            file.write(response['AudioStream'].read())

        return local_path
    
    except Exception as err:
        print(err)
        return None

def generate_polly_voices(srtfile_path, voice='Mia'):
    audio_id = 0
    audios = list()
    
    current_line = 0
    audio_path, start_time, end_time = None, None, None

    audios_local_path = 'tmp/audios/'
    Path(audios_local_path).mkdir(parents=True, exist_ok=True)

    with open(srtfile_path, 'r') as file:

        for line in file.readlines():
            
            current_line += 1
            line = line.split('\n')[0]

            if current_line == 1:
                audio_id += 1
                audio_path = f'{audios_local_path}{audio_id}.mp3'

            elif current_line == 2:
                start_time, end_time =  line.split(' --> ')

            elif current_line == 3:
                play_sound(line, audio_path, voice)

            else:
                audios.append({
                        'start_time': start_time,
                        'end_time': end_time,
                        'audio_path': audio_path
                    })

                current_line = 0
                audio_path, start_time, end_time = None, None, None

    return audios

def generate_video_speech(bucket, mediafile_key, voices):

    videos_local_path = 'tmp/videos/'
    Path(videos_local_path).mkdir(parents=True, exist_ok=True)

    videos = list()
    video_path = f'{videos_local_path}{mediafile_key}'

    download_file(bucket, mediafile_key, video_path)

    for item in voices:

        video = VideoFileClip(video_path).subclip(item['start_time'], item['end_time'])
        video.audio = AudioFileClip(item['audio_path'])

        videos.append(video)
    
    concatenate_videoclips(videos).write_videofile(video_path)
    
