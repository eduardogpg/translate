import boto3
from mutagen.mp3 import MP3
from datetime import datetime, timedelta

def play_sound(text):
    client = boto3.client('polly')

    response = client.synthesize_speech(OutputFormat="mp3",
                                        SampleRate="22050",
                                        Text=text,
                                        VoiceId='Mia')

    body = response['AudioStream'].read()

    local_path = 'tmp/voices.mp3'
    
    with open(local_path, 'wb') as file:
        file.write(body)

    return local_path

def get_duration_from_audio(local_path):
    audio = MP3(local_path)
    return audio.info.length - 0.6

def add_duration_audio_to_time(time, local_path):
    duration = get_duration_from_audio(local_path)
    
    time = datetime.strptime(time, '%H:%M:%S.%f')
    time = time + timedelta(seconds=duration)
    
    return time.time()

"""
[Nicole, Kevin, Enrique, Tatyana, Russell, Lotte, Geraint, Carmen, Mads, Penelope, Mia, Joanna, Matthew, Brian, Seoyeon, Ruben, Ricardo, Maxim, Lea, Giorgio, Carla, Naja, Maja, Astrid, Ivy, Kimberly, Chantal, Amy, Vicki, Marlene, Ewa, Conchita, Camila, Karl, Zeina, Miguel, Mathieu, Justin, Lucia, Jacek, Bianca, Takumi, Ines, Gwyneth, Cristiano, Mizuki, Celine, Zhiyu, Jan, Liv, Joey, Raveena, Filiz, Dora, Salli, Aditi, Vitoria, Emma, Lupe, Hans, Kendra]
"""