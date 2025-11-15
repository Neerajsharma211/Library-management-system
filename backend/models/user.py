import bcrypt
from models.database import db

class User:
    @staticmethod
    def create(username, email, password, full_name, role='student', **kwargs):
        """Create a new user"""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        query = """
            INSERT INTO users (username, email, password_hash, full_name, role, phone, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            username,
            email,
            password_hash.decode('utf-8'),
            full_name,
            role,
            kwargs.get('phone'),
            kwargs.get('address')
        )

        return db.execute_query(query, params)

    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = ? AND is_active = 1"
        return db.execute_query(query, (user_id,), fetch_one=True)

    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = ? AND is_active = 1"
        return db.execute_query(query, (email,), fetch_one=True)

    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = ? AND is_active = 1"
        return db.execute_query(query, (username,), fetch_one=True)

    @staticmethod
    def verify_password(stored_hash, password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

    @staticmethod
    def get_all(role=None):
        """Get all users, optionally filtered by role"""
        if role:
            query = "SELECT * FROM users WHERE role = ? AND is_active = 1 ORDER BY created_at DESC"
            return db.execute_query(query, (role,), fetch_all=True)
        else:
            query = "SELECT * FROM users WHERE is_active = 1 ORDER BY created_at DESC"
            return db.execute_query(query, fetch_all=True)

    @staticmethod
    def update(user_id, **kwargs):
        """Update user information"""
        allowed_fields = ['email', 'full_name', 'phone', 'address', 'role', 'is_active']

        updates = []
        params = []

        for field in allowed_fields:
            if field in kwargs:
                updates.append(f"{field} = ?")
                params.append(kwargs[field])

        if not updates:
            return False

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"

        db.execute_query(query, tuple(params))
        return True

    @staticmethod
    def delete(user_id):
        """Soft delete user"""
        query = "UPDATE users SET is_active = 0 WHERE user_id = ?"
        db.execute_query(query, (user_id,))
        return True

    @staticmethod
    def change_password(user_id, new_password):
        """Change user password"""
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        query = "UPDATE users SET password_hash = ? WHERE user_id = ?"
        db.execute_query(query, (password_hash.decode('utf-8'), user_id))
        return True
