from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.http import JsonResponse
from .models import Orders, MenuItem


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


def create_order(request):
    if request.method == 'POST':
        try:
            # Extract data from the POST request
            customer = request.user  # Assuming the user is authenticated
            payment_method = request.POST.get('payment_method')
            menu_item_ids = request.POST.getlist('menu_items')  # List of item IDs

            # Validate the payment method
            if payment_method not in dict(Orders.PAYMENT_CHOICES):
                return JsonResponse({'error': 'Invalid payment method'}, status=400)

            # Fetch the menu items
            menu_items = MenuItem.objects.filter(id__in=menu_item_ids)
            if not menu_items.exists():
                return JsonResponse({'error': 'Invalid menu items'}, status=400)

            # Create the order
            order = Orders.objects.create(
                customer=customer,
                payment_method=payment_method,
            )
            order.items.set(menu_items)  # Assuming a Many-to-Many field for items
            order.save()

            return JsonResponse({'message': 'Order created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def orders_dashboard_data(request):
    # Fetch all orders (modify the query as needed)
    orders = Orders.objects.all()

    # Serialize orders into a JSON-friendly format
    orders_data = [
        {
            'id': order.id,
            'customer': str(order.customer),  # Assuming the customer field is a ForeignKey
            'payment_method': order.get_payment_method_display(),
            'date': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for order in orders
    ]

    return JsonResponse({'orders': orders_data}, safe=False)
