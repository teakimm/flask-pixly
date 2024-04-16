import os
import boto3
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from PIL import Image, ExifTags
from werkzeug.utils import secure_filename

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
    """Get all image urls."""

    public_urls = []
    try:
        for item in s3.list_objects(Bucket=BUCKET_NAME)['Contents']:
            url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{item['Key']}"
            public_urls.append(url)
    except Exception as e:
        print(e)
    return public_urls


@app.post("/images")
def upload_images():
    """Upload image to cloud server."""

    image_data = request.files['image']
    file_name = secure_filename(image_data.filename)

    try:
        s3.upload_fileobj(image_data, BUCKET_NAME, file_name, ExtraArgs={
                          'ContentType': image_data.content_type})
        pass
    except Exception as e:
        print(e)
    return {'success': 'uploaded image', 'fileName': file_name}
