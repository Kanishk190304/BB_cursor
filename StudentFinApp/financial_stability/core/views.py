from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta
from calendar import monthrange
import json

from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm, 
    UserProfileForm,
    TransactionForm, 
    BudgetForm, 
    SavingsGoalForm,
    UpdateSavingsForm,
    CategoryForm
)
from .models import (
    Category,
    UserProfile,
    Transaction,
    Budget,
    SavingsGoal,
    Achievement
)

# Authentication views
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard and Home views
@login_required
def dashboard_view(request):
    user = request.user
    
    # Get all transactions for the current month
    now = timezone.now()
    current_month_start = timezone.make_aware(datetime(now.year, now.month, 1))
    _, last_day = monthrange(now.year, now.month)
    current_month_end = timezone.make_aware(datetime(now.year, now.month, last_day, 23, 59, 59))
    
    # Get recent transactions (last 5)
    recent_transactions = Transaction.objects.filter(
        user=user
    ).order_by('-date')[:5]
    
    # Monthly summary
    income = Transaction.objects.filter(
        user=user,
        is_expense=False,
        date__range=(current_month_start, current_month_end)
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    expenses = Transaction.objects.filter(
        user=user,
        is_expense=True,
        date__range=(current_month_start, current_month_end)
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate savings rate
    if income > 0:
        savings_rate = ((income - expenses) / income) * 100
    else:
        savings_rate = 0
    
    # Get budgets for the current month
    current_budgets = Budget.objects.filter(
        user=user,
        month=now.month,
        year=now.year
    ).select_related('category')
    
    # Prepare budget data for charts
    budget_data = []
    for budget in current_budgets:
        spent = budget.get_spent_amount()
        budget_data.append({
            'category': budget.category.name,
            'budget': float(budget.amount),
            'spent': float(spent),
            'remaining': float(budget.amount - spent),
            'percentage': budget.get_percentage()
        })
    
    # Get savings goals
    savings_goals = SavingsGoal.objects.filter(user=user)
    
    # Get achievements
    achievements = Achievement.objects.filter(user=user).order_by('-date_earned')[:5]
    
    context = {
        'recent_transactions': recent_transactions,
        'income': income,
        'expenses': expenses,
        'savings_rate': savings_rate,
        'budget_data': json.dumps(budget_data),
        'budgets': current_budgets,
        'savings_goals': savings_goals,
        'achievements': achievements,
    }
    
    return render(request, 'core/dashboard.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'core/profile.html', {'form': form})

# Transaction views
@login_required
def transaction_list_view(request):
    # Get filter parameters
    category_id = request.GET.get('category')
    transaction_type = request.GET.get('type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Base queryset
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    # Apply filters
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    
    if transaction_type:
        is_expense = transaction_type == 'expense'
        transactions = transactions.filter(is_expense=is_expense)
    
    if date_from:
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        transactions = transactions.filter(date__gte=date_from)
    
    if date_to:
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        date_to = datetime.combine(date_to, datetime.max.time())
        transactions = transactions.filter(date__lte=date_to)
    
    # Get categories for filter dropdown
    categories = Category.objects.all()
    
    context = {
        'transactions': transactions,
        'categories': categories,
        'selected_category': category_id,
        'selected_type': transaction_type,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'core/transactions.html', context)

@login_required
def transaction_create_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction added successfully!")
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'core/transaction_form.html', {'form': form, 'action': 'Add'})

@login_required
def transaction_edit_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully!")
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    
    return render(request, 'core/transaction_form.html', {'form': form, 'action': 'Edit'})

@login_required
def transaction_delete_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transaction deleted successfully!")
        return redirect('transaction_list')
    
    return render(request, 'core/transaction_confirm_delete.html', {'transaction': transaction})

# Budget views
@login_required
def budget_list_view(request):
    now = timezone.now()
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))
    
    budgets = Budget.objects.filter(
        user=request.user,
        month=month,
        year=year
    ).select_related('category')
    
    context = {
        'budgets': budgets,
        'current_month': month,
        'current_year': year,
        'months': range(1, 13),
        'years': range(now.year-2, now.year+3),
    }
    
    return render(request, 'core/budgets.html', context)

@login_required
def budget_create_view(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            
            # Check if a budget for this category/month/year already exists
            existing_budget = Budget.objects.filter(
                user=request.user,
                category=budget.category,
                month=budget.month,
                year=budget.year
            ).first()
            
            if existing_budget:
                messages.error(request, "A budget for this category already exists for the selected month/year.")
            else:
                budget.save()
                messages.success(request, "Budget created successfully!")
                return redirect('budget_list')
    else:
        form = BudgetForm(user=request.user)
    
    return render(request, 'core/budget_form.html', {'form': form, 'action': 'Create'})

@login_required
def budget_edit_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget updated successfully!")
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget, user=request.user)
    
    return render(request, 'core/budget_form.html', {'form': form, 'action': 'Edit'})

@login_required
def budget_delete_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    
    if request.method == 'POST':
        budget.delete()
        messages.success(request, "Budget deleted successfully!")
        return redirect('budget_list')
    
    return render(request, 'core/budget_confirm_delete.html', {'budget': budget})

# Savings Goal views
@login_required
def savings_goal_list_view(request):
    savings_goals = SavingsGoal.objects.filter(user=request.user)
    
    for goal in savings_goals:
        goal.percentage = goal.get_percentage()
        goal.status = goal.get_status()
    
    return render(request, 'core/savings.html', {'savings_goals': savings_goals})

@login_required
def savings_goal_create_view(request):
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            savings_goal = form.save(commit=False)
            savings_goal.user = request.user
            savings_goal.save()
            messages.success(request, "Savings goal created successfully!")
            return redirect('savings_goal_list')
    else:
        form = SavingsGoalForm()
    
    return render(request, 'core/savings_goal_form.html', {'form': form, 'action': 'Create'})

@login_required
def savings_goal_edit_view(request, pk):
    savings_goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=savings_goal)
        if form.is_valid():
            form.save()
            messages.success(request, "Savings goal updated successfully!")
            return redirect('savings_goal_list')
    else:
        form = SavingsGoalForm(instance=savings_goal)
    
    return render(request, 'core/savings_goal_form.html', {'form': form, 'action': 'Edit'})

