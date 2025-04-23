#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_stability.settings')
django.setup()

# Import models
from core.models import Transaction, Category
from django.contrib.auth.models import User
from django.utils import timezone

# Get the first user and category
user = User.objects.first()
category = Category.objects.first()

if user and category:
    # Create a transaction
    transaction = Transaction.objects.create(
        user=user,
        category=category,
        amount=150.00,
        description='Test transaction from script',
        date=timezone.now(),
        is_expense=True
    )
    print(f"Transaction created successfully with ID: {transaction.id}")
    
    # Get all transactions
    all_transactions = Transaction.objects.filter(user=user)
    print(f"Found {len(all_transactions)} transactions for user {user.username}")
    
    # List them
    for t in all_transactions:
        print(f"ID: {t.id}, Amount: {t.amount}, Description: {t.description}")
else:
    if not user:
        print("No users found in the database!")
    if not category:
        print("No categories found in the database!") 