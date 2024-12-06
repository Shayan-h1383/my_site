from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# Association table for likes
likes = db.Table(
    'likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('liked_at', db.DateTime, default=datetime.utcnow) 
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # Store hashed password
    email = db.Column(db.String(120), unique=False, nullable=False)
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    liked_books = db.relationship(
        'Book', secondary=likes, back_populates='liked_by'
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    reviews = db.relationship('Review', backref='book', lazy='dynamic')
    liked_by = db.relationship('User', secondary=likes, back_populates='liked_books')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

