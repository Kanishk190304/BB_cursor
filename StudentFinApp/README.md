# BachatBuddy - Financial Stability App

BachatBuddy is a comprehensive financial management application built with Django that helps users track their expenses, create budgets, set savings goals, and manage their overall financial health.

## Features

- **User Authentication**: Secure registration and login
- **Dashboard**: Visualize your financial overview
- **Transaction Management**: Track all your income and expenses
- **Budget Planning**: Set monthly budgets by category
- **Savings Goals**: Create and track progress towards financial goals
- **Reports**: Analyze your spending patterns over time

## Getting Started

### Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bachatbuddy.git
   cd bachatbuddy
   ```

2. Set up the MySQL database:
   
   **For Windows:**
   ```powershell
   # Run the setup script
   .\setup_mysql.ps1
   ```
   
   **For Linux/Mac:**
   ```bash
   # Make the script executable
   chmod +x setup_mysql.sh
   
   # Run the setup script
   ./setup_mysql.sh
   ```
   
   Alternatively, follow the manual setup in `MYSQL_SETUP_GUIDE.md`.

3. Create a superuser (admin account):
   ```bash
   cd financial_stability
   python manage.py createsuperuser
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

5. Open your browser and go to http://localhost:8000

## Database Schema

The application uses the following key models:

- **User**: Django's built-in user model
- **UserProfile**: Extended user information
- **Category**: Transaction categories
- **Transaction**: Income and expense records
- **Budget**: Monthly budgets by category
- **SavingsGoal**: Financial targets and tracking
- **Achievement**: User accomplishments

## Development

### Running Tests

```bash
python manage.py test
```

### Coding Style

This project follows the PEP 8 style guide for Python code.

## Deployment

For production deployment:

1. Set `DEBUG=False` in your `.env` file
2. Configure a proper web server (Nginx, Apache)
3. Use a production-grade WSGI server (Gunicorn, uWSGI)
4. Set up proper database backups

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap for frontend components
- Font Awesome for icons
- Chart.js for data visualization

## Contact

For questions or feedback, please contact:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername) 