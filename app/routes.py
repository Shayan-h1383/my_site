from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Book, User, Review
from . import db
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import RegistrationForm

bp = Blueprint('main', __name__)

# Homepage: Already implemented
@bp.route('/')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books, user=current_user)

@bp.route('/unlike/<int:book_id>', methods=['POST'])
@login_required
def unlike_book(book_id):
    book = Book.query.get(book_id)
    if book in current_user.liked_books:
        current_user.liked_books.remove(book)
        db.session.commit()
        flash(f'You unliked "{book.title}".', 'success')
    else:
        flash('This book is not in your liked books.', 'warning')
    return redirect(url_for('main.your_reviews'))

@bp.route('/your_reviews')
@login_required
def your_reviews():
    # Fetch liked books
    liked_books = current_user.liked_books

    # Fetch reviews written by the user
    reviews = (
        Review.query.join(Book)
        .filter(Review.user_id == current_user.id)
        .add_columns(Book.title)
        .all()
    )

    return render_template(
        'your_reviews.html',
        liked_books=liked_books,
        reviews=reviews,
    )
    
# Login Page
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(request.args.get('next') or url_for('main.home'))
        else:
            flash('Invalid username or password.', 'login_error')  # Specify category for login errors

    return render_template('login.html')

# Logout Page
@bp.route('/logout')
@login_required
def logout():
    logout_user()  # Use logout_user from Flask-Login
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.home'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            # Handle registration logic (e.g., save user, hash password)
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                flash('Username already exists.', 'danger')
                return redirect(url_for('main.register'))

            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(request.args.get('next') or url_for('main.home'))
        return redirect(url_for('success')) 
    return render_template('register.html', form=form)
    
@bp.route('/account_details', methods=['GET', 'POST'])
@login_required
def account_details():
    if request.method == 'POST':
        # Delete the account
        db.session.delete(current_user)
        db.session.commit()
        return redirect(url_for('auth.login'))  # Redirect to the login page after deletion
    return render_template('account_details.html')

@bp.route('/book_review/<int:book_id>', methods=['GET', 'POST'])
def book_review(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You must be logged in to add a review or like a book.', 'danger')
            return redirect(url_for('main.login'))

        # Handle adding a review
        if 'review' in request.form:
            content = request.form.get('review')
            if content.strip():  # Ensure content is not empty or just spaces
                review = Review(content=content, user_id=current_user.id, book_id=book_id)
                db.session.add(review)
                db.session.commit()
                flash('Review added successfully!', 'success')
                return redirect(url_for('main.book_review', book_id=book_id))
            else:
                flash('Review cannot be empty.', 'danger')

    return render_template('book_review.html', book=book, reviews=reviews, user=current_user)


@bp.route('/like/<int:book_id>', methods=['POST'])
def like_book(book_id):
    book = Book.query.get_or_404(book_id)

    if not current_user.is_authenticated:
        return jsonify({'error': 'You must be logged in to like or unlike a book.'}), 403

    # Handle liking the book
    if book not in current_user.liked_books:
        current_user.liked_books.append(book)
        db.session.commit()
        liked = True
    else:
        current_user.liked_books.remove(book)
        db.session.commit()
        liked = False

    # Return updated like status and count
    likes_count = len(book.liked_by)
    return jsonify({'liked': liked, 'likes_count': likes_count})


