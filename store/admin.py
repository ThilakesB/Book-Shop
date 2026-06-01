from django.contrib import admin
from .models import Category, Book, Subscriber, CartItem

# Customizing the Django Admin Site Headers
admin.site.site_header = "Cyber Bookshop Administration"
admin.site.site_title = "Cyber Bookshop Admin Portal"
admin.site.index_title = "Welcome to the Cyber Bookshop Management Panel"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'is_featured', 'is_bestseller', 'is_new_arrival', 'created_at')
    list_filter = ('category', 'is_featured', 'is_bestseller', 'is_new_arrival', 'created_at')
    search_fields = ('title', 'author', 'description')
    list_editable = ('price', 'is_featured', 'is_bestseller', 'is_new_arrival')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('General Info', {
            'fields': ('title', 'author', 'category', 'price', 'description')
        }),
        ('Media & Links', {
            'fields': ('image', 'image_url')
        }),
        ('Featured Sections', {
            'fields': ('is_featured', 'is_bestseller', 'is_new_arrival')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
    ordering = ('-subscribed_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_session', 'book', 'quantity', 'created_at')
    list_filter = ('created_at', 'book__category')
    search_fields = ('user_session', 'book__title', 'book__author')
    readonly_fields = ('created_at',)

