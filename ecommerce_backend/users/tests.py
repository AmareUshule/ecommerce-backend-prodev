from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class UserAuthIntegrationTests(APITestCase):
	def setUp(self):
		self.register_url = '/api/users/register/'
		self.login_url = '/api/users/login/'
		self.refresh_url = '/api/users/token/refresh/'
		self.logout_url = '/api/users/logout/'
		self.user_data = {
			'email': 'testuser@example.com',
			'username': 'testuser',
			'password': 'strongpassword123',
			'confirm_password': 'strongpassword123',
			'first_name': 'Test',
			'last_name': 'User'
		}

	def test_register_and_jwt_login_flow(self):
		# Register
		resp = self.client.post(self.register_url, self.user_data, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

		# Login (obtain tokens)
		login_resp = self.client.post(self.login_url, {
			'email': self.user_data['email'],
			'password': self.user_data['password']
		}, format='json')
		self.assertEqual(login_resp.status_code, status.HTTP_200_OK)
		self.assertIn('access', login_resp.data)
		self.assertIn('refresh', login_resp.data)
		self.assertIn('user', login_resp.data)

		refresh = login_resp.data['refresh']
		access = login_resp.data['access']

		# Refresh token
		refresh_resp = self.client.post(self.refresh_url, {'refresh': refresh}, format='json')
		self.assertEqual(refresh_resp.status_code, status.HTTP_200_OK)
		self.assertIn('access', refresh_resp.data)

		# Logout (blacklist refresh)
		# Authenticate with access token before logout (endpoint requires IsAuthenticated)
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		logout_resp = self.client.post(self.logout_url, {'refresh': refresh}, format='json')
		# Logout returns 205 Reset Content on success
		self.assertIn(logout_resp.status_code, (status.HTTP_205_RESET_CONTENT, status.HTTP_200_OK,))
