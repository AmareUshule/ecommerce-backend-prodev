from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from categories.models import Category
from products.models import Product


class ProductIntegrationTests(APITestCase):
	def setUp(self):
		# Create admin user
		self.admin = User.objects.create_superuser(email='admin@example.com', username='admin', password='adminpass')
		# Create regular user
		self.user = User.objects.create_user(email='user@example.com', username='user', password='userpass')

		# Create a category for products
		self.category = Category.objects.create(name='Test Cat', slug='test-cat')

		self.create_url = '/api/products/create/'
		self.list_url = '/api/products/'

	def obtain_token_for_user(self, email, password):
		resp = self.client.post('/api/users/login/', {'email': email, 'password': password}, format='json')
		return resp.data.get('access'), resp.data.get('refresh')

	def test_admin_can_create_product_and_public_can_list_with_pagination(self):
		access, _ = self.obtain_token_for_user('admin@example.com', 'adminpass')
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

		product_payload = {
			'name': 'Product 1',
			'slug': 'product-1',
			'sku': 'SKU1',
			'description': 'A product',
			'price': '10.00',
			'category_id': self.category.id,
			'stock_quantity': 5,
			'is_active': True
		}

		create_resp = self.client.post(self.create_url, product_payload, format='json')
		self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)

		# create additional products for pagination
		for i in range(2, 26):
			Product.objects.create(
				name=f'Product {i}', slug=f'product-{i}', sku=f'SKU{i}',
				description='desc', price='5.00', category=self.category, stock_quantity=1
			)

		# Public list with pagination: page 2, page_size 10 -> should return 10 items
		self.client.credentials()  # clear auth for public access
		list_resp = self.client.get(self.list_url + '?page=2&page_size=10')
		self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
		self.assertIn('results', list_resp.data)
		self.assertEqual(len(list_resp.data['results']), 10)

	def test_non_admin_cannot_create_product(self):
		access, _ = self.obtain_token_for_user('user@example.com', 'userpass')
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

		payload = {
			'name': 'Forbidden Product',
			'slug': 'forbidden-product',
			'sku': 'FORBID1',
			'description': 'no',
			'price': '1.00',
			'category_id': self.category.id,
			'stock_quantity': 1
		}
		resp = self.client.post(self.create_url, payload, format='json')
		self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED))
