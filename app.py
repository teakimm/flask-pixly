import os
import boto3
import json
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from PIL import Image, ExifTags
from werkzeug.utils import secure_filename
from flask_cors import CORS
from models import connect_db, Image, db, SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///pixly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

env = load_dotenv()
connect_db(app)

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
    image_data = request.files.get('image')
    state = request.form.get("state")
    file_type = request.form.get("fileType")
    model = request.form.get("model")
    name = secure_filename(image_data.filename)

    new_image = Image(state=state, file_type=file_type, model=model, name=name)

    print(db.session.add(new_image))
    db.session.commit()

    try:
        s3.upload_fileobj(image_data, BUCKET_NAME, new_image.id, ExtraArgs={
                          'ContentType': image_data.content_type})
        pass
    except Exception as e:
        print(e)
    return {'success': 'uploaded image', 'fileName': name}
