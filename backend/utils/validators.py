import re
from email_validator import validate_email, EmailNotValidError

class Validator:
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        try:
            validate_email(email)
            return True, None
        except EmailNotValidError as e:
            return False, str(e)

    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"

        return True, None

    @staticmethod
    def validate_isbn(isbn):
        """Validate ISBN-10 or ISBN-13"""
        isbn = isbn.replace('-', '').replace(' ', '')

        if len(isbn) == 10:
            return Validator._validate_isbn10(isbn)
        elif len(isbn) == 13:
            return Validator._validate_isbn13(isbn)
        else:
            return False, "ISBN must be 10 or 13 digits"

    @staticmethod
    def _validate_isbn10(isbn):
        if not isbn[:-1].isdigit():
            return False, "Invalid ISBN-10 format"

        total = sum((i + 1) * int(digit) for i, digit in enumerate(isbn[:9]))
        check = (11 - (total % 11)) % 11
        check_digit = 'X' if check == 10 else str(check)

        if isbn[-1] != check_digit:
            return False, "Invalid ISBN-10 checksum"

        return True, None

    @staticmethod
    def _validate_isbn13(isbn):
        if not isbn.isdigit():
            return False, "Invalid ISBN-13 format"

        total = sum((3 if i % 2 else 1) * int(digit) for i, digit in enumerate(isbn[:12]))
        check = (10 - (total % 10)) % 10

        if int(isbn[-1]) != check:
            return False, "Invalid ISBN-13 checksum"

        return True, None

    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, phone.replace('-', '').replace(' ', '')):
            return False, "Invalid phone number format"
        return True, None

    @staticmethod
    def validate_role(role):
        """Validate user role"""
        valid_roles = ['admin', 'librarian', 'student']
        if role not in valid_roles:
            return False, f"Role must be one of: {', '.join(valid_roles)}"
        return True, None
