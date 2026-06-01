from django.test import TestCase
from django.urls import reverse
from .models import Category, Book, Subscriber, CartItem

class StoreModelsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Science")
        self.book = Book.objects.create(
            title="Cosmos",
            author="Carl Sagan",
            category=self.category,
            price=15.99,
            description="The story of cosmic evolution...",
            image_url="http://example.com/cosmos.jpg",
            is_featured=True
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Science")
        self.assertEqual(str(self.category), "Science")

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Cosmos")
        self.assertEqual(self.book.author, "Carl Sagan")
        self.assertEqual(float(self.book.price), 15.99)
        self.assertTrue(self.book.is_featured)
        self.assertEqual(self.book.cover_url, "http://example.com/cosmos.jpg")
        self.assertEqual(str(self.book), "Cosmos by Carl Sagan")

    def test_book_default_cover_fallback(self):
        # Create a book with no cover details to test default fallback url
        book_no_cover = Book.objects.create(
            title="Generic Book",
            author="Anonymous",
            category=self.category,
            price=9.99,
            description="Empty"
        )
        self.assertEqual(book_no_cover.cover_url, "/static/store/images/default_cover.jpg")


class StoreViewsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Technology")
        self.book = Book.objects.create(
            title="Clean Code",
            author="Robert C. Martin",
            category=self.category,
            price=37.50,
            description="Software craftsmanship book..."
        )

    def test_homepage_view(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/home.html')

    def test_browse_view_filtering(self):
        # Test standard list
        response = self.client.get(reverse('store:browse'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Clean Code")
        
        # Test category filtering
        response = self.client.get(reverse('store:browse') + f'?category={self.category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Clean Code")

        # Test search filtering
        response = self.client.get(reverse('store:browse') + '?search=Clean')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Clean Code")
        
        # Test non-matching search filtering
        response = self.client.get(reverse('store:browse') + '?search=Astronomy')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Clean Code")

    def test_book_detail_view(self):
        response = self.client.get(reverse('store:book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Clean Code")
        self.assertContains(response, "Robert C. Martin")

    def test_newsletter_ajax_subscription(self):
        # Successful signup
        response = self.client.post(
            reverse('store:subscribe'),
            {'email': 'test@example.com'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {
                'success': True,
                'message': "Thank you for subscribing! Keep an eye on your inbox for our latest updates and book recommendations."
            }
        )
        self.assertTrue(Subscriber.objects.filter(email='test@example.com').exists())

        # Duplicate signup should handle gracefully
        response_dup = self.client.post(
            reverse('store:subscribe'),
            {'email': 'test@example.com'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response_dup.status_code, 200)
        self.assertJSONEqual(
            response_dup.content.decode('utf-8'),
            {
                'success': True,
                'message': "You are already in our list of premium bookworms. Stay tuned for exciting newsletters!"
            }
        )

