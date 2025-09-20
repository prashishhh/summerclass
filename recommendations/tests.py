from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from store.models import Product, Category
from .models import UserActivity
from django.utils import timezone
from decimal import Decimal

User = get_user_model()


class RecommendationSystemTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test category
        self.category = Category.objects.create(
            category_name='Test Category',
            slug='test-category'
        )
        
        # Create test products
        self.product1 = Product.objects.create(
            product_name='Test Product 1',
            slug='test-product-1',
            price=100,
            stock=10,
            category=self.category,
            owner=self.user
        )
        
        self.product2 = Product.objects.create(
            product_name='Test Product 2',
            slug='test-product-2',
            price=200,
            stock=5,
            category=self.category,
            owner=self.user
        )
        
        self.product3 = Product.objects.create(
            product_name='Test Product 3',
            slug='test-product-3',
            price=150,
            stock=8,
            category=self.category,
            owner=self.user
        )
        
        # Create test client
        self.client = Client()
    
    def test_recently_viewed(self):
        """Test recently viewed products endpoint"""
        # Create some view activities
        UserActivity.objects.create(
            user=self.user,
            product=self.product1,
            action='view',
            timestamp=timezone.now()
        )
        
        UserActivity.objects.create(
            user=self.user,
            product=self.product2,
            action='view',
            timestamp=timezone.now()
        )
        
        url = reverse('recommendations:recently_viewed', args=[self.user.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['products']), 2)
    
    def test_also_bought(self):
        """Test also bought products endpoint"""
        # Create some purchase activities
        UserActivity.objects.create(
            user=self.user,
            product=self.product1,
            action='buy',
            timestamp=timezone.now()
        )
        
        UserActivity.objects.create(
            user=self.user,
            product=self.product2,
            action='buy',
            timestamp=timezone.now()
        )
        
        url = reverse('recommendations:also_bought', args=[self.product1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['products']), 1)  # Should exclude current product
    
    def test_trending(self):
        """Test trending products endpoint"""
        # Create some recent purchase activities
        UserActivity.objects.create(
            user=self.user,
            product=self.product1,
            action='buy',
            timestamp=timezone.now()
        )
        
        UserActivity.objects.create(
            user=self.user,
            product=self.product2,
            action='buy',
            timestamp=timezone.now()
        )
        
        url = reverse('recommendations:trending')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['products']), 2)
    
    def test_user_activity_model(self):
        """Test UserActivity model creation and string representation"""
        activity = UserActivity.objects.create(
            user=self.user,
            product=self.product1,
            action='view'
        )
        
        self.assertEqual(str(activity), f"{self.user.username} viewed {self.product1.product_name} at {activity.timestamp}")
        self.assertEqual(activity.action, 'view')
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.product, self.product1)
