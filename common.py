def read_content(bucket, mediafile_key):
    try:
        import boto3
        
        s3 = boto3.client('s3')
        data = s3.get_object(Bucket=bucket, Key=mediafile_key)

        contents = data['Body'].read()
        return contents

    except:
        return None

def put_file(bucket, mediafile_key, local_path):
    try:
        import boto3
        
        s3 = boto3.resource('s3')

        s3.meta.client.upload_file(local_path, bucket, mediafile_key)

    except:
        return None        