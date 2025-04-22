# BachatBuddy - Student Financial Stability App

BachatBuddy is a comprehensive financial management application designed specifically for students. The app helps students track expenses, set budgets, create savings goals, and develop healthy financial habits.

## Features

- **Expense Tracking**: Log your daily expenses and income with detailed categorization
- **Budget Management**: Set monthly budgets for different expense categories
- **Savings Goals**: Create and track progress towards your financial goals
- **Financial Analytics**: Visualize your spending patterns and identify areas for improvement
- **Category Management**: Customize expense and income categories to suit your needs
- **User Profiles**: Personalize your experience with customizable settings

## Tech Stack

- **Backend**: Django 5.2
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (default), easily configurable for PostgreSQL or MySQL
- **Charts**: Chart.js
- **Icons**: Font Awesome 6

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/bachatbuddy.git
cd bachatbuddy
```

2. **Create and activate a virtual environment**

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Navigate to the project directory**

```bash
cd StudentFinApp/financial_stability
```

5. **Apply migrations**

```bash
python manage.py migrate
```

6. **Load initial data (categories)**

```bash
python manage.py loaddata core/fixtures/initial_categories.json
```

7. **Create a superuser**

```bash
python manage.py createsuperuser
```

8. **Run the development server**

```bash
python manage.py runserver
```

9. **Access the application**

Open your browser and navigate to `http://127.0.0.1:8000`

## Screenshots

![Dashboard](dashboard.png)
![Transactions](transactions.png)
![Budget](budget.png)
![Savings Goals](savings.png)

## Development

### Project Structure

```
financial_stability/
├── core/                 # Main app with all financial functionality
│   ├── fixtures/         # Initial data
│   ├── migrations/       # Database migrations
│   ├── templates/        # HTML templates
│   ├── forms.py          # Form definitions
│   ├── models.py         # Database models
│   ├── urls.py           # URL routing
│   └── views.py          # View controllers
├── static/               # Static files (CSS, JS, images)
│   ├── css/              # CSS files
│   ├── js/               # JavaScript files
│   └── img/              # Images
├── templates/            # Base templates
└── financial_stability/  # Project settings
```

### Making Changes

1. Create a new branch for your feature
2. Make changes and test locally
3. Commit changes to your branch
4. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Bootstrap for the responsive UI components
- Chart.js for data visualization
- Font Awesome for icons
- Django community for the excellent framework

## Contact

For questions or feedback, please contact:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername) 