from flask import Blueprint, request, jsonify
from models.book import Book
from models.transaction import Transaction
from models.fine import Fine
from models.user import User
from middleware.auth_middleware import token_required, role_required

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
@token_required
@role_required('admin', 'librarian')
def get_dashboard_stats(current_user_id, current_user_role):
    """Get dashboard statistics"""
    try:
        # Total books
        all_books = Book.get_all()
        total_books = len(all_books)

        # Available books
        available_books = len([b for b in all_books if b['available_copies'] > 0])

        # Total users by role
        all_users = User.get_all()
        total_users = len(all_users)
        students = len([u for u in all_users if u['role'] == 'student'])
        librarians = len([u for u in all_users if u['role'] == 'librarian'])

        # Current transactions
        issued_books = len(Transaction.get_all(status='issued'))

        # Overdue books
        Transaction.update_overdue_status()
        overdue_books = len(Transaction.get_overdue())

        # Pending fines
        total_pending_fines = Fine.get_total_pending()

        # Recent transactions
        recent_transactions = Transaction.get_all()[:10]  # Last 10 transactions

        return jsonify({
            'stats': {
                'total_books': total_books,
                'available_books': available_books,
                'total_users': total_users,
                'students': students,
                'librarians': librarians,
                'issued_books': issued_books,
                'overdue_books': overdue_books,
                'pending_fines': total_pending_fines
            },
            'recent_transactions': recent_transactions
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/inventory', methods=['GET'])
@token_required
@role_required('admin', 'librarian')
def get_inventory_report(current_user_id, current_user_role):
    """Get inventory report"""
    try:
        books = Book.get_all()

        # Group by category
        categories = {}
        for book in books:
            category = book['category']
            if category not in categories:
                categories[category] = {
                    'total_books': 0,
                    'total_copies': 0,
                    'available_copies': 0
                }

            categories[category]['total_books'] += 1
            categories[category]['total_copies'] += book['total_copies']
            categories[category]['available_copies'] += book['available_copies']

        return jsonify({
            'inventory': categories,
            'total_categories': len(categories)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/circulation', methods=['GET'])
@token_required
@role_required('admin', 'librarian')
def get_circulation_report(current_user_id, current_user_role):
    """Get circulation report for date range"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({'error': 'Start date and end date are required'}), 400

        # This would require more complex queries in a real implementation
        # For now, return basic transaction counts
        all_transactions = Transaction.get_all()

        # Filter by date range (simplified)
        issued_count = len([t for t in all_transactions
                           if t['status'] in ['issued', 'returned']])

        returned_count = len([t for t in all_transactions
                             if t['status'] == 'returned'])

        overdue_count = len([t for t in all_transactions
                            if t['status'] == 'overdue'])

        return jsonify({
            'circulation': {
                'books_issued': issued_count,
                'books_returned': returned_count,
                'books_overdue': overdue_count,
                'period': f'{start_date} to {end_date}'
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/fines', methods=['GET'])
@token_required
@role_required('admin', 'librarian')
def get_fines_report(current_user_id, current_user_role):
    """Get fines report"""
    try:
        status = request.args.get('status', 'pending')
        fines = Fine.get_all(status=status)

        total_amount = sum(fine['amount'] for fine in fines)

        return jsonify({
            'fines': fines,
            'total_amount': total_amount,
            'count': len(fines)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
