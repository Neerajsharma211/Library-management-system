from functools import wraps
from flask import jsonify

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user_role = kwargs.get('current_user_role')
        if current_user_role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

def librarian_required(f):
    """Decorator to require librarian role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user_role = kwargs.get('current_user_role')
        if current_user_role not in ['admin', 'librarian']:
            return jsonify({'error': 'Librarian access required'}), 403
        return f(*args, **kwargs)
    return decorated

def student_required(f):
    """Decorator to require student role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user_role = kwargs.get('current_user_role')
        if current_user_role not in ['admin', 'librarian', 'student']:
            return jsonify({'error': 'Student access required'}), 403
        return f(*args, **kwargs)
    return decorated
