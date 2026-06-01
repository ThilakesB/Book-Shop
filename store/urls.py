from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('books/', views.browse_view, name='browse'),
    path('books/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('books/<int:book_id>/ai-summary/', views.ai_summary_view, name='ai_summary'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/', views.update_cart_view, name='update_cart'),
    path('cart/remove/', views.remove_from_cart_view, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/success/', views.checkout_success_view, name='checkout_success'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
]

