import time
import uuid
import boto3

def transcribe(bucket, video_uri, name, format='mp4', lenguage='en-US'):
    transcribe = boto3.client('transcribe')
    
    job_name = f'transcribe_{uuid.uuid4().hex}_{name}'

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={
            'MediaFileUri': video_uri
        },
        OutputBucketName=bucket,
        MediaFormat=format,
        LanguageCode=lenguage
    )

    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if response['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        
        time.sleep(10)
    
    transcribe_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    return transcribe_uri.split('/')[-1]
