# Student Financial Stability Project

A student-focused budgeting and financial wellness app to track income, categorize expenses, encourage savings, and promote smart money habits.

## Features

- **Smart Budgeting**: Create custom budgets for categories like Food, Hangouts, and Books with limits and alerts
- **Expense Tracking**: Visualize your spending with beautiful charts and breakdowns
- **Savings Goals**: Set and track progress towards financial goals
- **Financial Education**: Learn money management through bite-sized tips
- **Achievements**: Earn badges by completing financial challenges
- **Dark/Light Mode**: Beautiful aesthetic with both light and dark themes

## Getting Started

### Prerequisites

- Python 3.8+
- Django 5.0+

### Installation

1. Clone the repository:
```
git clone <repository-url>
cd StudentFinApp
```

2. Install dependencies:
```
pip install django
```

3. Navigate to the project directory:
```
cd financial_stability
```

4. Run migrations:
```
python manage.py migrate
```

5. Start the development server:
```
python manage.py runserver
```

6. Visit `http://127.0.0.1:8000/` in your browser to see the app

## Project Structure

```
financial_stability/
├── core/                  # Main app for financial functionality
├── static/                # Static files (CSS, JS, images)
│   ├── css/               # CSS stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Images and icons
├── templates/             # HTML templates
│   ├── base.html          # Base template with header/footer
│   ├── home.html          # Homepage
│   └── dashboard.html     # Main dashboard
└── financial_stability/   # Project settings
```

## Usage

- **Home Page**: Information about the app and features
- **Dashboard**: Track expenses, budgets, and savings goals
- **Dark Mode**: Toggle between light and dark mode with the moon/sun icon in the navbar

## Future Enhancements

- Mobile app version with cross-platform synchronization
- Receipt scanning for automatic expense logging
- Peer-to-peer payment options for group expenses
- Integration with banking APIs for real-time transaction tracking
- Advanced financial insights and recommendations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Bootstrap for the responsive UI components
- Chart.js for data visualization
- FontAwesome for icons 