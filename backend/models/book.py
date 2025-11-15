from models.database import db

class Book:
    @staticmethod
    def create(isbn, title, author, category, total_copies=1, **kwargs):
        """Create a new book"""
        query = """
            INSERT INTO books
            (isbn, title, author, publisher, publication_year, category,
             total_copies, available_copies, shelf_location, description, cover_image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            isbn, title, author,
            kwargs.get('publisher'),
            kwargs.get('publication_year'),
            category,
            total_copies,
            total_copies,  # available_copies = total_copies initially
            kwargs.get('shelf_location'),
            kwargs.get('description'),
            kwargs.get('cover_image')
        )

        return db.execute_query(query, params)

    @staticmethod
    def get_by_id(book_id):
        """Get book by ID"""
        query = "SELECT * FROM books WHERE book_id = ?"
        return db.execute_query(query, (book_id,), fetch_one=True)

    @staticmethod
    def get_by_isbn(isbn):
        """Get book by ISBN"""
        query = "SELECT * FROM books WHERE isbn = ?"
        return db.execute_query(query, (isbn,), fetch_one=True)

    @staticmethod
    def get_all(category=None, available_only=False):
        """Get all books"""
        query = "SELECT * FROM books"
        conditions = []
        params = []

        if category:
            conditions.append("category = ?")
            params.append(category)

        if available_only:
            conditions.append("available_copies > 0")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY title"

        return db.execute_query(query, tuple(params), fetch_all=True)

    @staticmethod
    def search(keyword):
        """Search books by title, author, or ISBN"""
        query = """
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
            ORDER BY title
        """
        pattern = f"%{keyword}%"
        return db.execute_query(query, (pattern, pattern, pattern), fetch_all=True)

    @staticmethod
    def update(book_id, **kwargs):
        """Update book information"""
        allowed_fields = ['title', 'author', 'publisher', 'publication_year',
                         'category', 'total_copies', 'shelf_location',
                         'description', 'cover_image']

        updates = []
        params = []

        for field in allowed_fields:
            if field in kwargs:
                updates.append(f"{field} = ?")
                params.append(kwargs[field])

        if not updates:
            return False

        params.append(book_id)
        query = f"UPDATE books SET {', '.join(updates)} WHERE book_id = ?"

        db.execute_query(query, tuple(params))
        return True

    @staticmethod
    def delete(book_id):
        """Delete book (only if not issued)"""
        # Check if book is currently issued
        check_query = """
            SELECT COUNT(*) as count FROM transactions
            WHERE book_id = ? AND status = 'issued'
        """
        result = db.execute_query(check_query, (book_id,), fetch_one=True)

        if result['count'] > 0:
            return False, "Cannot delete book that is currently issued"

        query = "DELETE FROM books WHERE book_id = ?"
        db.execute_query(query, (book_id,))
        return True, "Book deleted successfully"

    @staticmethod
    def is_available(book_id):
        """Check if book is available"""
        book = Book.get_by_id(book_id)
        return book and book['available_copies'] > 0

    @staticmethod
    def get_categories():
        """Get all unique categories"""
        query = "SELECT DISTINCT category FROM books ORDER BY category"
        return db.execute_query(query, fetch_all=True)
