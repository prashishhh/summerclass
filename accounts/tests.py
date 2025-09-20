from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from .forms import CustomPasswordResetForm

User = get_user_model()

class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Activate the user for password reset
        self.user.is_active = True
        self.user.save()
    
    def test_password_reset_view_get(self):
        """Test that password reset page loads correctly"""
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reset Password')
        self.assertIsInstance(response.context['form'], CustomPasswordResetForm)
    
    def test_password_reset_view_post_valid_email(self):
        """Test password reset with valid email"""
        response = self.client.post(reverse('password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to done page
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password Reset Request', mail.outbox[0].subject)
    
    def test_password_reset_view_post_invalid_email(self):
        """Test password reset with invalid email"""
        response = self.client.post(reverse('password_reset'), {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Still redirects for security
        self.assertEqual(len(mail.outbox), 0)  # No email sent
    
    def test_password_reset_done_view(self):
        """Test password reset done page"""
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email Sent!')
    
    def test_forgot_password_link_in_login(self):
        """Test that forgot password link exists in login page"""
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forgot password?')
        self.assertContains(response, reverse('password_reset'))
    
    def test_get_started_button_visibility(self):
        """Test that Get Started button shows for non-authenticated users"""
        # Test home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Get Started')
        
        # Test store page
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Get Started')
        
        # Login user
        self.client.force_login(self.user)
        
        # Test home page after login
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Get Started')
        
        # Test store page after login
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Get Started')
    
    def test_navbar_consistency(self):
        """Test that navbar has consistent styling across pages"""
        # Test home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'min-height:64px')
        
        # Test store page
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'min-height:64px')
        
        # Test login page
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'min-height:64px')
    
    def test_email_content_format(self):
        """Test that email content is properly formatted"""
        response = self.client.post(reverse('password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        
        email = mail.outbox[0]
        # Check basic email properties
        self.assertIn('Password Reset Request', email.subject)
        self.assertIn('test@example.com', email.to)
        
        # Check that email content is HTML
        self.assertEqual(email.content_subtype, 'html')
        self.assertIn('Reset Password', email.body)
        self.assertIn('<html>', email.body)
        
        # Check that email has alternatives (text content)
        if hasattr(email, 'alternatives') and email.alternatives:
            self.assertIn('text/plain', email.alternatives[0][1])
            self.assertIn('Password Reset', email.alternatives[0][0])  # Text content
