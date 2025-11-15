class AuthManager {
    constructor() {
        this.currentUser = this.loadUser();
    }

    // Load user from localStorage
    loadUser() {
        const userStr = localStorage.getItem('currentUser');
        return userStr ? JSON.parse(userStr) : null;
    }

    // Save user to localStorage
    saveUser(user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
        this.currentUser = user;
    }

    // Check if user is logged in
    isLoggedIn() {
        return this.currentUser !== null && localStorage.getItem('token') !== null;
    }

    // Get current user
    getCurrentUser() {
        return this.currentUser;
    }

    // Check if user has specific role
    hasRole(role) {
        return this.currentUser && this.currentUser.role === role;
    }

    // Check if user has any of the specified roles
    hasAnyRole(roles) {
        return this.currentUser && roles.includes(this.currentUser.role);
    }

    // Login
    async login(email, password) {
        try {
            const response = await api.login(email, password);

            // Save token and user
            api.setToken(response.token);
            this.saveUser(response.user);

            return { success: true, user: response.user };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Logout
    logout() {
        api.removeToken();
        localStorage.removeItem('currentUser');
        this.currentUser = null;
        window.location.href = '/login.html';
    }

    // Require authentication
    requireAuth() {
        if (!this.isLoggedIn()) {
            window.location.href = '/login.html';
            return false;
        }
        return true;
    }

    // Require specific role
    requireRole(role) {
        if (!this.requireAuth()) return false;

        if (!this.hasRole(role)) {
            alert('Access denied: Insufficient permissions');
            window.location.href = '/dashboard.html';
            return false;
        }
        return true;
    }

    // Require any of specified roles
    requireAnyRole(roles) {
        if (!this.requireAuth()) return false;

        if (!this.hasAnyRole(roles)) {
            alert('Access denied: Insufficient permissions');
            window.location.href = '/dashboard.html';
            return false;
        }
        return true;
    }
}

// Export singleton instance
const authManager = new AuthManager();
