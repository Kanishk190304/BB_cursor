from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard and Profile
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # Transactions
    path('transactions/', views.transaction_list_view, name='transactions'),
    path('transactions/add/', views.transaction_create_view, name='add_transaction'),
    path('transactions/<int:pk>/edit/', views.transaction_edit_view, name='edit_transaction'),
    path('transactions/<int:pk>/delete/', views.transaction_delete_view, name='delete_transaction'),
    
    # Budgets
    path('budgets/', views.budget_list_view, name='budgets'),
    path('budgets/add/', views.budget_create_view, name='add_budget'),
    path('budgets/<int:pk>/edit/', views.budget_edit_view, name='edit_budget'),
    path('budgets/<int:pk>/delete/', views.budget_delete_view, name='delete_budget'),
    
    # Savings Goals
    path('savings/', views.savings_goal_list_view, name='savings'),
    path('savings/add/', views.savings_goal_create_view, name='add_savings_goal'),
    path('savings/<int:pk>/edit/', views.savings_goal_edit_view, name='edit_savings_goal'),
    path('savings/<int:pk>/delete/', views.savings_goal_delete_view, name='delete_savings_goal'),
    path('savings/<int:pk>/update/', views.update_savings_view, name='update_savings'),
    
    # Categories
    path('categories/', views.category_list_view, name='categories'),
    path('categories/add/', views.category_create_view, name='add_category'),
    path('categories/<int:pk>/edit/', views.category_edit_view, name='edit_category'),
    path('categories/<int:pk>/delete/', views.category_delete_view, name='delete_category'),
    
    # Reports
    path('reports/income-expense/', views.income_expense_report_view, name='income_expense_report'),
    
    # Debug
    path('debug/urls/', views.debug_urls, name='debug_urls'),
] 