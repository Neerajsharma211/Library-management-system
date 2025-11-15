# Library Management System

A comprehensive library management system built with Flask (backend) and vanilla JavaScript (frontend), featuring role-based access control, book management, transaction tracking, and fine calculation.

## Features

### Core Functionality
- **User Management**: Admin, Librarian, and Student roles with appropriate permissions
- **Book Management**: Add, update, search, and organize books by category
- **Transaction Management**: Issue and return books with due date tracking
- **Fine Management**: Automatic fine calculation for overdue books
- **Reports**: Comprehensive reporting on inventory, circulation, and user activity
- **Authentication**: JWT-based secure authentication system

### User Roles
- **Admin**: Full system access, user management, book management, reports
- **Librarian**: Book issuing/returning, user assistance, basic reports
- **Student**: Browse books, view personal transactions and fines

## Technology Stack

### Backend
- **Flask**: Web framework
- **SQLite**: Database
- **JWT**: Authentication
- **bcrypt**: Password hashing
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **HTML5/CSS3**: Structure and styling
- **Vanilla JavaScript**: Client-side logic
- **Responsive Design**: Mobile-friendly interface

## Project Structure

```
library-management-system/
│
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Configuration settings
│   ├── requirements.txt          # Python dependencies
│   │
│   ├── models/
│   │   ├── database.py          # Database connection
│   │   ├── user.py              # User model
│   │   ├── book.py              # Book model
│   │   ├── transaction.py       # Transaction model
│   │   └── fine.py              # Fine model
│   │
│   ├── routes/
│   │   ├── auth.py              # Authentication routes
│   │   ├── books.py             # Book CRUD routes
│   │   ├── transactions.py      # Issue/Return routes
│   │   ├── users.py             # User management routes
│   │   └── reports.py           # Reporting routes
│   │
│   ├── middleware/
│   │   ├── auth_middleware.py   # JWT validation
│   │   └── role_middleware.py   # Role-based access control
│   │
│   ├── utils/
│   │   ├── validators.py        # Input validation
│   │   ├── helpers.py           # Helper functions
│   │   └── fine_calculator.py   # Fine calculation logic
│   │
│   └── scripts/
│       └── create_admin.py      # Admin user creation script
│
├── frontend/
│   ├── index.html               # Landing page
│   ├── login.html               # Login page
│   ├── dashboard.html           # Main dashboard
│   │
│   ├── pages/
│   │   ├── admin/
│   │   │   ├── manage-books.html
│   │   │   ├── manage-users.html
│   │   │   └── reports.html
│   │   │
│   │   ├── librarian/
│   │   │   ├── issue-book.html
│   │   │   ├── return-book.html
│   │   │   └── search-books.html
│   │   │
│   │   └── student/
│   │       ├── browse-books.html
│   │       ├── my-books.html
│   │       └── my-fines.html
│   │
│   ├── css/
│   │   ├── main.css             # Global styles
│   │   └── dashboard.css        # Dashboard styles
│   │
│   └── js/
│       ├── api.js               # API calls
│       ├── auth.js              # Authentication logic
│       ├── dashboard.js         # Dashboard functionality
│       └── utils.js             # Utility functions
│
├── database/
│   └── library.db               # SQLite database (auto-generated)
│
├── tests/                       # Test files
├── .env                         # Environment variables
└── README.md
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database:**
   ```bash
   python -c "from models.database import db; print('Database initialized')"
   ```

5. **Create default users:**
   ```bash
   python scripts/create_admin.py
   ```

6. **Run the backend server:**
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Serve the frontend:**
   ```bash
   # Using Python's built-in server
   python -m http.server 8000

   # Or using npx
   npx serve .
   ```

3. **Open browser:**
   ```
   http://localhost:8000
   ```

## Default Users

After running the setup script, you can login with these default accounts:

- **Admin**: `admin@library.com` / `Admin@123`
- **Librarian**: `librarian@library.com` / `Librarian@123`
- **Student**: `student@library.com` / `Student@123`

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/change-password` - Change password

### Book Endpoints
- `GET /api/books` - Get all books
- `POST /api/books` - Create new book
- `PUT /api/books/{id}` - Update book
- `DELETE /api/books/{id}` - Delete book
- `GET /api/books/search` - Search books

### Transaction Endpoints
- `POST /api/transactions/issue` - Issue book
- `POST /api/transactions/return/{id}` - Return book
- `GET /api/transactions` - Get transactions

### User Endpoints
- `GET /api/users` - Get users
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Report Endpoints
- `GET /api/reports/dashboard` - Dashboard statistics
- `GET /api/reports/inventory` - Inventory report
- `GET /api/reports/circulation` - Circulation report

## Database Schema

The system uses SQLite with the following main tables:
- `users` - User accounts and roles
- `books` - Book inventory
- `transactions` - Book issue/return records
- `fines` - Fine records for overdue books
- `categories` - Book categories
- `audit_log` - System activity log

## Configuration

Environment variables in `.env`:
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `DATABASE_PATH` - SQLite database path
- `FINE_PER_DAY` - Fine amount per day overdue
- `MAX_BOOKS_PER_USER` - Maximum books per user
- `DEFAULT_ISSUE_DAYS` - Default issue period

## Development

### Running Tests
```bash
cd backend
python -m pytest tests/
```

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue on GitHub.
