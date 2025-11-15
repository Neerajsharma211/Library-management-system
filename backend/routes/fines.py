from flask import Blueprint, request, jsonify
from models.fine import Fine
from middleware.auth_middleware import token_required, role_required

fines_bp = Blueprint('fines', __name__)

@fines_bp.route('/user/<int:user_id>', methods=['GET'])
@token_required
def get_user_fines(user_id, current_user_id, current_user_role):
    """Get fines for a specific user"""
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

@fines_bp.route('/', methods=['GET'])
@token_required
@role_required('admin', 'librarian')
def get_all_fines(current_user_id, current_user_role):
    """Get all fines"""
    status = request.args.get('status')
    fines = Fine.get_all(status=status)

    total_amount = sum(fine['amount'] for fine in fines)

    return jsonify({
        'fines': fines,
        'total_amount': total_amount,
        'count': len(fines)
    }), 200

@fines_bp.route('/<int:fine_id>', methods=['GET'])
@token_required
def get_fine(fine_id, current_user_id, current_user_role):
    """Get a specific fine"""
    fine = Fine.get_by_id(fine_id)

    if not fine:
        return jsonify({'error': 'Fine not found'}), 404

    # Users can only view their own fines
    if current_user_role == 'student' and fine['user_id'] != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({'fine': fine}), 200

@fines_bp.route('/<int:fine_id>/pay', methods=['POST'])
@token_required
@role_required('admin', 'librarian')
def pay_fine(fine_id, current_user_id, current_user_role):
    """Mark a fine as paid"""
    data = request.get_json() or {}
    payment_method = data.get('payment_method', 'cash')

    success = Fine.pay_fine(fine_id, payment_method)

    if success:
        return jsonify({'message': 'Fine marked as paid'}), 200
    else:
        return jsonify({'error': 'Failed to update fine'}), 500

@fines_bp.route('/<int:fine_id>/waive', methods=['POST'])
@token_required
@role_required('admin')
def waive_fine(fine_id, current_user_id, current_user_role):
    """Waive a fine"""
    success = Fine.waive_fine(fine_id)

    if success:
        return jsonify({'message': 'Fine waived successfully'}), 200
    else:
        return jsonify({'error': 'Failed to waive fine'}), 500
