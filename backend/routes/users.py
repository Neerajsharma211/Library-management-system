from flask import Blueprint, request, jsonify
from models.user import User
from models.fine import Fine
from models.transaction import Transaction
from middleware.auth_middleware import token_required, role_required
from utils.validators import Validator

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@token_required
@role_required('admin', 'librarian')
def get_users(current_user_id, current_user_role):
    """Get all users"""
    role = request.args.get('role')
    users = User.get_all(role=role)

    return jsonify({
        'users': users,
        'count': len(users)
    }), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id, current_user_id, current_user_role):
    """Get a specific user"""
    # Users can only view their own profile, admins can view all
    if current_user_role != 'admin' and user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    user = User.get_by_id(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Remove password hash from response
    user.pop('password_hash', None)

    return jsonify({'user': user}), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id, current_user_id, current_user_role):
    """Update user information"""
    # Users can only update their own profile, admins can update all
    if current_user_role != 'admin' and user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()

    # Validate email if provided
    if 'email' in data:
        valid, error = Validator.validate_email(data['email'])
        if not valid:
            return jsonify({'error': error}), 400

    # Validate role if provided (only admin can change roles)
    if 'role' in data and current_user_role != 'admin':
        return jsonify({'error': 'Only admins can change user roles'}), 403

    try:
        success = User.update(user_id, **data)
        if success:
            return jsonify({'message': 'User updated successfully'}), 200
        else:
            return jsonify({'error': 'No changes made'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_user(user_id, current_user_id, current_user_role):
    """Delete a user (soft delete)"""
    if user_id == current_user_id:
        return jsonify({'error': 'Cannot delete your own account'}), 400

    success = User.delete(user_id)

    if success:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete user'}), 500

@users_bp.route('/<int:user_id>/books', methods=['GET'])
@token_required
def get_user_books(user_id, current_user_id, current_user_role):
    """Get books issued to a user"""
    # Users can only view their own books, admins/librarians can view all
    if current_user_role == 'student' and user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    transactions = Transaction.get_by_user(user_id, status='issued')

    return jsonify({
        'books': transactions,
        'count': len(transactions)
    }), 200

@users_bp.route('/<int:user_id>/fines', methods=['GET'])
@token_required
def get_user_fines(user_id, current_user_id, current_user_role):
    """Get fines for a user"""
    # Users can only view their own fines, admins/librarians can view all
    if current_user_role == 'student' and user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    status = request.args.get('status')
    fines = Fine.get_by_user(user_id, status=status)

    total_pending = Fine.get_total_pending(user_id)

    return jsonify({
        'fines': fines,
        'total_pending': total_pending,
        'count': len(fines)
    }), 200
