from datetime import datetime, timedelta
from models.database import db
from config import Config

class Transaction:
    @staticmethod
    def issue_book(book_id, user_id, librarian_id, issue_days=None):
        """Issue a book to a user"""
        if issue_days is None:
            issue_days = Config.DEFAULT_ISSUE_DAYS

        # Check if user has reached max books limit
        count_query = """
            SELECT COUNT(*) as count FROM transactions
            WHERE user_id = ? AND status = 'issued'
        """
        result = db.execute_query(count_query, (user_id,), fetch_one=True)

        if result['count'] >= Config.MAX_BOOKS_PER_USER:
            return False, "User has reached maximum book limit"

        # Check if book is available
        book_query = "SELECT available_copies FROM books WHERE book_id = ?"
        book = db.execute_query(book_query, (book_id,), fetch_one=True)

        if not book or book['available_copies'] <= 0:
            return False, "Book is not available"

        # Issue the book
        issue_date = datetime.now().date()
        due_date = issue_date + timedelta(days=issue_days)

        query = """
            INSERT INTO transactions
            (book_id, user_id, librarian_id, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, ?, 'issued')
        """
        params = (book_id, user_id, librarian_id, issue_date, due_date)

        transaction_id = db.execute_query(query, params)
        return True, transaction_id

    @staticmethod
    def return_book(transaction_id, librarian_id):
        """Return a book"""
        # Get transaction details
        trans = Transaction.get_by_id(transaction_id)

        if not trans:
            return False, "Transaction not found"

        if trans['status'] != 'issued':
            return False, "Book is not currently issued"

        return_date = datetime.now().date()

        # Update transaction
        query = """
            UPDATE transactions
            SET status = 'returned', return_date = ?
            WHERE transaction_id = ?
        """
        db.execute_query(query, (return_date, transaction_id))

        # Calculate fine if overdue
        due_date = datetime.strptime(trans['due_date'], '%Y-%m-%d').date()

        if return_date > due_date:
            days_overdue = (return_date - due_date).days
            fine_amount = min(days_overdue * Config.FINE_PER_DAY, Config.MAX_FINE_AMOUNT)

            # Create fine record
            from models.fine import Fine
            Fine.create(transaction_id, trans['user_id'], fine_amount, days_overdue)

            return True, f"Book returned with fine: ${fine_amount:.2f}"

        return True, "Book returned successfully"

    @staticmethod
    def get_by_id(transaction_id):
        """Get transaction by ID"""
        query = """
            SELECT t.*, b.title, b.author, u.full_name as user_name
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            JOIN users u ON t.user_id = u.user_id
            WHERE t.transaction_id = ?
        """
        return db.execute_query(query, (transaction_id,), fetch_one=True)

    @staticmethod
    def get_by_user(user_id, status=None):
        """Get all transactions for a user"""
        query = """
            SELECT t.*, b.title, b.author, b.isbn
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            WHERE t.user_id = ?
        """
        params = [user_id]

        if status:
            query += " AND t.status = ?"
            params.append(status)

        query += " ORDER BY t.issue_date DESC"

        return db.execute_query(query, tuple(params), fetch_all=True)

    @staticmethod
    def get_all(status=None):
        """Get all transactions"""
        query = """
            SELECT t.*, b.title, b.author, u.full_name as user_name, u.email
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            JOIN users u ON t.user_id = u.user_id
        """
        params = []

        if status:
            query += " WHERE t.status = ?"
            params.append(status)

        query += " ORDER BY t.issue_date DESC"

        return db.execute_query(query, tuple(params), fetch_all=True)

    @staticmethod
    def get_overdue():
        """Get all overdue transactions"""
        today = datetime.now().date()
        query = """
            SELECT t.*, b.title, b.author, u.full_name as user_name, u.email
            FROM transactions t
            JOIN books b ON t.book_id = b.book_id
            JOIN users u ON t.user_id = u.user_id
            WHERE t.status = 'issued' AND t.due_date < ?
            ORDER BY t.due_date
        """
        return db.execute_query(query, (today,), fetch_all=True)

    @staticmethod
    def update_overdue_status():
        """Update status of overdue books"""
        today = datetime.now().date()
        query = """
            UPDATE transactions
            SET status = 'overdue'
            WHERE status = 'issued' AND due_date < ?
        """
        db.execute_query(query, (today,))
