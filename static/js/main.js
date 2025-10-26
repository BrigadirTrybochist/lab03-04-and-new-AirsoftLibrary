// Main JavaScript file for the airsoft collection app

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Confirm deletion forms
    const deleteButtons = document.querySelectorAll('form[onsubmit*="confirm"]');
    deleteButtons.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const confirmMessage = form.getAttribute('onsubmit').match(/confirm\('([^']+)'/);
            if (confirmMessage && !confirm(confirmMessage[1])) {
                e.preventDefault();
                return false;
            }
        });
    });

    // Weapon card hover effects
    const weaponCards = document.querySelectorAll('.weapon-card');
    weaponCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.15)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });

    // Real-time input validation
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(function(input) {
        input.addEventListener('input', function() {
            if (this.hasAttribute('required') && this.value.trim()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.remove('is-valid');
            }
        });
    });

    // FPS to Joules calculator (approximate conversion)
    const fpsInput = document.querySelector('input[name="fps"]');
    const joulesInput = document.querySelector('input[name="joules"]');
    
    if (fpsInput && joulesInput) {
        fpsInput.addEventListener('input', function() {
            const fps = parseFloat(this.value);
            if (!isNaN(fps) && fps > 0) {
                // Approximate conversion: J = (fps^2 * bb_weight_in_kg) / (2 * 3.28^2 * 1000)
                // Assuming 0.2g BB weight
                const joules = (Math.pow(fps, 2) * 0.0002) / (2 * Math.pow(3.28, 2) * 1000);
                if (!joulesInput.value) {
                    joulesInput.value = joules.toFixed(2);
                }
            }
        });

        joulesInput.addEventListener('input', function() {
            const joules = parseFloat(this.value);
            if (!isNaN(joules) && joules > 0) {
                // Reverse conversion
                const fps = Math.sqrt((joules * 2 * Math.pow(3.28, 2) * 1000) / 0.0002);
                if (!fpsInput.value) {
                    fpsInput.value = Math.round(fps);
                }
            }
        });
    }

    // Table sorting functionality
    const tableHeaders = document.querySelectorAll('th[data-sort]');
    tableHeaders.forEach(function(header) {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const column = this.dataset.sort;
            const currentOrder = this.dataset.order || 'asc';
            const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
            
            // Update header indicators
            tableHeaders.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
            this.classList.add('sorted-' + newOrder);
            this.dataset.order = newOrder;
            
            // Sort rows
            rows.sort(function(a, b) {
                const aValue = a.children[parseInt(column)].textContent.trim();
                const bValue = b.children[parseInt(column)].textContent.trim();
                
                if (newOrder === 'asc') {
                    return aValue.localeCompare(bValue, 'uk', { numeric: true });
                } else {
                    return bValue.localeCompare(aValue, 'uk', { numeric: true });
                }
            });
            
            // Reorder table
            rows.forEach(row => tbody.appendChild(row));
        });
    });

    // Search functionality for tables
    const searchInputs = document.querySelectorAll('.table-search');
    searchInputs.forEach(function(searchInput) {
        const table = searchInput.dataset.table ? document.querySelector(searchInput.dataset.table) : searchInput.closest('.card').querySelector('table');
        if (!table) return;
        
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Inject CSRF token into fetch requests automatically (if meta tag present)
(function() {
    try {
        const meta = document.querySelector('meta[name="csrf-token"]');
        const CSRF = meta ? meta.getAttribute('content') : null;
        if (!CSRF) return;

        const _fetch = window.fetch;
        window.fetch = function(input, init) {
            init = init || {};
            init.headers = init.headers || {};

            // If headers is a Headers instance, set via .set
            if (typeof Headers !== 'undefined' && init.headers instanceof Headers) {
                if (!init.headers.get('X-CSRFToken')) init.headers.set('X-CSRFToken', CSRF);
            } else if (typeof init.headers === 'object') {
                if (!init.headers['X-CSRFToken'] && !init.headers['X-CSRF-Token']) {
                    init.headers['X-CSRFToken'] = CSRF;
                }
            }

            return _fetch(input, init);
        };
    } catch (e) {
        // silent
        console.debug('CSRF fetch wrapper error', e);
    }
})();

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('uk-UA', {
        style: 'currency',
        currency: 'UAH',
        minimumFractionDigits: 0
    }).format(amount);
}

// Utility function to format date
function formatDate(date) {
    return new Intl.DateTimeFormat('uk-UA', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }).format(new Date(date));
}

// Function to show confirmation modal
function showConfirmation(message, onConfirm) {
    if (confirm(message)) {
        onConfirm();
    }
}

// Function to show toast notification
function showToast(message, type = 'info') {
    // Create toast element if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}
