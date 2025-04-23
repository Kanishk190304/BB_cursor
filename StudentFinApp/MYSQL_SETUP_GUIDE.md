# MySQL Integration Guide for BachatBuddy

This guide will help you set up MySQL for your BachatBuddy Django application.

## Prerequisites

1. MySQL Server installed on your system
2. Python and pip installed

## Step 1: Install Required Python Packages

```bash
pip install -r requirements.txt
```

This will install the required packages including `mysqlclient` for MySQL connectivity.

## Step 2: Set Up MySQL Database and User

You can set up the database in two ways:

### Option 1: Using the MySQL Command Line

1. Log in to MySQL as root:
   ```bash
   mysql -u root -p
   ```

2. Run the SQL commands from `mysql_setup.sql`:
   ```bash
   source mysql_setup.sql
   ```

### Option 2: Using the SQL File Directly

```bash
mysql -u root -p < mysql_setup.sql
```

## Step 3: Migrate Your Database

Once MySQL is set up, you need to migrate your Django models to create the tables:

```bash
cd financial_stability
python manage.py makemigrations
python manage.py migrate
```

## Step 4: Load Initial Data

Load the initial categories and other data:

```bash
python manage.py loaddata core/fixtures/initial_data.json
```

## Step 5: Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

## Step 6: Run the Development Server

```bash
python manage.py runserver
```

## Troubleshooting

### Common Issues

1. **Connection Refused**: Make sure MySQL server is running
   ```bash
   # On Windows
   net start mysql
   
   # On Linux
   sudo systemctl start mysql
   ```

2. **Authentication Failed**: Check your MySQL credentials in `settings.py`

3. **Missing mysqlclient**: If you get an error about missing mysqlclient:
   ```bash
   pip install mysqlclient
   ```

4. **MySQL Server Version**: If you're using MySQL 8.0+, you might need to change the authentication method:
   ```sql
   ALTER USER 'bbuser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'bbpassword';
   FLUSH PRIVILEGES;
   ```

## Production Considerations

For production environments:

1. Use environment variables for database credentials
2. Set appropriate character sets and collations
3. Configure database connection pooling
4. Set up proper backup procedures 