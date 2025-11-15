#!/usr/bin/env python3
"""
Script to create default admin user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User

def create_admin():
    """Create default admin user"""
    try:
        # Check if admin already exists
        existing_admin = User.get_by_email('admin@library.com')
        if existing_admin:
            print("Admin user already exists!")
            return

        # Create admin user
        admin_id = User.create(
            username='admin',
            email='admin@library.com',
            password='Admin@123',
            full_name='System Administrator',
            role='admin'
        )

        print(f"Admin user created successfully with ID: {admin_id}")

        # Create sample librarian
        librarian_id = User.create(
            username='librarian',
            email='librarian@library.com',
            password='Librarian@123',
            full_name='Head Librarian',
            role='librarian'
        )

        print(f"Librarian user created successfully with ID: {librarian_id}")

        # Create sample student
        student_id = User.create(
            username='student',
            email='student@library.com',
            password='Student@123',
            full_name='John Doe',
            role='student'
        )

        print(f"Student user created successfully with ID: {student_id}")

    except Exception as e:
        print(f"Error creating users: {e}")

if __name__ == '__main__':
    create_admin()
