from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from models.user import User
from utils.validators import Validator
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'email', 'password', 'full_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Validate email
    valid, error = Validator.validate_email(data['email'])
    if not valid:
        return jsonify({'error': error}), 400

    # Validate password
    valid, error = Validator.validate_password(data['password'])
    if not valid:
        return jsonify({'error': error}), 400

    # Check if user already exists
    if User.get_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 409

    if User.get_by_username(data['username']):
        return jsonify({'error': 'Username already taken'}), 409

    # Create user
    try:
        user_id = User.create(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            full_name=data['full_name'],
            role=data.get('role', 'student'),
            phone=data.get('phone'),
            address=data.get('address')
        )

        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password required'}), 400

    # Get user
    user = User.get_by_email(data['email'])

    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Verify password
    if not User.verify_password(user['password_hash'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate JWT token
    payload = {
        'user_id': user['user_id'],
        'role': user['role'],
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    }

    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'role': user['role']
        }
    }), 200

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """Change user password (requires token)"""
    from middleware.auth_middleware import token_required

    @token_required
    def _change_password(current_user_id, **kwargs):
        data = request.get_json()

        required = ['current_password', 'new_password']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        # Get user
        user = User.get_by_id(current_user_id)

        # Verify current password
        if not User.verify_password(user['password_hash'], data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 401

        # Validate new password
        valid, error = Validator.validate_password(data['new_password'])
        if not valid:
            return jsonify({'error': error}), 400

        # Change password
        User.change_password(current_user_id, data['new_password'])

        return jsonify({'message': 'Password changed successfully'}), 200

    return _change_password()
