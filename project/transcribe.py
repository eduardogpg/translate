import boto3
import time
import uuid

def transcribe(bucket, mediafile_uri, name='', prefix='transcribe_', format='mp4', lenguage='en-US'):
    transcribe = boto3.client('transcribe')

    job = f'{prefix}{uuid.uuid4().hex}_{name}'

    transcribe.start_transcription_job(
        TranscriptionJobName=job,
        Media={
            'MediaFileUri': mediafile_uri
        },
        OutputBucketName=bucket,
        MediaFormat=format,
        LanguageCode=lenguage
    )

    print('>>> Comenzando transcripción')

    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job)
        if response['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        
        print("Transcripción en progreso...")
        time.sleep(10)
    
    print('>>> Transcripción finalizada')
    
    remote_mediafile_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    job = remote_mediafile_uri.split('/')[-1]

    return job

