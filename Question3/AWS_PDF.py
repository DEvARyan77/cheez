import json
import boto3
import base64

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'your-s3-bucket-name'
    file_content_base64 = event['body'] 
    file_name = event['file_name'] 
    
    # Decode the base64 file content to binary data
    file_content = base64.b64decode(file_content_base64)
    
    # Uploading file
    try:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        
        # Response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'File {file_name} uploaded successfully!',
                'file_name': file_name
            })
        }
        
    except Exception as e:
        # error handling
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error uploading file',
                'error': str(e)
            })
        }
