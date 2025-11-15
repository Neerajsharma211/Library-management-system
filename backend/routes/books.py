from flask import Blueprint, request, jsonify
from models.book import Book
from middleware.auth_middleware import token_required, role_required
from utils.validators import Validator

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
@token_required
def get_books(current_user_id, current_user_role):
    """Get all books"""
    category = request.args.get('category')
    available_only = request.args.get('available_only', 'false').lower() == 'true'

    books = Book.get_all(category=category, available_only=available_only)

    return jsonify({
        'books': books,
        'count': len(books)
    }), 200

@books_bp.route('/<int:book_id>', methods=['GET'])
@token_required
def get_book(book_id, current_user_id, current_user_role):
    """Get a specific book"""
    book = Book.get_by_id(book_id)

    if not book:
        return jsonify({'error': 'Book not found'}), 404

    return jsonify({'book': book}), 200

@books_bp.route('/search', methods=['GET'])
@token_required
def search_books(current_user_id, current_user_role):
    """Search books"""
    keyword = request.args.get('q', '')

    if not keyword:
        return jsonify({'error': 'Search keyword required'}), 400

    books = Book.search(keyword)

    return jsonify({
        'books': books,
        'count': len(books)
    }), 200

@books_bp.route('/', methods=['POST'])
@token_required
@role_required('admin', 'librarian')
def create_book(current_user_id, current_user_role):
    """Create a new book"""
    data = request.get_json()

    # Validate required fields
    required = ['isbn', 'title', 'author', 'category']
    for field in required:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Validate ISBN
    valid, error = Validator.validate_isbn(data['isbn'])
    if not valid:
        return jsonify({'error': error}), 400

    # Check if ISBN already exists
    if Book.get_by_isbn(data['isbn']):
        return jsonify({'error': 'Book with this ISBN already exists'}), 409

    try:
        book_id = Book.create(
            isbn=data['isbn'],
            title=data['title'],
            author=data['author'],
            category=data['category'],
            total_copies=data.get('total_copies', 1),
            publisher=data.get('publisher'),
            publication_year=data.get('publication_year'),
            shelf_location=data.get('shelf_location'),
            description=data.get('description'),
            cover_image=data.get('cover_image')
        )

        return jsonify({
            'message': 'Book created successfully',
            'book_id': book_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['PUT'])
@token_required
@role_required('admin', 'librarian')
def update_book(book_id, current_user_id, current_user_role):
    """Update a book"""
    data = request.get_json()

    if not Book.get_by_id(book_id):
        return jsonify({'error': 'Book not found'}), 404

    try:
        Book.update(book_id, **data)
        return jsonify({'message': 'Book updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_book(book_id, current_user_id, current_user_role):
    """Delete a book"""
    success, message = Book.delete(book_id)

    if not success:
        return jsonify({'error': message}), 400

    return jsonify({'message': message}), 200

@books_bp.route('/categories', methods=['GET'])
@token_required
def get_categories(current_user_id, current_user_role):
    """Get all book categories"""
    categories = Book.get_categories()
    return jsonify({'categories': categories}), 200
