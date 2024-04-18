import os
import boto3
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from models import connect_db, Image, db

app = Flask(__name__)
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

    searchTerm = request.args.get('searchTerm')
    category = request.args.get('category')
    if searchTerm and category:
        images = Image.query.filter(
            Image.__table__.c[category].ilike(f'%{searchTerm}%')
        ).all()
    else:
        images = Image.query.all()

    imageData = []
    try:
        for image in images:
            url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{image.id}.{image.file_type}"
            imageData.append({
                'url': url,
                'id': image.id,
                'name': image.name,
                'location': image.location,
                'model': image.model
            })
    except Exception as e:
        print(e)
    response = jsonify({
        'imageData': imageData
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.post("/images")
def upload_images():
    """Upload image to cloud server."""
    image_data = request.files.get('image') or None
    location = request.form.get("location") or None
    file_type = request.form.get("fileType") or None
    model = request.form.get("model") or None
    name = request.form.get('name')

    new_image = Image(location=location, file_type=file_type, model=model, name=name)

    db.session.add(new_image)
    db.session.commit()

    try:
        s3.upload_fileobj(image_data,
                          BUCKET_NAME, f"{str(new_image.id)}.{file_type}",
                          ExtraArgs={
                              'ContentType': image_data.content_type
                          })
        pass
    except Exception as e:
        print(e)
    return {'success': 'uploaded image', 'fileName': str(new_image.id)}
