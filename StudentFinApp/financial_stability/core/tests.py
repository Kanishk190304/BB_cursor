from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import datetime

from .models import (
    Category, 
    UserProfile, 
    Transaction, 
    Budget, 
    SavingsGoal, 
    Achievement
)
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

class ModelTests(TestCase):
    """Tests for core application models"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create test categories
        self.income_category = Category.objects.create(
            name='Salary',
            icon='money',
            color='#00ff00',
            is_expense=False
        )
        
        self.expense_category = Category.objects.create(
            name='Food',
            icon='food',
            color='#ff0000',
            is_expense=True
        )
        
        # Create test transactions
        self.income_transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('1000.00'),
            description='Monthly salary',
            category=self.income_category,
            date=timezone.now(),
            is_expense=False
        )
        
        self.expense_transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('200.00'),
            description='Groceries',
            category=self.expense_category,
            date=timezone.now(),
            is_expense=True
        )
        
        # Create test budget
        self.budget = Budget.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('300.00'),
            month=timezone.now().month,
            year=timezone.now().year
        )
        
        # Create test savings goal
        self.savings_goal = SavingsGoal.objects.create(
            user=self.user,
            name='Vacation',
            target_amount=Decimal('5000.00'),
            current_amount=Decimal('1000.00'),
            target_date=timezone.now() + datetime.timedelta(days=90)
        )
    
    def test_category_str(self):
        self.assertEqual(str(self.income_category), 'Salary')
    
    def test_user_profile_created(self):
        """Test that a UserProfile is automatically created when a User is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
    
    def test_transaction_str(self):
        self.assertEqual(
            str(self.income_transaction),
            f'Rs. 1000.00 - Monthly salary'
        )
    
    def test_budget_get_spent_amount(self):
        """Test the get_spent_amount method of Budget"""
        spent = self.budget.get_spent_amount()
        self.assertEqual(spent, Decimal('200.00'))
    
    def test_budget_get_percentage(self):
        """Test the get_percentage method of Budget"""
        percentage = self.budget.get_percentage()
        # 200/300 = 66.67%
        self.assertAlmostEqual(float(percentage), 66.67, places=2)
    
    def test_savings_goal_get_percentage(self):
        """Test the get_percentage method of SavingsGoal"""
        percentage = self.savings_goal.get_percentage()
        # 1000/5000 = 20%
        self.assertEqual(percentage, 20)
    
    def test_savings_goal_get_status(self):
        """Test the get_status method of SavingsGoal"""
        status = self.savings_goal.get_status()
        self.assertEqual(status, 'in_progress')
        
        # Test 'completed' status
        self.savings_goal.current_amount = self.savings_goal.target_amount
        self.savings_goal.save()
        self.assertEqual(self.savings_goal.get_status(), 'completed')
        
        # Test 'overdue' status
        self.savings_goal.current_amount = Decimal('2500.00')
        self.savings_goal.target_date = timezone.now() - datetime.timedelta(days=1)
        self.savings_goal.save()
        self.assertEqual(self.savings_goal.get_status(), 'overdue')
    
    def test_user_profile_calculate_savings(self):
        """Test the calculate_savings method of UserProfile"""
        savings = self.user.profile.calculate_savings()
        # Income 1000 - Expense 200 = 800
        self.assertEqual(savings, Decimal('800.00'))


