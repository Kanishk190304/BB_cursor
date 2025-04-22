from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Transaction, Budget, Category, SavingsGoal
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    """Enhanced user registration form"""
    email = forms.EmailField(required=True)
    monthly_income = forms.DecimalField(max_digits=10, decimal_places=2, required=False, 
                                        help_text="Enter your monthly income")
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
            # Update the user profile with additional data
            if "monthly_income" in self.cleaned_data and self.cleaned_data["monthly_income"]:
                user.profile.monthly_income = self.cleaned_data["monthly_income"]
                user.profile.save()
        
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """Enhanced login form with Bootstrap styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

class UserProfileForm(forms.ModelForm):
    """Form for editing user profile information"""
    
    class Meta:
        model = UserProfile
        fields = ['monthly_income', 'emergency_fund_goal', 'preferred_currency', 'dark_mode']
        widgets = {
            'monthly_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'emergency_fund_goal': forms.NumberInput(attrs={'class': 'form-control'}),
            'preferred_currency': forms.Select(attrs={'class': 'form-control'}),
            'dark_mode': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TransactionForm(forms.ModelForm):
    """Form for adding/editing financial transactions"""
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter categories by user and transaction type
        if self.user:
            self.fields['category'].queryset = Category.objects.all()  # We'll filter in the view
    
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'category', 'date', 'is_expense']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_expense': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BudgetForm(forms.ModelForm):
    """Form for setting monthly budget categories"""
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only show expense categories for budgets
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(is_expense=True)
        
        # Set default month/year to current
        now = timezone.now()
        if not self.instance.pk:  # If creating new budget
            self.initial['month'] = now.month
            self.initial['year'] = now.year
    
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 2000, 'max': 2100}),
        }

class SavingsGoalForm(forms.ModelForm):
    """Form for creating savings goals"""
    
    class Meta:
        model = SavingsGoal
        fields = ['name', 'target_amount', 'current_amount', 'target_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class UpdateSavingsForm(forms.Form):
    """Form for updating progress towards a savings goal"""
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    def __init__(self, *args, **kwargs):
        self.savings_goal = kwargs.pop('savings_goal', None)
        super().__init__(*args, **kwargs)
        
        if self.savings_goal:
            remaining = self.savings_goal.target_amount - self.savings_goal.current_amount
            self.fields['amount'].help_text = f"Remaining: Rs. {remaining}"

class CategoryForm(forms.ModelForm):
    """Form for creating custom expense/income categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'icon', 'color', 'is_expense']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'is_expense': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        } 