def read_content(bucket, mediafile_key):
    """
    Lee el contenido de un archivo remoto sin descargarlo
    """
    try:
        import boto3
        
        s3 = boto3.client('s3')
        data = s3.get_object(Bucket=bucket, Key=mediafile_key)

        contents = data['Body'].read()
        return contents

    except:
        return None

def download_file(bucket, mediafile_key, local_path):
    try:
        import boto3

        s3 = boto3.client('s3')
        with open(local_path, 'wb') as file:
            s3.download_fileobj(bucket, mediafile_key, file)

    except:
        return None

def put_file(bucket, mediafile_key, local_path):
    try:
        import boto3
        
        s3 = boto3.cliente('s3')
        s3.upload_file(local_path, bucket, mediafile_key)
        return True

    except:
        return None

def delete_file(bucket, mediafile_key):
    try:
        import boto3

        client = boto3.client('s3')
        client.delete_object(bucket, mediafile_key)
        return True
    except:
        return None
