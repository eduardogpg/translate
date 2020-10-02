import boto3

def read_content(bucket, mediafile_key):
    try:
        s3 = boto3.client('s3')
        data = s3.get_object(Bucket=bucket, Key=mediafile_key)

        content = data['Body'].read()
        return content

    except Exception as err:
        print(err)
        return None

def download_file(bucket, mediafile_key, local_path):
    try:
        s3 = boto3.client('s3')
        
        with open(local_path, 'wb') as file:
            s3.download_fileobj(bucket, mediafile_key, file)

        return local_path

    except Exception as err:
        print(err)
        return None

def put_file(bucket, mediafile_key, local_path):
    try:
        s3 = boto3.client('s3')
        s3.upload_file(local_path, bucket, mediafile_key)
        
        return True

    except Exception as err:
        print(err)
        return None

def put_object(bucket, mediafile_key, content):
    try:
        s3 = boto3.client('s3')
        
        s3.put_object(Bucket=bucket, Key=mediafile_key, Body=content)
        
        return True

    except Exception as err:
        print(err)
        return None

def get_bucket_from_mediafile(mediafile_uri):
    return mediafile_uri.split('//')[1].split('.')[0]

def get_format_from_mediafile(mediafile_uri):
    return mediafile_uri.split('.')[-1]

def get_name_medifile(mediafile_uri):
    mediafile = mediafile_uri.split('/')[-1]
    return mediafile.split('.')[0]
