# PowerShell script for setting up MySQL for BachatBuddy on Windows
Write-Host "Setting up MySQL for BachatBuddy" -ForegroundColor Green

# Check if MySQL is installed
try {
    $mysqlPath = Get-Command mysql -ErrorAction Stop
    Write-Host "MySQL is already installed at: $($mysqlPath.Source)" -ForegroundColor Green
} 
catch {
    Write-Host "MySQL is not installed or not in PATH" -ForegroundColor Yellow
    Write-Host "Please download and install MySQL from: https://dev.mysql.com/downloads/installer/" -ForegroundColor Yellow
    Write-Host "Make sure to add MySQL to your PATH during installation" -ForegroundColor Yellow
    exit
}

# Check Python and required packages
try {
    $pythonPath = Get-Command python -ErrorAction Stop
    Write-Host "Python is installed at: $($pythonPath.Source)" -ForegroundColor Green
    
    # Check pip and install required packages
    try {
        $pipPath = Get-Command pip -ErrorAction Stop
        Write-Host "Installing required Python packages..." -ForegroundColor Green
        pip install -r requirements.txt
    }
    catch {
        Write-Host "pip is not installed or not in PATH" -ForegroundColor Red
        exit
    }
}
catch {
    Write-Host "Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit
}

# Create MySQL database and user
Write-Host "Setting up MySQL database and user..." -ForegroundColor Green
Write-Host "Please enter your MySQL root password:" -ForegroundColor Cyan
$securePassword = Read-Host -AsSecureString
$credential = New-Object System.Management.Automation.PSCredential("root", $securePassword)
$rootPassword = $credential.GetNetworkCredential().Password

# Create a temporary SQL file with the setup script
$tempSqlFile = [System.IO.Path]::GetTempFileName()
Get-Content "mysql_setup.sql" | Out-File $tempSqlFile -Encoding ASCII

# Run the SQL script
Write-Host "Creating database and user..." -ForegroundColor Green
mysql -u root -p"$rootPassword" < $tempSqlFile

# Clean up
Remove-Item $tempSqlFile

# Create .env file from example
if (-not (Test-Path "financial_stability/.env")) {
    Write-Host "Creating .env file from example..." -ForegroundColor Green
    Copy-Item "financial_stability/.env-example" "financial_stability/.env"
    Write-Host ".env file created. Please update it with your settings if needed." -ForegroundColor Green
}

# Run migrations
Write-Host "Running Django migrations..." -ForegroundColor Green
cd financial_stability
python manage.py makemigrations
python manage.py migrate

# Load initial data
Write-Host "Loading initial data..." -ForegroundColor Green
python manage.py loaddata core/fixtures/initial_data.json

Write-Host "MySQL setup complete!" -ForegroundColor Green
Write-Host "You can now run 'python manage.py runserver' to start the application" -ForegroundColor Green 