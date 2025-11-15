// Utility functions for the frontend

function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.getElementById('alert-container') ||
                          document.createElement('div');

    if (!alertContainer.id) {
        alertContainer.id = 'alert-container';
        document.body.insertBefore(alertContainer, document.body.firstChild);
    }

    const alertId = 'alert-' + Date.now();
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type}" style="margin-bottom: 1rem;">
            ${message}
            <button onclick="this.parentElement.remove()" style="float: right; background: none; border: none; font-size: 1.2em; cursor: pointer;">&times;</button>
        </div>
    `;

    alertContainer.insertAdjacentHTML('beforeend', alertHTML);

    // Auto remove after duration
    if (duration > 0) {
        setTimeout(() => {
            const alertElement = document.getElementById(alertId);
            if (alertElement) {
                alertElement.remove();
            }
        }, duration);
    }
}

function showSpinner(element) {
    element.innerHTML = '<div class="spinner"></div>';
}

function hideSpinner(element) {
    // This will be replaced by actual content
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function getStatusBadge(status) {
    const badges = {
        'issued': 'badge-info',
        'returned': 'badge-success',
        'overdue': 'badge-danger',
        'pending': 'badge-warning',
        'paid': 'badge-success',
        'waived': 'badge-secondary'
    };

    return `<span class="badge ${badges[status] || 'badge-info'}">${status}</span>`;
}

function confirmAction(message) {
    return window.confirm(message);
}

function createTable(headers, data, actions = []) {
    let html = '<table class="table"><thead><tr>';

    headers.forEach(header => {
        html += `<th>${header}</th>`;
    });

    if (actions.length > 0) {
        html += '<th>Actions</th>';
    }

    html += '</tr></thead><tbody>';

    data.forEach(row => {
        html += '<tr>';
        headers.forEach(header => {
            const key = header.toLowerCase().replace(' ', '_');
            html += `<td>${row[key] || 'N/A'}</td>`;
        });

        if (actions.length > 0) {
            html += '<td>';
            actions.forEach(action => {
                html += `<button class="btn btn-sm ${action.class}" onclick="${action.handler}(${row.id})">${action.label}</button> `;
            });
            html += '</td>';
        }

        html += '</tr>';
    });

    html += '</tbody></table>';
    return html;
}

function createModal(id, title, content, footer = '') {
    return `
        <div id="${id}" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button onclick="closeModal('${id}')">&times;</button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
                ${footer ? `<div class="modal-footer">${footer}</div>` : ''}
            </div>
        </div>
    `;
}

function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Form validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 8;
}

function validateRequired(value) {
    return value && value.trim() !== '';
}

// Local storage helpers
function setStorageItem(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
        console.error('Error saving to localStorage:', e);
    }
}

function getStorageItem(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (e) {
        console.error('Error reading from localStorage:', e);
        return null;
    }
}

function removeStorageItem(key) {
    localStorage.removeItem(key);
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions to global scope
window.showAlert = showAlert;
window.showSpinner = showSpinner;
window.hideSpinner = hideSpinner;
window.formatDate = formatDate;
window.formatCurrency = formatCurrency;
window.getStatusBadge = getStatusBadge;
window.confirmAction = confirmAction;
window.createTable = createTable;
window.createModal = createModal;
window.openModal = openModal;
window.closeModal = closeModal;
window.validateEmail = validateEmail;
window.validatePassword = validatePassword;
window.validateRequired = validateRequired;
window.setStorageItem = setStorageItem;
window.getStorageItem = getStorageItem;
window.removeStorageItem = removeStorageItem;
window.debounce = debounce;