@login_required
def savings_goal_delete_view(request, pk):
    savings_goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        savings_goal.delete()
        messages.success(request, "Savings goal deleted successfully!")
        return redirect('savings_goal_list')
    
    return render(request, 'core/savings_goal_confirm_delete.html', {'savings_goal': savings_goal})

@login_required
def update_savings_view(request, pk):
    savings_goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = UpdateSavingsForm(request.POST, savings_goal=savings_goal)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            # Update the savings goal
            savings_goal.current_amount += amount
            savings_goal.save()
            
            # Create a transaction record for this savings contribution
            category, created = Category.objects.get_or_create(
                name="Savings",
                defaults={
                    'is_expense': True,
                    'icon': 'piggy-bank',
                    'color': '#4CAF50'
                }
            )
            
            Transaction.objects.create(
                user=request.user,
                category=category,
                amount=amount,
                description=f"Contribution to {savings_goal.name}",
                date=timezone.now(),
                is_expense=True
            )
            
            messages.success(request, f"Added Rs. {amount} to {savings_goal.name}!")
            
            # Check if the goal is completed
            if savings_goal.current_amount >= savings_goal.target_amount:
                messages.success(request, f"Congratulations! You've reached your savings goal for {savings_goal.name}!")
                
                # Create an achievement
                Achievement.objects.create(
                    user=request.user,
                    name=f"Savings Goal Achieved: {savings_goal.name}",
                    description=f"Successfully saved Rs. {savings_goal.target_amount} for {savings_goal.name}",
                    icon="trophy",
                    date_earned=timezone.now()
                )
            
            return redirect('savings_goal_list')
    else:
        form = UpdateSavingsForm(savings_goal=savings_goal)
    
    return render(request, 'core/update_savings.html', {'form': form, 'savings_goal': savings_goal})

# Category management
@login_required
def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'core/category_list.html', {'categories': categories})

@login_required
def category_create_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'core/category_form.html', {'form': form, 'action': 'Create'})

@login_required
def category_edit_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'core/category_form.html', {'form': form, 'action': 'Edit'})

