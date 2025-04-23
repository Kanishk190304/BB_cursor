#!/bin/bash
# Bash script for setting up MySQL for BachatBuddy on Linux/Mac

echo -e "\e[32mSetting up MySQL for BachatBuddy\e[0m"

# Check if MySQL is installed
if command -v mysql &> /dev/null; then
    echo -e "\e[32mMySQL is already installed\e[0m"
else
    echo -e "\e[33mMySQL is not installed\e[0m"
    echo -e "\e[33mPlease install MySQL using your package manager:\e[0m"
    echo -e "\e[33mDebian/Ubuntu: sudo apt install mysql-server\e[0m"
    echo -e "\e[33mFedora/RHEL: sudo dnf install mysql mysql-server\e[0m"
    echo -e "\e[33mArch: sudo pacman -S mysql\e[0m"
    echo -e "\e[33mMac: brew install mysql\e[0m"
    exit 1
fi

# Check Python and required packages
if command -v python3 &> /dev/null; then
    echo -e "\e[32mPython is installed\e[0m"
    
    # Check pip and install required packages
    if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
        echo -e "\e[32mInstalling required Python packages...\e[0m"
        pip install -r requirements.txt
    else
        echo -e "\e[31mpip is not installed\e[0m"
        echo -e "\e[33mPlease install pip using your package manager\e[0m"
        exit 1
    fi
else
    echo -e "\e[31mPython is not installed\e[0m"
    echo -e "\e[33mPlease install Python 3 using your package manager\e[0m"
    exit 1
fi

# Create MySQL database and user
echo -e "\e[32mSetting up MySQL database and user...\e[0m"
echo -e "\e[36mPlease enter your MySQL root password:\e[0m"
read -s ROOT_PASSWORD

# Run the SQL script
echo -e "\e[32mCreating database and user...\e[0m"
mysql -u root -p"$ROOT_PASSWORD" < mysql_setup.sql

# Create .env file from example
if [ ! -f "financial_stability/.env" ]; then
    echo -e "\e[32mCreating .env file from example...\e[0m"
    cp financial_stability/.env-example financial_stability/.env
    echo -e "\e[32m.env file created. Please update it with your settings if needed.\e[0m"
fi

# Run migrations
echo -e "\e[32mRunning Django migrations...\e[0m"
cd financial_stability
python manage.py makemigrations
python manage.py migrate

# Load initial data
echo -e "\e[32mLoading initial data...\e[0m"
python manage.py loaddata core/fixtures/initial_data.json

echo -e "\e[32mMySQL setup complete!\e[0m"
echo -e "\e[32mYou can now run 'python manage.py runserver' to start the application\e[0m" 