from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Image(db.model):
    __tablename__ = "images"

    name = db.Column(
        db.Text,
        nullable=False
    )

    id = db.Column(
        db.Text,
        primary_key=True,
        autoincrement=True
    )

    file_type = db.Column(
        db.Text
    )

    file_type = db.Column(
        db.Text
    )
