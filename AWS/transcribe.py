import time
import uuid
import boto3

def transcribe(bucket, mediafile_uri, format='mp4', lenguage='en-US'):
    transcribe = boto3.client('transcribe')

    name = mediafile_uri.split('/')[-1].split('.')[0]
    
    job_name = f'transcribe_{uuid.uuid4().hex}_{name}'

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={
            'MediaFileUri': mediafile_uri
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
    
    remote_mediafile_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    return remote_mediafile_uri.split('/')[-1]
