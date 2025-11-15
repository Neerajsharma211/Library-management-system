from flask import Blueprint, request, jsonify
from models.transaction import Transaction
from middleware.auth_middleware import token_required, role_required

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/issue', methods=['POST'])
@token_required
@role_required('admin', 'librarian')
def issue_book(current_user_id, current_user_role):
    """Issue a book to a user"""
    data = request.get_json()

    required = ['book_id', 'user_id']
    for field in required:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    success, result = Transaction.issue_book(
        book_id=data['book_id'],
        user_id=data['user_id'],
        librarian_id=current_user_id,
        issue_days=data.get('issue_days')
    )

    if not success:
        return jsonify({'error': result}), 400

    return jsonify({
        'message': 'Book issued successfully',
        'transaction_id': result
    }), 201

@transactions_bp.route('/return/<int:transaction_id>', methods=['POST'])
@token_required
@role_required('admin', 'librarian')
def return_book(transaction_id, current_user_id, current_user_role):
    """Return a book"""
    success, message = Transaction.return_book(transaction_id, current_user_id)

    if not success:
        return jsonify({'error': message}), 400

    return jsonify({'message': message}), 200

@transactions_bp.route('/', methods=['GET'])
@token_required
def get_transactions(current_user_id, current_user_role):
    """Get transactions"""
    status = request.args.get('status')
    user_id = request.args.get('user_id')

    # Students can only view their own transactions
    if current_user_role == 'student':
        user_id = current_user_id

    if user_id:
        transactions = Transaction.get_by_user(int(user_id), status)
    else:
        transactions = Transaction.get_all(status)

    return jsonify({
        'transactions': transactions,
        'count': len(transactions)
    }), 200

@transactions_bp.route('/<int:transaction_id>', methods=['GET'])
@token_required
def get_transaction(transaction_id, current_user_id, current_user_role):
    """Get a specific transaction"""
    transaction = Transaction.get_by_id(transaction_id)

    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    # Students can only view their own transactions
    if current_user_role == 'student' and transaction['user_id'] != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({'transaction': transaction}), 200

@transactions_bp.route('/overdue', methods=['GET'])
@token_required
@role_required('admin', 'librarian')
def get_overdue(current_user_id, current_user_role):
    """Get all overdue transactions"""
    # Update overdue status first
    Transaction.update_overdue_status()

    overdue = Transaction.get_overdue()

    return jsonify({
        'overdue_transactions': overdue,
        'count': len(overdue)
    }), 200
