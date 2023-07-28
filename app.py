from flask import Flask, request, render_template, redirect, url_for
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\evanj\OneDrive\Desktop\Masterschool Bootcamp\Book_Alchemy\data\library.sqlite'
db.init_app(app)

#Create Tables Once
with app.app_context():
    db.create_all() 
    #already created the tables, so commented out

@app.route('/home')
def home():
    # Get sort_by parameter from the query string
    sort_by = request.args.get('sort_by', 'title') #default sort by title/choose appropriate sorting method
    search = request.args.get('search', '')
    if sort_by == 'title':
        # Query all books sorted by title
        books = Book.query.filter(Book.title.like(f"%{search}%")).order_by(Book.title).all()
    elif sort_by == 'author':
        # Query all books sorted by author
        books = Book.query.join(Author).filter(Author.name.like(f"%{search}%")).order_by(Author.name).all()
    else:
    # Query all books from the database
        books = Book.query.order_by(Book.title).all()
    # Render the home template with the list of books
    return render_template('home.html', books=books)

@app.route('/')
#redirect to homepage
def index():
    return redirect(url_for('home'))

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
        date_of_death = request.form['date_of_death']
        if date_of_death:  # If this field is not empty
            date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d')
        else:
            date_of_death = None
        # Create a new Author object
        new_author = Author(name=name, birth_date=birthdate, death_of_date=date_of_death)
        # Add new_author to the database
        db.session.add(new_author)
        db.session.commit()
        # Render the form again with a success message
        return render_template('add_author.html', message='Author added successfully!')
    # If the request method is GET, just render the form
    return render_template('add_author.html')


import requests

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get data from the form
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = int(request.form['publication_year'])
        author_id = int(request.form['author_id'])
        # Fetch the book details from the Open Library Books API
        response = requests.get(f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data')
        data = response.json()
        cover_image_url = data[f'ISBN:{isbn}']['cover']['medium']
        # Create a new Book object
        new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id, cover_image_url=cover_image_url)
        # Add new_book to the database
        db.session.add(new_book)
        db.session.commit()
        # Get all authors for the dropdown list
        authors = Author.query.all()
        # Render the form again with a success message
        return render_template('add_book.html', message='Book added successfully!', authors=authors)
    # If the request method is GET
    authors = Author.query.all()
    # Just render the form with the list of authors
    return render_template('add_book.html', authors=authors)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    #Query the book
    book = Book.query.get(book_id)
    #check if author has other books
    author = Author.query.get(book.author_id)
    if len(author.books) <= 1:
        #delete author
        db.session.delete(author)
    #delete book
    db.session.delete(book)
    db.session.commit()
    #redirect to homepage
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)