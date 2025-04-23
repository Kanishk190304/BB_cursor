#!/usr/bin/env python
import os
import django
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_stability.settings')
django.setup()

# Import models
from core.models import Budget, Category
from django.contrib.auth.models import User

# Get the first user and an expense category
user = User.objects.first()
expense_category = Category.objects.filter(is_expense=True).first()

if user and expense_category:
    # Get current month and year
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    # Create a budget
    budget = Budget.objects.create(
        user=user,
        category=expense_category,
        amount=500.00,
        month=current_month,
        year=current_year
    )
    print(f"Budget created successfully with ID: {budget.id}")
    
    # Get all budgets
    all_budgets = Budget.objects.filter(user=user)
    print(f"Found {len(all_budgets)} budgets for user {user.username}")
    
    # List them
    for b in all_budgets:
        print(f"ID: {b.id}, Category: {b.category.name}, Amount: {b.amount}, Month/Year: {b.month}/{b.year}")
else:
    if not user:
        print("No users found in the database!")
    if not expense_category:
        print("No expense categories found in the database!") 