# Reports and Analytics
@login_required
def income_expense_report_view(request):
    user = request.user
    
    # Get date range
    now = timezone.now()
    months_back = int(request.GET.get('months', 6))
    start_date = timezone.make_aware(datetime(now.year, now.month, 1) - timedelta(days=30*months_back))
    
    # Get all transactions in date range
    transactions = Transaction.objects.filter(
        user=user,
        date__gte=start_date
    )
    
    # Prepare monthly data
    monthly_data = {}
    current = start_date
    
    while current <= now:
        month_key = f"{current.year}-{current.month:02d}"
        
        # Get month's transactions
        month_start = timezone.make_aware(datetime(current.year, current.month, 1))
        _, last_day = monthrange(current.year, current.month)
        month_end = timezone.make_aware(datetime(current.year, current.month, last_day, 23, 59, 59))
        
        month_income = transactions.filter(
            is_expense=False,
            date__range=(month_start, month_end)
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        month_expenses = transactions.filter(
            is_expense=True,
            date__range=(month_start, month_end)
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        month_savings = month_income - month_expenses
        
        if month_income > 0:
            savings_rate = (month_savings / month_income) * 100
        else:
            savings_rate = 0
        
        monthly_data[month_key] = {
            'month_name': current.strftime('%b %Y'),
            'income': float(month_income),
            'expenses': float(month_expenses),
            'savings': float(month_savings),
            'savings_rate': round(savings_rate, 2)
        }
        
        # Move to next month
        if current.month == 12:
            current = timezone.make_aware(datetime(current.year + 1, 1, 1))
        else:
            current = timezone.make_aware(datetime(current.year, current.month + 1, 1))
    
    # Convert to list for chart.js
    chart_data = {
        'labels': [data['month_name'] for month, data in monthly_data.items()],
        'income': [data['income'] for month, data in monthly_data.items()],
        'expenses': [data['expenses'] for month, data in monthly_data.items()],
        'savings': [data['savings'] for month, data in monthly_data.items()],
        'savings_rate': [data['savings_rate'] for month, data in monthly_data.items()],
    }
    
    # Get category breakdown for current month
    current_month_start = timezone.make_aware(datetime(now.year, now.month, 1))
    _, last_day = monthrange(now.year, now.month)
    current_month_end = timezone.make_aware(datetime(now.year, now.month, last_day, 23, 59, 59))
    
    # Expense categories
    expense_categories = {}
    expense_transactions = transactions.filter(
        is_expense=True,
        date__range=(current_month_start, current_month_end)
    )
    
    for transaction in expense_transactions:
        category_name = transaction.category.name
        if category_name not in expense_categories:
            expense_categories[category_name] = {
                'amount': 0,
                'color': transaction.category.color
            }
        expense_categories[category_name]['amount'] += float(transaction.amount)
    
    # Income categories
    income_categories = {}
    income_transactions = transactions.filter(
        is_expense=False,
        date__range=(current_month_start, current_month_end)
    )
    
    for transaction in income_transactions:
        category_name = transaction.category.name
        if category_name not in income_categories:
            income_categories[category_name] = {
                'amount': 0,
                'color': transaction.category.color
            }
        income_categories[category_name]['amount'] += float(transaction.amount)
    
    # Prepare category data for charts
    expense_chart_data = {
        'labels': list(expense_categories.keys()),
        'data': [category['amount'] for category in expense_categories.values()],
        'colors': [category['color'] for category in expense_categories.values()]
    }
    
    income_chart_data = {
        'labels': list(income_categories.keys()),
        'data': [category['amount'] for category in income_categories.values()],
        'colors': [category['color'] for category in income_categories.values()]
    }
    
    context = {
        'months_options': [3, 6, 12],
        'selected_months': months_back,
        'chart_data': json.dumps(chart_data),
        'expense_chart_data': json.dumps(expense_chart_data),
        'income_chart_data': json.dumps(income_chart_data)
    }
    
    return render(request, 'core/income_expense_report.html', context)

# For debugging URLs
def debug_urls(request):
    """Debug view to show all available URLs"""
    from django.urls import get_resolver
    resolver = get_resolver()
    url_patterns = []
    
    def collect_urls(patterns, parent_pattern=''):
        for pattern in patterns:
            if hasattr(pattern, 'pattern'):
                sub_pattern = pattern.pattern
                if hasattr(sub_pattern, '_route'):
                    route = parent_pattern + sub_pattern._route
                    if hasattr(pattern, 'name') and pattern.name:
                        url_patterns.append({
                            'route': route,
                            'name': pattern.name,
                            'view': pattern.callback.__name__ if callable(pattern.callback) else str(pattern.callback)
                        })
                
                if hasattr(pattern, 'url_patterns'):
                    collect_urls(pattern.url_patterns, route)
    
    collect_urls(resolver.url_patterns)
    
    # Sort URLs alphabetically
    url_patterns.sort(key=lambda x: x['route'])
    
    return render(request, 'debug_urls.html', {'urls': url_patterns})
