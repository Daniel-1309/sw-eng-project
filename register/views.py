from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import UserProfile  

# The login view to handle authentication and role-based redirection
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Use Django's built-in authenticate function to check the credentials
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)

            # Check the user's role and redirect accordingly
            if hasattr(user, 'role'):  # Ensure 'role' attribute exists
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'restaurant_manager':
                    return redirect('restaurant_dashboard')
                else:
                    return redirect('customer_dashboard')
            else:
                # If no role attribute, default to customer dashboard
                return redirect('customer_dashboard')
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid username or password.")
    
    # Render the login page
    return render(request, 'login.html')

# The signup view to handle new user creation
def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')

        # Ensure that the username is unique
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Create the new user instance
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create a UserProfile instance for the user
        profile = UserProfile.objects.create(user=user, address=address, phone_number=phone_number, role=role)

        messages.success(request, "Your account has been created. You can now log in.")
        return redirect('login')
    
    return render(request, 'signup.html')

# Dashboard view for customers
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

# Dashboard view for restaurant managers
def restaurant_dashboard(request):
    return render(request, 'restaurant_dashboard.html')

# Dashboard view for admins
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
