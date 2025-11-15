// Dashboard functionality

document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    if (!authManager.requireAuth()) return;

    const user = authManager.getCurrentUser();
    document.getElementById('userName').textContent = user.full_name;
    document.getElementById('userRole').textContent = user.role.charAt(0).toUpperCase() + user.role.slice(1);

    // Show/hide navigation based on role
    if (user.role === 'admin') {
        document.getElementById('nav-admin').classList.remove('hidden');
    }

    // Load dashboard data
    loadDashboardStats();
    loadQuickActions();
    loadRecentActivity();

    // Logout functionality
    document.getElementById('logoutBtn').addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to logout?')) {
            authManager.logout();
        }
    });
});

async function loadDashboardStats() {
    const statsGrid = document.getElementById('statsGrid');

    try {
        const response = await api.getDashboardStats();
        const stats = response.stats;

        statsGrid.innerHTML = `
            <div class="stat-card">
                <h3>${stats.total_books}</h3>
                <p>Total Books</p>
            </div>
            <div class="stat-card">
                <h3>${stats.available_books}</h3>
                <p>Available Books</p>
            </div>
            <div class="stat-card">
                <h3>${stats.issued_books}</h3>
                <p>Books Issued</p>
            </div>
            <div class="stat-card">
                <h3>${stats.overdue_books}</h3>
                <p>Overdue Books</p>
            </div>
            <div class="stat-card">
                <h3>${stats.total_users}</h3>
                <p>Total Users</p>
            </div>
            <div class="stat-card">
                <h3>${formatCurrency(stats.pending_fines)}</h3>
                <p>Pending Fines</p>
            </div>
        `;
    } catch (error) {
        statsGrid.innerHTML = '<div class="alert alert-error">Failed to load dashboard statistics</div>';
        console.error('Error loading dashboard stats:', error);
    }
}

function loadQuickActions() {
    const quickActions = document.getElementById('quickActions');
    const user = authManager.getCurrentUser();

    let actions = '';

    if (user.role === 'admin') {
        actions = `
            <a href="/pages/admin/manage-books.html" class="btn btn-primary">Manage Books</a>
            <a href="/pages/admin/manage-users.html" class="btn btn-secondary">Manage Users</a>
            <a href="/pages/admin/reports.html" class="btn btn-outline">View Reports</a>
        `;
    } else if (user.role === 'librarian') {
        actions = `
            <a href="/pages/librarian/issue-book.html" class="btn btn-primary">Issue Book</a>
            <a href="/pages/librarian/return-book.html" class="btn btn-secondary">Return Book</a>
            <a href="/pages/librarian/search-books.html" class="btn btn-outline">Search Books</a>
        `;
    } else if (user.role === 'student') {
        actions = `
            <a href="/pages/student/browse-books.html" class="btn btn-primary">Browse Books</a>
            <a href="/pages/student/my-books.html" class="btn btn-secondary">My Books</a>
            <a href="/pages/student/my-fines.html" class="btn btn-outline">My Fines</a>
        `;
    }

    quickActions.innerHTML = actions;
}

async function loadRecentActivity() {
    const recentActivity = document.getElementById('recentActivity');

    try {
        const response = await api.getDashboardStats();
        const transactions = response.recent_transactions;

        if (transactions.length === 0) {
            recentActivity.innerHTML = '<p>No recent activity</p>';
            return;
        }

        let html = '<ul class="activity-list">';
        transactions.slice(0, 5).forEach(transaction => {
            const status = getStatusBadge(transaction.status);
            const date = formatDate(transaction.issue_date);
            html += `
                <li class="activity-item">
                    <span>${transaction.title} - ${transaction.user_name}</span>
                    <span>${status}</span>
                    <small>${date}</small>
                </li>
            `;
        });
        html += '</ul>';

        recentActivity.innerHTML = html;
    } catch (error) {
        recentActivity.innerHTML = '<div class="alert alert-error">Failed to load recent activity</div>';
        console.error('Error loading recent activity:', error);
    }
}
