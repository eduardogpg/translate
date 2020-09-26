def read_content(bucket, mediafile_key):
    try:
        import boto3
        
        s3 = boto3.client('s3')
        data = s3.get_object(Bucket=bucket, Key=mediafile_key)

        content = data['Body'].read()
        return content

    except Exception as err:
        print(err)
        return None

def download_file(bucket, mediafile_key, local_path):
    try:
        import boto3

        s3 = boto3.client('s3')
        with open(local_path, 'wb') as file:
            s3.download_fileobj(bucket, mediafile_key, file)

    except Exception as err:
        print(err)
        return None

def put_file(bucket, mediafile_key, local_path):
    try:
        import boto3
        
        s3 = boto3.client('s3')
        s3.upload_file(local_path, bucket, mediafile_key)
        return True

    except Exception as err:
        print(err)
        return None

def delete_file(bucket, mediafile_key):
    try:
        import boto3

        client = boto3.client('s3')
        return client.delete_object(Bucket=bucket, Key=mediafile_key)
        
    except Exception as err:
        print(err)
        return None