class FormTests(TestCase):
    """Tests for core application forms"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create test categories
        self.income_category = Category.objects.create(
            name='Salary',
            icon='money',
            color='#00ff00',
            is_expense=False
        )
        
        self.expense_category = Category.objects.create(
            name='Food',
            icon='food',
            color='#ff0000',
            is_expense=True
        )
    
    def test_custom_user_creation_form_valid_data(self):
        form = CustomUserCreationForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
            'monthly_income': '5000.00'
        })
        self.assertTrue(form.is_valid())
    
    def test_custom_user_creation_form_invalid_data(self):
        form = CustomUserCreationForm(data={
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'complex_password123',
            'password2': 'different_password',
        })
        self.assertFalse(form.is_valid())
    
    def test_transaction_form_valid_data(self):
        form = TransactionForm(
            user=self.user,
            data={
                'amount': '100.00',
                'description': 'Test transaction',
                'category': self.expense_category.id,
                'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
                'is_expense': True
            }
        )
        self.assertTrue(form.is_valid())
    
    def test_budget_form_valid_data(self):
        form = BudgetForm(
            user=self.user,
            data={
                'category': self.expense_category.id,
                'amount': '300.00',
                'month': timezone.now().month,
                'year': timezone.now().year
            }
        )
        self.assertTrue(form.is_valid())
    
    def test_savings_goal_form_valid_data(self):
        form = SavingsGoalForm(data={
            'name': 'Test Goal',
            'target_amount': '1000.00',
            'current_amount': '200.00',
            'target_date': (timezone.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        })
        self.assertTrue(form.is_valid())
    
    def test_category_form_valid_data(self):
        form = CategoryForm(data={
            'name': 'Entertainment',
            'icon': 'movie',
            'color': '#0000ff',
            'is_expense': True
        })
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    """Tests for core application views"""
    
    def setUp(self):
        # Create test client
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create test categories
        self.income_category = Category.objects.create(
            name='Salary',
            icon='money',
            color='#00ff00',
            is_expense=False
        )
        
        self.expense_category = Category.objects.create(
            name='Food',
            icon='food',
            color='#ff0000',
            is_expense=True
        )
        
        # Create test transactions
        self.income_transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('1000.00'),
            description='Monthly salary',
            category=self.income_category,
            date=timezone.now(),
            is_expense=False
        )
        
        self.expense_transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('200.00'),
            description='Groceries',
            category=self.expense_category,
            date=timezone.now(),
            is_expense=True
        )
        
        # Create test budget
        self.budget = Budget.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('300.00'),
            month=timezone.now().month,
            year=timezone.now().year
        )
        
        # Create test savings goal
        self.savings_goal = SavingsGoal.objects.create(
            user=self.user,
            name='Vacation',
            target_amount=Decimal('5000.00'),
            current_amount=Decimal('1000.00'),
            target_date=timezone.now() + datetime.timedelta(days=90)
        )
        
        # Login URLs
        self.login_url = reverse('login')
        
        # URLs requiring authentication
        self.dashboard_url = reverse('dashboard')
        self.profile_url = reverse('profile')
        self.transactions_url = reverse('transactions')
        self.add_transaction_url = reverse('add_transaction')
        self.budget_url = reverse('budgets')
        self.add_budget_url = reverse('add_budget')
        self.savings_url = reverse('savings')
        self.add_savings_url = reverse('add_savings')
        self.categories_url = reverse('categories')
        self.add_category_url = reverse('add_category')
        self.reports_url = reverse('income_expense_report')
    
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/register.html')
    
    def test_register_view_post(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
            'monthly_income': '5000.00'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertEqual(User.objects.count(), 2)  # Original user + new user
    
    def test_login_view(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.url.endswith(reverse('dashboard')))
    
    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertTrue(response.url.endswith(reverse('login')))
    
    def test_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/dashboard.html')
        self.assertContains(response, 'Recent Transactions')
        self.assertContains(response, 'Budget Overview')
    
    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/profile.html')
    
    def test_profile_view_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_transaction_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.transactions_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/transactions.html')
    
    def test_transaction_list_view_unauthenticated(self):
        response = self.client.get(self.transactions_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_transaction_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.add_transaction_url, {
            'amount': '50.00',
            'description': 'Test transaction',
            'category': self.expense_category.id,
            'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'is_expense': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)  # Original + new transaction
    
    def test_transaction_create_view_unauthenticated(self):
        response = self.client.post(self.add_transaction_url, {
            'amount': '50.00',
            'description': 'Test transaction',
            'category': self.expense_category.id,
            'date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'is_expense': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_budget_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.budget_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/budgets.html')
    
    def test_budget_list_view_unauthenticated(self):
        response = self.client.get(self.budget_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_budget_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.add_budget_url, {
            'category': self.expense_category.id,
            'amount': '200.00',
            'month': timezone.now().month,
            'year': timezone.now().year
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Budget.objects.filter(user=self.user).count(), 2)  # Original + new budget
    
    def test_budget_create_view_unauthenticated(self):
        response = self.client.post(self.add_budget_url, {
            'category': self.expense_category.id,
            'amount': '200.00',
            'month': timezone.now().month,
            'year': timezone.now().year
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_savings_goal_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.savings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/savings.html')
    
    def test_savings_goal_list_view_unauthenticated(self):
        response = self.client.get(self.savings_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_savings_goal_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.add_savings_url, {
            'name': 'New Goal',
            'target_amount': '2000.00',
            'current_amount': '0.00',
            'target_date': (timezone.now() + datetime.timedelta(days=60)).strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(SavingsGoal.objects.filter(user=self.user).count(), 2)  # Original + new goal
    
    def test_savings_goal_create_view_unauthenticated(self):
        response = self.client.post(self.add_savings_url, {
            'name': 'New Goal',
            'target_amount': '2000.00',
            'current_amount': '0.00',
            'target_date': (timezone.now() + datetime.timedelta(days=60)).strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_update_savings_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('update_savings', args=[self.savings_goal.id]), {
            'current_amount': '1500.00'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.savings_goal.refresh_from_db()
        self.assertEqual(self.savings_goal.current_amount, Decimal('1500.00'))
    
    def test_update_savings_view_unauthenticated(self):
        response = self.client.post(reverse('update_savings', args=[self.savings_goal.id]), {
            'current_amount': '1500.00'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_category_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/categories.html')
    
    def test_category_list_view_unauthenticated(self):
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_category_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.add_category_url, {
            'name': 'New Category',
            'icon': 'music',
            'color': '#0000ff',
            'is_expense': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Category.objects.count(), 3)  # Original 2 + new category
    
    def test_category_create_view_unauthenticated(self):
        response = self.client.post(self.add_category_url, {
            'name': 'New Category',
            'icon': 'music',
            'color': '#0000ff',
            'is_expense': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_income_expense_report_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.reports_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/reports.html')
    
    def test_income_expense_report_view_unauthenticated(self):
        response = self.client.get(self.reports_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(self.login_url))
    
    def test_transaction_create_view(self):
        # Create a test user and login
        self.client.login(username='testuser', password='testpassword123')
        
        # Get a sample category
        category = Category.objects.get(name='Food')
        
        # Test GET request
        response = self.client.get(reverse('add_transaction'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/transaction_form.html')
        
        # Test POST request with valid data
        transaction_data = {
            'description': 'Test transaction',
            'amount': 50.00,
            'transaction_type': 'expense',
            'category': category.id,
            'date': timezone.now().date().isoformat()
        }
        
        response = self.client.post(reverse('add_transaction'), transaction_data)
        self.assertEqual(response.status_code, 302)  # Redirects after successful creation
        
        # Verify that the transaction was created
        self.assertTrue(Transaction.objects.filter(description='Test transaction').exists())
        
        # Test POST request with invalid data
        invalid_data = {
            'description': '',  # Empty description
            'amount': 'not-a-number',
            'transaction_type': 'expense',
            'category': category.id,
            'date': timezone.now().date().isoformat()
        }
        
        response = self.client.post(reverse('add_transaction'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Returns to form with errors
        self.assertFalse(Transaction.objects.filter(amount='not-a-number').exists())
    
    def test_transaction_edit_view(self):
        # Create a test user and login
        self.client.login(username='testuser', password='testpassword123')
        
        # Get a sample category
        category = Category.objects.get(name='Food')
        
        # Create a test transaction to edit
        test_transaction = Transaction.objects.create(
            user=self.user,
            description='Original transaction',
            amount=100.00,
            transaction_type='expense',
            category=category,
            date=timezone.now().date()
        )
        
        # Test GET request to edit form
        response = self.client.get(reverse('edit_transaction', args=[test_transaction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/transaction_form.html')
        
        # Test POST request with valid update data
        updated_data = {
            'description': 'Updated transaction',
            'amount': 75.00,
            'transaction_type': 'expense',
            'category': category.id,
            'date': timezone.now().date().isoformat()
        }
        
        response = self.client.post(reverse('edit_transaction', args=[test_transaction.id]), updated_data)
        self.assertEqual(response.status_code, 302)  # Redirects after successful update
        
        # Verify that the transaction was updated
        test_transaction.refresh_from_db()
        self.assertEqual(test_transaction.description, 'Updated transaction')
        self.assertEqual(test_transaction.amount, 75.00)
        
        # Test editing a non-existent transaction
        response = self.client.get(reverse('edit_transaction', args=[9999]))
        self.assertEqual(response.status_code, 404)
        
        # Test editing another user's transaction
        other_user = User.objects.create_user(username='otheruser', password='testpassword123')
        other_transaction = Transaction.objects.create(
            user=other_user,
            description='Other user transaction',
            amount=50.00,
            transaction_type='expense',
            category=category,
            date=timezone.now().date()
        )
        
        response = self.client.get(reverse('edit_transaction', args=[other_transaction.id]))
        self.assertEqual(response.status_code, 404)  # Should return 404 for security
    
    def test_transaction_delete_view(self):
        # Create a test user and login
        self.client.login(username='testuser', password='testpassword123')
        
        # Get a sample category
        category = Category.objects.get(name='Food')
        
        # Create a test transaction to delete
        test_transaction = Transaction.objects.create(
            user=self.user,
            description='Transaction to delete',
            amount=25.00,
            transaction_type='expense',
            category=category,
            date=timezone.now().date()
        )
        
        # Confirm transaction exists
        self.assertTrue(Transaction.objects.filter(id=test_transaction.id).exists())
        
        # Test GET request to delete confirmation page
        response = self.client.get(reverse('delete_transaction', args=[test_transaction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/transaction_confirm_delete.html')
        
        # Test POST request to delete transaction
        response = self.client.post(reverse('delete_transaction', args=[test_transaction.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion
        
        # Verify that the transaction was deleted
        self.assertFalse(Transaction.objects.filter(id=test_transaction.id).exists())
        
        # Test deleting a non-existent transaction
        response = self.client.get(reverse('delete_transaction', args=[9999]))
        self.assertEqual(response.status_code, 404)
        
        # Test deleting another user's transaction
        other_user = User.objects.create_user(username='otheruser2', password='testpassword123')
        other_transaction = Transaction.objects.create(
            user=other_user,
            description='Other user transaction to delete',
            amount=75.00,
            transaction_type='expense',
            category=category,
            date=timezone.now().date()
        )
        
        response = self.client.get(reverse('delete_transaction', args=[other_transaction.id]))
        self.assertEqual(response.status_code, 404)  # Should return 404 for security
    
    def test_transaction_filter_functionality(self):
        # Create a test user and login
        self.client.login(username='testuser', password='testpassword123')
        
        # Get sample categories
        food_category = Category.objects.get(name='Food')
        entertainment_category = Category.objects.get(name='Entertainment')
        
        # Create test transactions with different categories, types and dates
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        last_month = today - timezone.timedelta(days=30)
        
        # Create food expense transaction
        Transaction.objects.create(
            user=self.user,
            description='Grocery shopping',
            amount=50.00,
            transaction_type='expense',
            category=food_category,
            date=today
        )
        
        # Create entertainment expense transaction
        Transaction.objects.create(
            user=self.user,
            description='Movie tickets',
            amount=25.00,
            transaction_type='expense',
            category=entertainment_category,
            date=yesterday
        )
        
        # Create income transaction
        Transaction.objects.create(
            user=self.user,
            description='Part-time job',
            amount=200.00,
            transaction_type='income',
            category=None,
            date=last_month
        )
        
        # Test filtering by transaction type (expense)
        response = self.client.get(reverse('transactions'), {'transaction_type': 'expense'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 2)  # Should return both expense transactions
        
        # Test filtering by transaction type (income)
        response = self.client.get(reverse('transactions'), {'transaction_type': 'income'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 1)  # Should return one income transaction
        
        # Test filtering by category
        response = self.client.get(reverse('transactions'), {'category': food_category.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 1)  # Should return one food transaction
        
        # Test filtering by date range
        start_date = (yesterday - timezone.timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
        response = self.client.get(reverse('transactions'), {'start_date': start_date, 'end_date': end_date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 2)  # Should return today's and yesterday's transactions
        
        # Test combined filters (expense + food category)
        response = self.client.get(reverse('transactions'), 
                                  {'transaction_type': 'expense', 'category': food_category.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 1)  # Should return only the food expense
    
    def test_budget_progress_calculation(self):
        # Create a test user and login
        self.client.login(username='testuser', password='testpassword123')
        
        # Get a sample category
        food_category = Category.objects.get(name='Food')
        
        # Create a test budget for the current month
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        test_budget = Budget.objects.create(
            user=self.user,
            category=food_category,
            amount=300.00,
            month=current_month,
            year=current_year
        )
        
        # Add some transactions for this budget's category
        # Transaction 1 - within budget period
        Transaction.objects.create(
            user=self.user,
            description='Grocery shopping',
            amount=100.00,
            transaction_type='expense',
            category=food_category,
            date=timezone.datetime(current_year, current_month, 15).date()
        )
        
        # Transaction 2 - within budget period
        Transaction.objects.create(
            user=self.user,
            description='Restaurant dinner',
            amount=50.00,
            transaction_type='expense',
            category=food_category,
            date=timezone.datetime(current_year, current_month, 20).date()
        )
        
        # Transaction 3 - previous month (should not count toward current budget)
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_year = current_year if current_month > 1 else current_year - 1
        Transaction.objects.create(
            user=self.user,
            description='Last month groceries',
            amount=75.00,
            transaction_type='expense',
            category=food_category,
            date=timezone.datetime(previous_year, previous_month, 15).date()
        )
        
        # Access the dashboard to trigger budget progress calculation
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Check if budget is in the context
        self.assertIn('budgets', response.context)
        
        # Calculate expected values
        expected_spent = 150.00  # 100 + 50
        expected_remaining = 150.00  # 300 - 150
        expected_percentage = 50  # (150/300) * 100
        
        # Find our test budget in the context
        context_budget = None
        for budget in response.context['budgets']:
            if budget['id'] == test_budget.id:
                context_budget = budget
                break
                
        # Assert budget calculations are correct
        self.assertIsNotNone(context_budget)
        self.assertEqual(context_budget['spent'], expected_spent)
        self.assertEqual(context_budget['remaining'], expected_remaining)
        self.assertEqual(context_budget['percentage'], expected_percentage)
        
        # Verify the progress color is correct (should be 'warning' for 50%)
        self.assertEqual(context_budget['progress_color'], 'warning')
        
        # Add another transaction to exceed the budget
        Transaction.objects.create(
            user=self.user,
            description='Expensive dinner',
            amount=200.00,
            transaction_type='expense',
            category=food_category,
            date=timezone.datetime(current_year, current_month, 25).date()
        )
        
        # Access the dashboard again
        response = self.client.get(reverse('dashboard'))
        
        # Find our test budget in the updated context
        context_budget = None
        for budget in response.context['budgets']:
            if budget['id'] == test_budget.id:
                context_budget = budget
                break
                
        # Calculate new expected values
        expected_spent = 350.00  # 100 + 50 + 200
        expected_remaining = -50.00  # 300 - 350
        expected_percentage = 116.67  # (350/300) * 100
        
        # Assert updated calculations are correct
        self.assertIsNotNone(context_budget)
        self.assertEqual(context_budget['spent'], expected_spent)
        self.assertEqual(context_budget['remaining'], expected_remaining)
        self.assertAlmostEqual(context_budget['percentage'], expected_percentage, places=2)
        
        # Verify the progress color is 'danger' when over budget
        self.assertEqual(context_budget['progress_color'], 'danger')

    def test_savings_goal_progress_calculation(self):
        # Create a test user and login
        self.client.login(username='testuser', password='testpassword123')
        
        # Create a test savings goal
        target_date = timezone.now().date() + timezone.timedelta(days=60)
        test_goal = SavingsGoal.objects.create(
            user=self.user,
            name='New Laptop',
            target_amount=1000.00,
            current_amount=0.00,
            target_date=target_date
        )
        
        # Access the savings goals page to verify initial state
        response = self.client.get(reverse('savings_goals'))
        self.assertEqual(response.status_code, 200)
        
        # Check if savings goal is in the context
        self.assertIn('savings_goals', response.context)
        self.assertEqual(len(response.context['savings_goals']), 1)
        
        # Verify initial progress is 0%
        goal = response.context['savings_goals'][0]
        self.assertEqual(goal.id, test_goal.id)
        self.assertEqual(goal.current_amount, 0.00)
        self.assertEqual(goal.progress, 0)
        
        # Update the savings goal with a contribution
        response = self.client.post(
            reverse('update_savings_goal', args=[test_goal.id]),
            {
                'name': 'New Laptop',
                'target_amount': 1000.00,
                'current_amount': 250.00,
                'target_date': target_date.strftime('%Y-%m-%d')
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Refresh the savings goal from the database
        test_goal.refresh_from_db()
        self.assertEqual(test_goal.current_amount, 250.00)
        
        # Access the savings goals page again
        response = self.client.get(reverse('savings_goals'))
        
        # Check updated progress
        goal = None
        for g in response.context['savings_goals']:
            if g.id == test_goal.id:
                goal = g
                break
                
        self.assertIsNotNone(goal)
        self.assertEqual(goal.current_amount, 250.00)
        self.assertEqual(goal.progress, 25)  # 25% progress (250/1000 * 100)
        
        # Add another contribution to reach 75%
        response = self.client.post(
            reverse('update_savings_goal', args=[test_goal.id]),
            {
                'name': 'New Laptop',
                'target_amount': 1000.00,
                'current_amount': 750.00,
                'target_date': target_date.strftime('%Y-%m-%d')
            }
        )
        
        # Access the savings goals page again
        response = self.client.get(reverse('savings_goals'))
        
        # Find our test goal in the context
        goal = None
        for g in response.context['savings_goals']:
            if g.id == test_goal.id:
                goal = g
                break
                
        # Verify progress is now 75%
        self.assertIsNotNone(goal)
        self.assertEqual(goal.current_amount, 750.00)
        self.assertEqual(goal.progress, 75)  # 75% progress
        
        # Complete the goal (100%)
        response = self.client.post(
            reverse('update_savings_goal', args=[test_goal.id]),
            {
                'name': 'New Laptop',
                'target_amount': 1000.00,
                'current_amount': 1000.00,
                'target_date': target_date.strftime('%Y-%m-%d')
            }
        )
        
        # Access the savings goals page again
        response = self.client.get(reverse('savings_goals'))
        
        # Find our test goal in the context
        goal = None
        for g in response.context['savings_goals']:
            if g.id == test_goal.id:
                goal = g
                break
                
        # Verify goal is now complete (100%)
        self.assertIsNotNone(goal)
        self.assertEqual(goal.current_amount, 1000.00)
        self.assertEqual(goal.progress, 100)  # 100% progress

    def test_transaction_categorization(self):
        # Create a test user and login
        self.client.login(username='testuser', password='testpassword123')
        
        # Get sample categories
        food_category = Category.objects.get(name='Food')
        utilities_category = Category.objects.get(name='Utilities')
        
        # Create a transaction with Food category
        food_transaction = Transaction.objects.create(
            user=self.user,
            description='Grocery Shopping',
            amount=75.50,
            category=food_category,
            transaction_type='expense',
            date=timezone.now().date()
        )
        
        # Create another transaction with Utilities category
        utility_transaction = Transaction.objects.create(
            user=self.user,
            description='Electricity Bill',
            amount=120.75,
            category=utilities_category,
            transaction_type='expense',
            date=timezone.now().date()
        )
        
        # Access the transactions page
        response = self.client.get(reverse('transactions'))
        self.assertEqual(response.status_code, 200)
        
        # Check if transactions are in the context and correctly categorized
        self.assertIn('transactions', response.context)
        transactions = response.context['transactions']
        self.assertEqual(len(transactions), 2)
        
        # Verify each transaction has the correct category
        for transaction in transactions:
            if transaction.id == food_transaction.id:
                self.assertEqual(transaction.category, food_category)
                self.assertEqual(transaction.category.name, 'Food')
            elif transaction.id == utility_transaction.id:
                self.assertEqual(transaction.category, utilities_category)
                self.assertEqual(transaction.category.name, 'Utilities')
        
        # Test filtering transactions by category
        response = self.client.get(f"{reverse('transactions')}?category={food_category.id}")
        self.assertEqual(response.status_code, 200)
        
        # Check that only food transactions are returned
        filtered_transactions = response.context['transactions']
        self.assertEqual(len(filtered_transactions), 1)
        self.assertEqual(filtered_transactions[0].id, food_transaction.id)
        self.assertEqual(filtered_transactions[0].category, food_category)
        
        # Test editing transaction category
        response = self.client.post(
            reverse('edit_transaction', args=[food_transaction.id]),
            {
                'description': 'Grocery Shopping',
                'amount': 75.50,
                'category': utilities_category.id,
                'transaction_type': 'expense',
                'date': food_transaction.date.strftime('%Y-%m-%d')
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Refresh the transaction from the database
        food_transaction.refresh_from_db()
        
        # Verify the category has been updated
        self.assertEqual(food_transaction.category, utilities_category)
        self.assertEqual(food_transaction.category.name, 'Utilities')
        
        # Access the transactions page again with filtering by utilities category
        response = self.client.get(f"{reverse('transactions')}?category={utilities_category.id}")
        
        # Both transactions should now be in utilities category
        filtered_transactions = response.context['transactions']
        self.assertEqual(len(filtered_transactions), 2)

    def test_budget_tracking_and_alerts(self):
        # Create a test user and login
        self.client.login(username='testuser', password='testpassword123')
        
        # Get food category
        food_category = Category.objects.get(name='Food')
        
        # Create a budget for Food category
        food_budget = Budget.objects.create(
            user=self.user,
            category=food_category,
            amount=300.00,
            month=timezone.now().month,
            year=timezone.now().year
        )
        
        # Verify initial budget status
        response = self.client.get(reverse('budgets'))
        self.assertEqual(response.status_code, 200)
        
        # Check if budget is in the context
        self.assertIn('budgets', response.context)
        budgets = response.context['budgets']
        self.assertEqual(len(budgets), 1)
        
        # Verify the budget properties
        budget = budgets[0]
        self.assertEqual(budget.category, food_category)
        self.assertEqual(budget.amount, 300.00)
        self.assertEqual(budget.spent, 0.00)  # No transactions yet
        self.assertEqual(budget.remaining, 300.00)  # Full amount remaining
        self.assertEqual(budget.percentage_used, 0)  # 0% used
        
        # Create a transaction within the budget
        transaction1 = Transaction.objects.create(
            user=self.user,
            description='Grocery Shopping',
            amount=75.50,
            category=food_category,
            transaction_type='expense',
            date=timezone.now().date()
        )
        
        # Check budget after first transaction
        response = self.client.get(reverse('budgets'))
        updated_budget = response.context['budgets'][0]
        self.assertEqual(updated_budget.spent, 75.50)
        self.assertEqual(updated_budget.remaining, 224.50)
        self.assertEqual(updated_budget.percentage_used, 25)  # Approximately 25% used
        
        # Create a second transaction
        transaction2 = Transaction.objects.create(
            user=self.user,
            description='Restaurant Dinner',
            amount=150.00,
            category=food_category,
            transaction_type='expense',
            date=timezone.now().date()
        )
        
        # Check budget after second transaction
        response = self.client.get(reverse('budgets'))
        updated_budget = response.context['budgets'][0]
        self.assertEqual(updated_budget.spent, 225.50)  # 75.50 + 150.00
        self.assertEqual(updated_budget.remaining, 74.50)
        self.assertEqual(updated_budget.percentage_used, 75)  # Approximately 75% used
        
        # Check for warning (over 75% of budget used)
        self.assertIn('budgets_warnings', response.context)
        self.assertEqual(len(response.context['budgets_warnings']), 1)
        
        # Add a third transaction that pushes over budget
        transaction3 = Transaction.objects.create(
            user=self.user,
            description='Snacks',
            amount=100.00,
            category=food_category,
            transaction_type='expense',
            date=timezone.now().date()
        )
        
        # Check budget after third transaction
        response = self.client.get(reverse('budgets'))
        updated_budget = response.context['budgets'][0]
        self.assertEqual(updated_budget.spent, 325.50)  # 75.50 + 150.00 + 100.00
        self.assertEqual(updated_budget.remaining, -25.50)  # Negative remaining
        self.assertEqual(updated_budget.percentage_used, 108)  # Over 100% used
        
        # Check for alerts (over 100% of budget used)
        self.assertIn('budgets_alerts', response.context)
        self.assertEqual(len(response.context['budgets_alerts']), 1)
        
        # Test budget adjustment
        response = self.client.post(
            reverse('edit_budget', args=[food_budget.id]),
            {
                'category': food_category.id,
                'amount': 400.00,
                'month': food_budget.month,
                'year': food_budget.year
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Check updated budget
        response = self.client.get(reverse('budgets'))
        updated_budget = response.context['budgets'][0]
        self.assertEqual(updated_budget.amount, 400.00)
        self.assertEqual(updated_budget.spent, 325.50)
        self.assertEqual(updated_budget.remaining, 74.50)  # Now positive again
        self.assertEqual(updated_budget.percentage_used, 81)  # 81% used

    def test_savings_goals_progress(self):
        # Create a test user and login
        self.client.login(username='testuser', password='testpassword123')
        
        # Create a savings goal
        savings_goal = SavingsGoal.objects.create(
            user=self.user,
            name='Emergency Fund',
            target_amount=1000.00,
            current_amount=200.00,
            target_date=timezone.now().date() + timezone.timedelta(days=90)
        )
        
        # Verify initial savings goal
        response = self.client.get(reverse('savings_goals'))
        self.assertEqual(response.status_code, 200)
        
        # Check if savings goal is in the context
        self.assertIn('savings_goals', response.context)
        goals = response.context['savings_goals']
        self.assertEqual(len(goals), 1)
        
        # Verify the goal properties
        goal = goals[0]
        self.assertEqual(goal.name, 'Emergency Fund')
        self.assertEqual(goal.target_amount, 1000.00)
        self.assertEqual(goal.current_amount, 200.00)
        self.assertEqual(goal.progress_percentage, 20)  # 20% progress
        
        # Test goal contribution
        response = self.client.post(
            reverse('add_to_savings_goal', args=[savings_goal.id]),
            {'amount': 300.00}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful contribution
        
        # Verify updated goal progress
        response = self.client.get(reverse('savings_goals'))
        updated_goal = response.context['savings_goals'][0]
        self.assertEqual(updated_goal.current_amount, 500.00)  # 200 + 300
        self.assertEqual(updated_goal.progress_percentage, 50)  # 50% progress
        
        # Make another contribution
        response = self.client.post(
            reverse('add_to_savings_goal', args=[savings_goal.id]),
            {'amount': 500.00}
        )
        
        # Verify goal is now complete
        response = self.client.get(reverse('savings_goals'))
        completed_goal = response.context['savings_goals'][0]
        self.assertEqual(completed_goal.current_amount, 1000.00)
        self.assertEqual(completed_goal.progress_percentage, 100)  # 100% progress
        self.assertTrue(completed_goal.is_achieved)
        
        # Check completed goals are properly categorized
        self.assertIn('completed_goals', response.context)
        self.assertEqual(len(response.context['completed_goals']), 1)
        self.assertEqual(len(response.context['ongoing_goals']), 0)
        
        # Test editing the goal to increase target
        response = self.client.post(
            reverse('edit_savings_goal', args=[savings_goal.id]),
            {
                'name': 'Emergency Fund',
                'target_amount': 1500.00,
                'target_date': (timezone.now().date() + timezone.timedelta(days=120)).strftime('%Y-%m-%d')
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Verify goal is no longer complete
        response = self.client.get(reverse('savings_goals'))
        updated_goal = response.context['savings_goals'][0]
        self.assertEqual(updated_goal.target_amount, 1500.00)
        self.assertEqual(updated_goal.progress_percentage, 67)  # Approximately 67% progress
        self.assertFalse(updated_goal.is_achieved)
        
        # Check ongoing goals
        self.assertEqual(len(response.context['completed_goals']), 0)
        self.assertEqual(len(response.context['ongoing_goals']), 1)

    def test_achievement_unlock(self):
        """Test the functionality of unlocking achievements"""
        # Create a test user and login
        self.client.login(username='testuser', password='testpassword123')
        
        # Get the initial count of transactions
        initial_transaction_count = Transaction.objects.filter(user=self.user, is_expense=True).count()
        
        # Perform actions that should trigger data tracking (create transactions)
        for i in range(5):
            Transaction.objects.create(
                user=self.user,
                amount=50.00 * (i + 1),
                description=f'Test transaction {i+1}',
                category=self.expense_category,
                date=timezone.now(),
                is_expense=True
            )
            
        # Access the dashboard
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        
        # Check that the dashboard renders properly
        self.assertTemplateUsed(response, 'core/dashboard.html')
        
        # Verify that 5 new transactions were created
        transactions = Transaction.objects.filter(user=self.user, is_expense=True)
        self.assertEqual(transactions.count(), initial_transaction_count + 5)
        
        # Create a savings goal
        savings_goal = SavingsGoal.objects.create(
            user=self.user,
            name='Quick Goal',
            target_amount=1000.00,
            current_amount=0.00,
            target_date=timezone.now().date() + timezone.timedelta(days=30)
        )
        
        # Update the goal to completion
        savings_goal.current_amount = 1000.00
        savings_goal.is_completed = True
        savings_goal.save()
        
        # Verify the goal is properly saved
        updated_goal = SavingsGoal.objects.get(id=savings_goal.id)
        self.assertEqual(updated_goal.current_amount, 1000.00)
        self.assertTrue(updated_goal.is_completed)
        
        # Access the dashboard again to make sure it loads with the updated data
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
