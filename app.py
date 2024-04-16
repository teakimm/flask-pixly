import os
import boto3
from flask import Flask, jsonify
from dotenv import load_dotenv

env = load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get('aws_access_key_id'),
    aws_secret_access_key=os.environ.get('aws_secret_access_key')
)

BUCKET_NAME = os.environ.get("aws_bucket_name")


@app.get("/images")
def get_all_images():
    public_urls = []
    try:
        for item in s3.list_objects(Bucket=BUCKET_NAME)['Contents']:
            presigned_url = s3.generate_presigned_url(
                'get_object', Params={'Bucket': BUCKET_NAME, 'Key': item['Key']}, ExpiresIn=100)
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    return public_urls
