from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    """Category for transactions (e.g., Food, Transport)"""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    color = models.CharField(max_length=20, help_text="Hex color code", default="#4361ee")
    is_expense = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extended user profile with financial settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    emergency_fund_goal = models.DecimalField(max_digits=10, decimal_places=2, default=5000)
    preferred_currency = models.CharField(max_length=3, default="Rs.")
    dark_mode = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def calculate_savings(self, year=None, month=None):
        """Calculate user's total savings"""
        if year and month:
            # Calculate for specific month
            income = Transaction.objects.filter(
                user=self.user, 
                is_expense=False,
                date__year=year,
                date__month=month
            ).aggregate(models.Sum('amount'))['amount__sum'] or 0
            
            expenses = Transaction.objects.filter(
                user=self.user, 
                is_expense=True,
                date__year=year,
                date__month=month
            ).aggregate(models.Sum('amount'))['amount__sum'] or 0
        else:
            # Calculate total
            income = Transaction.objects.filter(
                user=self.user, 
                is_expense=False
            ).aggregate(models.Sum('amount'))['amount__sum'] or 0
            
            expenses = Transaction.objects.filter(
                user=self.user, 
                is_expense=True
            ).aggregate(models.Sum('amount'))['amount__sum'] or 0
        
        return income - expenses

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when a User is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    instance.profile.save()

class Transaction(models.Model):
    """Individual financial transaction"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    is_expense = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        transaction_type = "Expense" if self.is_expense else "Income"
        return f"{transaction_type}: {self.amount} for {self.description}"

class Budget(models.Model):
    """Monthly budget for a specific category"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    
    class Meta:
        unique_together = ['user', 'category', 'month', 'year']
    
    def __str__(self):
        return f"{self.user.username}'s budget for {self.category.name} ({self.month}/{self.year})"
    
    def get_spent_amount(self):
        """Calculate how much has been spent in this category this month"""
        return Transaction.objects.filter(
            user=self.user,
            category=self.category,
            is_expense=True,
            date__year=self.year,
            date__month=self.month
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    def get_percentage(self):
        """Calculate percentage of budget used"""
        spent = self.get_spent_amount()
        if self.amount > 0:
            return int((spent / self.amount) * 100)
        return 0

class SavingsGoal(models.Model):
    """Savings goal for user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_goals')
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.current_amount}/{self.target_amount}"
    
    def get_percentage(self):
        """Calculate percentage of savings goal achieved"""
        if self.target_amount > 0:
            return int((self.current_amount / self.target_amount) * 100)
        return 0
    
    def get_status(self):
        """Get the status of the savings goal"""
        percentage = self.get_percentage()
        
        if self.is_completed:
            return "Completed"
        
        if not self.target_date:
            if percentage < 25:
                return "Behind"
            else:
                return "On Track"
        
        # Calculate based on time remaining
        today = timezone.now().date()
        # Convert target_date to date if it's a datetime
        target_date = self.target_date
        if hasattr(target_date, 'date'):
            target_date = target_date.date()
        
        if today > target_date:
            return "Overdue"
        
        # Since we don't have a created_date field, we'll assume the goal was created
        # a reasonable time ago and just focus on how close we are to the target date and amount
        if percentage >= 50:
            return "On Track"
        elif percentage >= 25:
            return "Slightly Behind"
        else:
            return "Behind"

class Achievement(models.Model):
    """User achievements and badges"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    date_earned = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} earned {self.name}"
