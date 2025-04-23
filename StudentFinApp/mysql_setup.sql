-- MySQL setup script for BachatBuddy application

-- Create the database
CREATE DATABASE IF NOT EXISTS bachatbuddy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create the user
CREATE USER IF NOT EXISTS 'bbuser'@'localhost' IDENTIFIED BY 'bbpassword';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON bachatbuddy.* TO 'bbuser'@'localhost';
FLUSH PRIVILEGES;

-- Use the database
USE bachatbuddy;

-- The rest of the tables will be created by Django migrations
-- This script only sets up the database and user 