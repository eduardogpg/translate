import boto3
import time
import uuid

BUCKET = 'pywombat'

def transcribe_job(mediafile_uri, format='mp4', lenguage='en-US'):
    transcribe = boto3.client('transcribe')

    job = f'transcribe_{uuid.uuid4().hex}_my_custome_job'

    transcribe.start_transcription_job(
        TranscriptionJobName=job,
        Media={
            'MediaFileUri': mediafile_uri
        },
        OutputBucketName=BUCKET,
        MediaFormat=format,
        LanguageCode=lenguage
    )

    print('>>> A new Job will start', job)

    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job)
        if response['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        
        print("Transcribe in progress")
        time.sleep(5)
    
    print('>>> The transcription has finished')
    return response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) )

if __name__ == '__main__':
    
    uri = 'https://pywombat.s3.us-east-2.amazonaws.com/video.mp4'

    response = transcribe_job(uri)
    print(response)