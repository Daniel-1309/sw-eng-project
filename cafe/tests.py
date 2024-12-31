from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from cafe.models import menu_item, order, rating, bill
from datetime import datetime, timedelta
import json

User = get_user_model()

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test user
        self.user = User.objects.create_user(phone='1234567890', password='password123', first_name='Test', last_name='User')
        self.admin_user = User.objects.create_superuser(phone='0987654321', password='adminpassword', first_name='Admin', last_name='User')

        # Create test menu items
        self.menu_item_1 = menu_item.objects.create(name='Espresso', price=100, desc='Strong coffee', category='hot', list_order=1)
        self.menu_item_2 = menu_item.objects.create(name='Iced Latte', price=150, desc='Cold coffee', category='cold', list_order=2)

        # Create test order
        self.order = order.objects.create(
            name='Test User',
            phone='1234567890',
            items_json=json.dumps({'item1': [1, 'Espresso', 100]}),
            table='1',
            order_time=datetime.now(),
            price=100
        )

    def test_menu_view(self):
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
        self.assertIn('items_by_category', response.context)

    def test_profile_view(self):
        self.client.login(phone='01203233117', password='8246')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_manage_menu_view(self):
        # Test anonymous user redirect
        response = self.client.get('/manage_menu/')
        self.assertEqual(response.status_code, 200)  # No POST, renders the page

        # Test POST request as admin
        self.client.login(phone='0987654321', password='adminpassword')
        with open('test_image.jpg', 'wb') as f:  # Mock file for upload
            response = self.client.post(
                '/manage_menu/',
                {'name': 'Mocha', 'price': 200, 'desc': 'Chocolate coffee', 'cat': 'hot', 'img': f},
                follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(menu_item.objects.filter(name='Mocha').exists())

    def test_delete_dish_view(self):
        # Test anonymous user redirect
        response = self.client.post(f'/delete_dish/{self.menu_item_1.id}/')
        self.assertEqual(response.status_code, 302)  # Redirect

        # Test admin user deletion
        self.client.login(phone='0987654321', password='adminpassword')
        response = self.client.post(f'/delete_dish/{self.menu_item_1.id}/')
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(menu_item.objects.filter(id=self.menu_item_1.id).exists())

    def test_cart_view(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_my_orders_view(self):
        self.client.login(phone='1234567890', password='password123')
        response = self.client.get('/my_orders/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_orders.html')
        self.assertIn('order_by_table', response.context)

    def test_login_view(self):
        response = self.client.post('/login/', {'phone': '1234567890', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Redirect to profile

    def test_logout_view(self):
        self.client.login(phone='1234567890', password='password123')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_signup_view(self):
        response = self.client.post('/signup/', {
            'fname': 'New', 'lname': 'User', 'number': '9876543210', 'password': 'newpassword', 'cpassword': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(phone='9876543210').exists())

    def test_generate_bill_view(self):
        self.client.login(phone='0987654321', password='adminpassword')
        response = self.client.get(f'/generate_bill/?table=1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'generate_bill.html')

    def test_view_bills_view(self):
        self.client.login(phone='0987654321', password='adminpassword')
        response = self.client.get('/view_bills/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bills.html')
