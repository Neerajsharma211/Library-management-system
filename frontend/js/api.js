// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

class API {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.token = localStorage.getItem('token');
    }

    // Set authentication token
    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    // Remove authentication token
    removeToken() {
        this.token = null;
        localStorage.removeItem('token');
    }

    // Get headers with authentication
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        return headers;
    }

    // Generic request method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        const config = {
            ...options,
            headers: this.getHeaders()
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Authentication
    async login(email, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    }

    async register(userData) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async changePassword(currentPassword, newPassword) {
        return this.request('/auth/change-password', {
            method: 'POST',
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword
            })
        });
    }

    // Books
    async getBooks(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/books?${query}`);
    }

    async getBook(bookId) {
        return this.request(`/books/${bookId}`);
    }

    async searchBooks(keyword) {
        return this.request(`/books/search?q=${encodeURIComponent(keyword)}`);
    }

    async createBook(bookData) {
        return this.request('/books', {
            method: 'POST',
            body: JSON.stringify(bookData)
        });
    }

    async updateBook(bookId, bookData) {
        return this.request(`/books/${bookId}`, {
            method: 'PUT',
            body: JSON.stringify(bookData)
        });
    }

    async deleteBook(bookId) {
        return this.request(`/books/${bookId}`, {
            method: 'DELETE'
        });
    }

    async getCategories() {
        return this.request('/books/categories');
    }

    // Transactions
    async issueBook(bookId, userId, issueDays) {
        return this.request('/transactions/issue', {
            method: 'POST',
            body: JSON.stringify({
                book_id: bookId,
                user_id: userId,
                issue_days: issueDays
            })
        });
    }

    async returnBook(transactionId) {
        return this.request(`/transactions/return/${transactionId}`, {
            method: 'POST'
        });
    }

    async getTransactions(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/transactions?${query}`);
    }

    async getTransaction(transactionId) {
        return this.request(`/transactions/${transactionId}`);
    }

    async getOverdueTransactions() {
        return this.request('/transactions/overdue');
    }

    // Users
    async getUsers(role) {
        const query = role ? `?role=${role}` : '';
        return this.request(`/users${query}`);
    }

    async getUser(userId) {
        return this.request(`/users/${userId}`);
    }

    async updateUser(userId, userData) {
        return this.request(`/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    }

    async deleteUser(userId) {
        return this.request(`/users/${userId}`, {
            method: 'DELETE'
        });
    }

    // Fines
    async getUserFines(userId, status) {
        const query = status ? `?status=${status}` : '';
        return this.request(`/fines/user/${userId}${query}`);
    }

    async getAllFines(status) {
        const query = status ? `?status=${status}` : '';
        return this.request(`/fines${query}`);
    }

    async payFine(fineId, paymentMethod) {
        return this.request(`/fines/${fineId}/pay`, {
            method: 'POST',
            body: JSON.stringify({ payment_method: paymentMethod })
        });
    }

    async waiveFine(fineId) {
        return this.request(`/fines/${fineId}/waive`, {
            method: 'POST'
        });
    }

    // Reports
    async getDashboardStats() {
        return this.request('/reports/dashboard');
    }

    async getInventoryReport() {
        return this.request('/reports/inventory');
    }

    async getCirculationReport(startDate, endDate) {
        return this.request(`/reports/circulation?start_date=${startDate}&end_date=${endDate}`);
    }
}

// Export singleton instance
const api = new API();
