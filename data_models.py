from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    death_of_date = db.Column(db.Date, nullable=True)
    def __repr__(self):
        return f'<Author {self.name}>'
    
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    cover_image_url = db.Column(db.String, nullable=True)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))
    def __repr__(self):
        return f'<Book {self.title}>'