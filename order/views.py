from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Custom template for login page

    def form_valid(self, form):
        # After successful login, we check the user's role
        user = form.get_user()  # Get the logged-in user

        # Redirect based on user role
        if user.role == 'restaurant_manager':
            return redirect('/restaurant_dashboard/')  # Redirect restaurant managers to a custom dashboard
        elif user.role == 'admin':
            return redirect('/admin_dashboard/')  # Redirect admin users to an admin dashboard
        return super().form_valid(form)  # For other users, use the default redirect

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            CustomLoginView(request, user)  # Log the user in immediately after registration
            return redirect('home')  # Redirect to the home page (or any other page you want)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})