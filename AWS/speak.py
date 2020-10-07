from mutagen.mp3 import MP3


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