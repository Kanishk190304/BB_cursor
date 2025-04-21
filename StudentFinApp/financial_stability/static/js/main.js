document.addEventListener('DOMContentLoaded', function() {
    // Theme toggler
    const themeToggle = document.getElementById('theme-toggle');
    const icon = themeToggle.querySelector('i');
    let currentTheme = localStorage.getItem('theme') || 'light';
    
    // Apply saved theme on load
    document.body.setAttribute('data-bs-theme', currentTheme);
    updateThemeIcon(currentTheme);
    
    themeToggle.addEventListener('click', function() {
        currentTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.body.setAttribute('data-bs-theme', currentTheme);
        localStorage.setItem('theme', currentTheme);
        updateThemeIcon(currentTheme);
    });
    
    function updateThemeIcon(theme) {
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
    
    // Initialize all tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Initialize all popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    
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
    
    // Form validation for transaction forms
    const transactionForms = document.querySelectorAll('.transaction-form');
    transactionForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
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
});

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