from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Image(db.Model):
    __tablename__ = "images"

    name = db.Column(
        db.Text,
        nullable=False,
        default=''
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    file_type = db.Column(
        db.Text
    )

    location = db.Column(
        db.String(13),
        default=''
    )

    model = db.Column(
        db.Text,
        default=''
    )

    uploaded_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)
