/* 
 * Fix for navbar and button issues
 * This script directly handles click events and navigation
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Fix script loaded');
    
    // Map menu items to their correct URLs
    const urlMap = {
        'Home': '/',
        'Dashboard': '/',
        'Expenses': '/transactions/',
        'Savings': '/savings/',
        'Learn': '#',
        'Profile': '/profile/',
        'Logout': '/logout/',
        'Login': '/login/',
        'Sign Up': '/register/',
        'Add Transaction': '/transactions/add/',
        'Create Budget': '/budgets/add/',
        'Add Savings Goal': '/savings/add/'
    };
    
    // Fix navbar links
    document.querySelectorAll('a.nav-link, a.navbar-brand, .dropdown-item').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const text = this.innerText.trim();
            if (urlMap[text]) {
                console.log(`Navigating to: ${urlMap[text]}`);
                window.location.href = urlMap[text];
            } else {
                // Try to extract from URL
                const href = this.getAttribute('href');
                if (href && href !== '#') {
                    window.location.href = href;
                }
            }
        });
    });
    
    // Fix buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const text = this.innerText.trim();
            if (urlMap[text]) {
                e.preventDefault();
                console.log(`Button navigating to: ${urlMap[text]}`);
                window.location.href = urlMap[text];
            }
            
            // Fix View All buttons
            if (text === 'View All') {
                const parentCard = this.closest('.card');
                if (parentCard) {
                    const cardTitle = parentCard.querySelector('.card-header h5').innerText.trim();
                    if (cardTitle.includes('Transactions')) {
                        e.preventDefault();
                        window.location.href = '/transactions/';
                    } else if (cardTitle.includes('Budget')) {
                        e.preventDefault();
                        window.location.href = '/budgets/';
                    } else if (cardTitle.includes('Savings')) {
                        e.preventDefault();
                        window.location.href = '/savings/';
                    }
                }
            }
        });
    });
    
    // Fix specific action buttons
    const addTransactionBtn = document.querySelector('a[href*="add_transaction"]');
    if (addTransactionBtn) {
        addTransactionBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/transactions/add/';
        });
    }
    
    const createBudgetBtn = document.querySelector('a[href*="add_budget"], a[href*="create_budget"]');
    if (createBudgetBtn) {
        createBudgetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = '/budgets/add/';
        });
    }
    
    // Fix dashboard buttons
    const dashboardBtns = {
        'Add Transaction': '/transactions/add/',
        'Add Savings Goal': '/savings/add/',
        'Create Budget': '/budgets/add/',
        'Manage Budgets': '/budgets/',
        'View All': '/transactions/' // Default, context-specific cases handled above
    };
    
    Object.keys(dashboardBtns).forEach(btnText => {
        document.querySelectorAll(`a:contains('${btnText}'), button:contains('${btnText}')`).forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                window.location.href = dashboardBtns[btnText];
            });
        });
    });
}); 