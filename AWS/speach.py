import boto3

client = boto3.client('polly')

def play_sound(text):
    response = client.synthesize_speech(OutputFormat="mp3",
                                        SampleRate="22050",
                                        Text=text,
                                        VoiceId='Amy')

    body = response['AudioStream'].read()

    print(response)

    with open('temp/voices.mp3', 'wb') as file:
        file.write(body)
    
if __name__ == '__main__':
    play_sound(
        'Hello World, this a simple tess, sound test number 2'
    )

def getSecondsFromTranslation( textToTranslate, targetLangCode, audioFileName ):

    # Set up the Amazon Polly and Amazon Translate services
    client = boto3.client('polly')
    translate = boto3.client(service_name='translate', region_name="us-east-1", use_ssl=True)
    
    # Use the translated text to create the synthesized speech
    response = client.synthesize_speech( OutputFormat="mp3", SampleRate="22050", Text=textToTranslate, VoiceId=getVoiceId( targetLangCode ) )
    
    # Write the stream out to disk so that we can load it into an AudioClip
    writeAudioStream( response, audioFileName )
    
    # Load the temporary audio clip into an AudioFileClip
    audio = AudioFileClip( audioFileName)
        
    # return the duration    
    return audio.duration