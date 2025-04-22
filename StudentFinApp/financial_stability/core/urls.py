from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard and profile
    path('', views.dashboard_view, name='dashboard'),
    path('home/', views.dashboard_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    
    # Transactions
    path('transactions/', views.transaction_list_view, name='transactions'),
    path('transactions/add/', views.transaction_create_view, name='add_transaction'),
    path('transactions/<int:pk>/edit/', views.transaction_edit_view, name='transaction_edit'),
    path('transactions/<int:pk>/delete/', views.transaction_delete_view, name='transaction_delete'),
    
    # Budgets
    path('budgets/', views.budget_list_view, name='budgets'),
    path('budgets/add/', views.budget_create_view, name='add_budget'),
    path('budgets/<int:pk>/edit/', views.budget_edit_view, name='budget_edit'),
    path('budgets/<int:pk>/delete/', views.budget_delete_view, name='budget_delete'),
    
    # Savings Goals
    path('savings/', views.savings_goal_list_view, name='savings'),
    path('savings/add/', views.savings_goal_create_view, name='add_savings'),
    path('savings/<int:pk>/edit/', views.savings_goal_edit_view, name='savings_goal_edit'),
    path('savings/<int:pk>/delete/', views.savings_goal_delete_view, name='savings_goal_delete'),
    path('savings/<int:pk>/update/', views.update_savings_view, name='update_savings'),
    
    # Categories
    path('categories/', views.category_list_view, name='categories'),
    path('categories/add/', views.category_create_view, name='add_category'),
    path('categories/<int:pk>/edit/', views.category_edit_view, name='category_edit'),
    
    # Reports and Analytics
    path('reports/income-expense/', views.income_expense_report_view, name='income_expense_report'),
] 