/**
 * BachatBuddy - Student Financial Stability
 * Main JavaScript file for UI interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initTooltips();
    
    // Setup theme toggler
    setupThemeToggle();
    
    // Setup auto-dismissing alerts
    setupAlerts();
    
    // Add form validation
    setupFormValidation();
    
    // Animate numbers in stat cards with countUp.js if available
    const statValues = document.querySelectorAll('.stat-value');
    if (statValues.length > 0 && typeof countUp !== 'undefined') {
        statValues.forEach(element => {
            const value = parseFloat(element.getAttribute('data-value') || element.innerText);
            const countUpAnim = new countUp.CountUp(element, value, {
                duration: 2,
                useEasing: true
            });
            if (!countUpAnim.error) {
                countUpAnim.start();
            }
        });
    }
    
    // Spending limit warning animations
    const budgetProgressBars = document.querySelectorAll('.budget-progress .progress-bar');
    budgetProgressBars.forEach(bar => {
        const value = parseInt(bar.getAttribute('aria-valuenow'));
        if (value >= 90) {
            bar.classList.add('bg-danger');
        } else if (value >= 75) {
            bar.classList.add('bg-warning');
        }
    });
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Initialize any charts if present
    initializeCharts();
    
    // Handle dashboard buttons
    const addTransactionBtn = document.querySelector('[href*="add_transaction"]');
    if (addTransactionBtn) {
        addTransactionBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/transactions/add/';
        });
    }
    
    const addSavingsGoalBtn = document.querySelector('[href*="add_savings"]');
    if (addSavingsGoalBtn) {
        addSavingsGoalBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/savings/add/';
        });
    }
    
    const createBudgetBtn = document.querySelector('[href*="add_budget"]');
    if (createBudgetBtn) {
        createBudgetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/budgets/add/';
        });
    }
    
    // Handle navigation menu
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            if (href && href !== '#') {
                window.location.href = href;
            }
        });
    });
    
    // Handle view all links
    const viewAllLinks = document.querySelectorAll('.btn-outline-primary');
    viewAllLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            if (href && href !== '#') {
                window.location.href = href;
            }
        });
    });
});

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Setup dark/light theme toggle
 */
function setupThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.querySelector('html');
    const body = document.querySelector('body');
    const icon = themeToggle ? themeToggle.querySelector('i') : null;
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = body.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            body.setAttribute('data-bs-theme', newTheme);
            if (icon) {
                if (newTheme === 'dark') {
                    icon.classList.remove('fa-moon');
                    icon.classList.add('fa-sun');
                } else {
                    icon.classList.remove('fa-sun');
                    icon.classList.add('fa-moon');
                }
            }
            
            // Save preference
            localStorage.setItem('theme', newTheme);
        });
        
        // Set initial theme from localStorage
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            body.setAttribute('data-bs-theme', savedTheme);
            if (icon) {
                if (savedTheme === 'dark') {
                    icon.classList.remove('fa-moon');
                    icon.classList.add('fa-sun');
                }
            }
        }
    }
}

/**
 * Setup auto-dismissing alerts
 */
function setupAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        // Auto-dismiss success alerts after 5 seconds
        if (alert.classList.contains('alert-success')) {
            setTimeout(() => {
                fadeOut(alert);
            }, 5000);
        }
        
        // Add click handler to close button
        const closeButton = alert.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                fadeOut(alert);
            });
        }
    });
}

/**
 * Fade out and remove an element
 * @param {HTMLElement} element - Element to fade out
 */
function fadeOut(element) {
    element.style.transition = 'opacity 0.5s ease';
    element.style.opacity = '0';
    
    setTimeout(() => {
        element.remove();
    }, 500);
}

/**
 * Setup form validation
 */
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Format currency with appropriate symbol
 * @param {number} amount - Amount to format
 * @param {string} currencySymbol - Currency symbol to use
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount, currencySymbol = 'Rs.') {
    return `${currencySymbol} ${parseFloat(amount).toFixed(2)}`;
}

/**
 * Calculate percentage and ensure it's between 0-100
 * @param {number} current - Current value
 * @param {number} total - Total value
 * @returns {number} Percentage (0-100)
 */
function calculatePercentage(current, total) {
    if (total <= 0) return 0;
    const percentage = (current / total) * 100;
    return Math.min(Math.max(percentage, 0), 100);
}

/**
 * Get appropriate CSS class based on percentage
 * @param {number} percentage - Percentage value
 * @returns {string} CSS class name
 */
function getPercentageClass(percentage) {
    if (percentage >= 90) return 'bg-danger';
    if (percentage >= 70) return 'bg-warning';
    if (percentage >= 50) return 'bg-info';
    return 'bg-success';
}

/**
 * Toggle visibility of an element
 * @param {string} elementId - ID of element to toggle
 */
function toggleElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        if (element.style.display === 'none') {
            element.style.display = 'block';
        } else {
            element.style.display = 'none';
        }
    }
}

