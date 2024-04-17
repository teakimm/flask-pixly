from app import app
from models import db, Image

db.drop_all()
db.create_all()