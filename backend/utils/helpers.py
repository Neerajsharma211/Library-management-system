from datetime import datetime

def format_date(date_str):
    """Format date string to readable format"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str

def calculate_days_overdue(due_date_str):
    """Calculate days overdue from due date"""
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        if today > due_date:
            return (today - due_date).days
        return 0
    except:
        return 0

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:.2f}"

def generate_book_id():
    """Generate a unique book ID"""
    import uuid
    return str(uuid.uuid4())[:8].upper()

def sanitize_string(text):
    """Sanitize string input"""
    if not text:
        return ""
    return str(text).strip()

def is_valid_date(date_str):
    """Check if date string is valid"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except:
        return False
