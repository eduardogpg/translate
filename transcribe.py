import boto3
import time
import uuid

def transcribe(bucket, mediafile_uri, format='mp4', lenguage='en-US'):
    transcribe = boto3.client('transcribe')

    job = f'transcribe_{uuid.uuid4().hex}_my_custome_job'

    transcribe.start_transcription_job(
        TranscriptionJobName=job,
        Media={
            'MediaFileUri': mediafile_uri
        },
        OutputBucketName=bucket,
        MediaFormat=format,
        LanguageCode=lenguage
    )

    print('>>> Comenzando al transcripción')

    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job)
        if response['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        
        print("Transcripción en progreso...")
        time.sleep(5)
    
    print('>>> La transcripción ha finalizado')
    
    remote_mediafile_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    job = remote_mediafile_uri.split('/')[-1]

    return job

