from django.shortcuts import render

# Create your views here.

def home(request):
    """View for homepage"""
    return render(request, 'home.html')

def dashboard(request):
    """View for the main dashboard"""
    return render(request, 'dashboard.html')
