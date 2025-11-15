from datetime import datetime
from models.database import db

class Fine:
    @staticmethod
    def create(transaction_id, user_id, amount, days_overdue):
        """Create a fine"""
        query = """
            INSERT INTO fines (transaction_id, user_id, amount, days_overdue, status)
            VALUES (?, ?, ?, ?, 'pending')
        """
        return db.execute_query(query, (transaction_id, user_id, amount, days_overdue))

    @staticmethod
    def get_by_id(fine_id):
        """Get fine by ID"""
        query = """
            SELECT f.*, t.book_id, b.title, u.full_name as user_name
            FROM fines f
            JOIN transactions t ON f.transaction_id = t.transaction_id
            JOIN books b ON t.book_id = b.book_id
            JOIN users u ON f.user_id = u.user_id
            WHERE f.fine_id = ?
        """
        return db.execute_query(query, (fine_id,), fetch_one=True)

    @staticmethod
    def get_by_user(user_id, status=None):
        """Get all fines for a user"""
        query = """
            SELECT f.*, t.book_id, b.title, b.author
            FROM fines f
            JOIN transactions t ON f.transaction_id = t.transaction_id
            JOIN books b ON t.book_id = b.book_id
            WHERE f.user_id = ?
        """
        params = [user_id]

        if status:
            query += " AND f.status = ?"
            params.append(status)

        query += " ORDER BY f.created_at DESC"

        return db.execute_query(query, tuple(params), fetch_all=True)

    @staticmethod
    def get_all(status=None):
        """Get all fines"""
        query = """
            SELECT f.*, u.full_name as user_name, u.email, b.title
            FROM fines f
            JOIN users u ON f.user_id = u.user_id
            JOIN transactions t ON f.transaction_id = t.transaction_id
            JOIN books b ON t.book_id = b.book_id
        """
        params = []

        if status:
            query += " WHERE f.status = ?"
            params.append(status)

        query += " ORDER BY f.created_at DESC"

        return db.execute_query(query, tuple(params), fetch_all=True)

    @staticmethod
    def pay_fine(fine_id, payment_method='cash'):
        """Mark fine as paid"""
        query = """
            UPDATE fines
            SET status = 'paid', paid_date = ?, payment_method = ?
            WHERE fine_id = ?
        """
        paid_date = datetime.now().date()
        db.execute_query(query, (paid_date, payment_method, fine_id))
        return True

    @staticmethod
    def waive_fine(fine_id):
        """Waive a fine"""
        query = "UPDATE fines SET status = 'waived' WHERE fine_id = ?"
        db.execute_query(query, (fine_id,))
        return True

    @staticmethod
    def get_total_pending(user_id=None):
        """Get total pending fines"""
        if user_id:
            query = """
                SELECT COALESCE(SUM(amount), 0) as total
                FROM fines
                WHERE user_id = ? AND status = 'pending'
            """
            result = db.execute_query(query, (user_id,), fetch_one=True)
        else:
            query = """
                SELECT COALESCE(SUM(amount), 0) as total
                FROM fines
                WHERE status = 'pending'
            """
            result = db.execute_query(query, fetch_one=True)

        return result['total'] if result else 0
