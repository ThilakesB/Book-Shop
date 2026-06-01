from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price in decimal
    description = models.TextField()
    image = models.ImageField(upload_to='books/covers/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Direct link to a cover image (useful fallback or CDN link)")
    
    # Showcase sections
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def cover_url(self):
        """Returns the cover image URL, prioritizing uploaded files over remote URLs."""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return "/static/store/images/default_cover.jpg"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class CartItem(models.Model):
    user_session = models.CharField(max_length=255, db_index=True, help_text="Django session key to track guest carts")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart Item: {self.quantity} x {self.book.title} (Session: {self.user_session[:8]}...)"

    @property
    def total_price(self):
        return self.book.price * self.quantity

