from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models_nosql import Category, Product
from mongoengine import connect


class CategoryTests(APITestCase):
    def setUp(self):
        self.category_data = {
            'name': 'Handicrafts',
            'description': 'Various handcrafted items.'
        }
        self.category = Category.objects.create(**self.category_data)

    def test_create_category(self):
        url = reverse('category-list')
        data = {
            'name': 'Artisan Products',
            'description': 'Artisan handmade products'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])

    def test_get_category(self):
        url = reverse('category-detail', args=[str(self.category.id)])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    def test_filter_category_by_name(self):
        url = reverse('category-filter-by-name')
        response = self.client.get(url, {'name': 'Handicrafts'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Handicrafts')


class ProductTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Handicrafts', description='Handmade products')
        self.product_data = {
            'name': 'Wooden Vase',
            'description': 'A handcrafted wooden vase',
            'price': 25.99,
            'stock': 10,
            'category': self.category,
            'images': ['http://example.com/image1.jpg'],
            'tags': ['vase', 'wood'],
            'available': True
        }
        self.product = Product.objects.create(**self.product_data)

    def test_create_product(self):
        url = reverse('product-list')
        data = self.product_data.copy()
        data['name'] = 'Stone Pot'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Stone Pot')

    def test_get_product(self):
        url = reverse('product-detail', args=[str(self.product.id)])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_search_product(self):
        url = reverse('product-search')
        response = self.client.get(url, {'q': 'Wooden Vase'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Wooden Vase')

    def test_filter_by_category(self):
        url = reverse('product-filter-by-category')
        response = self.client.get(url, {'category': 'Handicrafts'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['category'], str(self.category.id))

    def test_filter_by_price(self):
        url = reverse('product-filter-by-price')
        response = self.client.get(url, {'min_price': 10, 'max_price': 30}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['price'], self.product.price)

    def test_filter_by_availability(self):
        url = reverse('product-filter-by-availability')
        response = self.client.get(url, {'available': 'true'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['available'], True)