/**
 * Filter dropdown options based on search input
 * @param {string} inputId - ID of input element
 * @param {string} dropdownId - ID of dropdown element
 */
function filterDropdown(inputId, dropdownId) {
    const input = document.getElementById(inputId);
    const dropdown = document.getElementById(dropdownId);
    
    if (!input || !dropdown) return;
    
    input.addEventListener('keyup', function() {
        const filter = input.value.toUpperCase();
        const options = dropdown.querySelectorAll('.dropdown-item');
        
        options.forEach(option => {
            const txtValue = option.textContent || option.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                option.style.display = '';
            } else {
                option.style.display = 'none';
            }
        });
    });
}

/**
 * Update transaction form based on type selection
 * Filters categories based on expense/income selection
 */
function updateTransactionForm() {
    const isExpense = document.getElementById('id_is_expense');
    const categorySelect = document.getElementById('id_category');
    
    if (!isExpense || !categorySelect) return;
    
    // Store original options
    if (!window.originalOptions) {
        window.originalOptions = Array.from(categorySelect.options).map(opt => ({
            value: opt.value,
            text: opt.text,
            isExpense: opt.dataset.isExpense === 'true'
        }));
    }
    
    // Filter options based on transaction type
    function filterOptions() {
        const isExpenseChecked = isExpense.checked;
        
        // Clear current options
        categorySelect.innerHTML = '';
        
        // Add filtered options
        window.originalOptions.forEach(opt => {
            if (opt.isExpense === isExpenseChecked || opt.value === '') {
                const option = document.createElement('option');
                option.value = opt.value;
                option.text = opt.text;
                option.dataset.isExpense = opt.isExpense;
                categorySelect.appendChild(option);
            }
        });
    }
    
    // Filter on change
    isExpense.addEventListener('change', filterOptions);
    
    // Initial filter
    filterOptions();
}

/**
 * Setup date range picker for transaction filtering
 */
function setupDateRangePicker() {
    const dateFrom = document.getElementById('date_from');
    const dateTo = document.getElementById('date_to');
    
    if (!dateFrom || !dateTo) return;
    
    // Ensure dateTo is never before dateFrom
    dateFrom.addEventListener('change', function() {
        if (dateTo.value && dateFrom.value > dateTo.value) {
            dateTo.value = dateFrom.value;
        }
    });
    
    dateTo.addEventListener('change', function() {
        if (dateFrom.value && dateTo.value < dateFrom.value) {
            dateFrom.value = dateTo.value;
        }
    });
}

/**
 * Handle modal confirmation for delete actions
 */
function setupDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('[data-delete-url]');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const url = this.dataset.deleteUrl;
            const itemName = this.dataset.itemName || 'item';
            
            if (confirm(`Are you sure you want to delete this ${itemName}? This action cannot be undone.`)) {
                window.location.href = url;
            }
        });
    });
}

// Function to initialize charts
function initializeCharts() {
    // Spending categories pie chart
    const spendingCategoriesChart = document.getElementById('spendingCategoriesChart');
    if (spendingCategoriesChart) {
        new Chart(spendingCategoriesChart, {
            type: 'doughnut',
            data: {
                labels: ['Food', 'Hangouts', 'Transport', 'Utilities', 'Books', 'Others'],
                datasets: [{
                    data: [30, 20, 15, 10, 15, 10],
                    backgroundColor: [
                        '#4361ee', // primary
                        '#3a0ca3', // secondary
                        '#7209b7',
                        '#f72585',
                        '#4cc9f0', // accent
                        '#560bad'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': Rs. ' + context.raw;
                            }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }

    // Monthly spending history line chart
    const monthlySpendingChart = document.getElementById('monthlySpendingChart');
    if (monthlySpendingChart) {
        new Chart(monthlySpendingChart, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Spending',
                    data: [650, 590, 800, 810, 560, 550],
                    borderColor: '#4361ee',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'Budget',
                    data: [700, 700, 700, 700, 700, 700],
                    borderColor: '#e71d36',
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': Rs. ' + context.raw;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'Rs. ' + value;
                            }
                        }
                    }
                }
            }
        });
    }

    // Savings goal progress chart
    const savingsProgressChart = document.getElementById('savingsProgressChart');
    if (savingsProgressChart) {
        new Chart(savingsProgressChart, {
            type: 'bar',
            data: {
                labels: ['Emergency Fund', 'Spring Break', 'New Laptop', 'Graduation'],
                datasets: [{
                    label: 'Current',
                    data: [500, 300, 200, 100],
                    backgroundColor: '#4361ee'
                },
                {
                    label: 'Goal',
                    data: [1000, 500, 800, 1200],
                    backgroundColor: 'rgba(67, 97, 238, 0.2)'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': Rs. ' + context.raw;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                    },
                    y: {
                        stacked: false,
                        ticks: {
                            callback: function(value) {
                                return 'Rs. ' + value;
                            }
                        }
                    }
                }
            }
        });
    }
} 