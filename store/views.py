from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Category, Book, Subscriber, CartItem
from .gemini_service import generate_book_summary

# Utility to manage anonymous guest session IDs
def get_or_create_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

# Helper to get cart stats
def get_cart_stats(session_key):
    cart_items = CartItem.objects.filter(user_session=session_key)
    total_count = sum(item.quantity for item in cart_items)
    subtotal = sum(item.total_price for item in cart_items)
    return total_count, subtotal

def home_view(request):
    """Renders the storefront page with curated book sections."""
    session_key = get_or_create_session_id(request)
    cart_count, _ = get_cart_stats(session_key)
    
    featured_books = Book.objects.filter(is_featured=True)[:4]
    bestsellers = Book.objects.filter(is_bestseller=True)[:4]
    new_arrivals = Book.objects.filter(is_new_arrival=True)[:4]
    
    context = {
        'featured_books': featured_books,
        'bestsellers': bestsellers,
        'new_arrivals': new_arrivals,
        'cart_count': cart_count,
    }
    return render(request, 'store/home.html', context)

def browse_view(request):
    """Enables search, category filtering, price filtering, and sorting."""
    session_key = get_or_create_session_id(request)
    cart_count, _ = get_cart_stats(session_key)
    
    categories = Category.objects.all()
    books = Book.objects.all()
    
    # Extract query params
    search_query = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    sort_by = request.GET.get('sort', 'featured')

    # Apply search filter
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    # Apply category filter
    if category_id:
        books = books.filter(category_id=category_id)
        
    # Apply price range filter
    if price_min:
        try:
            books = books.filter(price__gte=float(price_min))
        except ValueError:
            pass
    if price_max:
        try:
            books = books.filter(price__lte=float(price_max))
        except ValueError:
            pass

    # Apply sorting
    if sort_by == 'price_asc':
        books = books.order_by('price')
    elif sort_by == 'price_desc':
        books = books.order_by('-price')
    elif sort_by == 'newest':
        books = books.order_by('-created_at')
    else:  # 'featured' default
        books = books.order_by('-is_featured', 'title')

    context = {
        'categories': categories,
        'books': books,
        'cart_count': cart_count,
        # Maintain filter values in UI
        'search_query': search_query,
        'selected_category': int(category_id) if category_id and category_id.isdigit() else None,
        'price_min': price_min,
        'price_max': price_max,
        'sort_by': sort_by,
    }
    return render(request, 'store/browse.html', context)

def book_detail_view(request, book_id):
    """Renders details of a specific book."""
    session_key = get_or_create_session_id(request)
    cart_count, _ = get_cart_stats(session_key)
    
    book = get_object_or_404(Book, id=book_id)
    related_books = Book.objects.filter(category=book.category).exclude(id=book.id)[:4]
    
    context = {
        'book': book,
        'related_books': related_books,
        'cart_count': cart_count,
    }
    return render(request, 'store/detail.html', context)

def ai_summary_view(request, book_id):
    """AJAX endpoint that dynamically retrieves AI-generated summary for a book."""
    book = get_object_or_404(Book, id=book_id)
    summary_html = generate_book_summary(book.title, book.author, book.description)
    return JsonResponse({'summary': summary_html})

def cart_view(request):
    """Renders the shopping cart page."""
    session_key = get_or_create_session_id(request)
    cart_items = CartItem.objects.filter(user_session=session_key).select_related('book')
    cart_count, subtotal = get_cart_stats(session_key)
    
    # Calculate dummy delivery fee and total
    delivery_fee = 3.99 if cart_count > 0 else 0.00
    grand_total = float(subtotal) + delivery_fee
    
    context = {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

@require_POST
def add_to_cart_view(request):
    """AJAX post to add a book to session-based cart."""
    session_key = get_or_create_session_id(request)
    book_id = request.POST.get('book_id')
    quantity = int(request.POST.get('quantity', 1))
    
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(
        user_session=session_key,
        book=book,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
        
    cart_count, _ = get_cart_stats(session_key)
    return JsonResponse({
        'success': True,
        'message': f"'{book.title}' has been successfully added to your cart!",
        'cart_count': cart_count
    })

@require_POST
def update_cart_view(request):
    """AJAX post to update the quantity of a cart item."""
    session_key = get_or_create_session_id(request)
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item = get_object_or_404(CartItem, id=item_id, user_session=session_key)
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        subtotal_updated = cart_item.total_price
    else:
        cart_item.delete()
        subtotal_updated = 0.00
        
    cart_count, subtotal = get_cart_stats(session_key)
    delivery_fee = 3.99 if cart_count > 0 else 0.00
    grand_total = float(subtotal) + delivery_fee
    
    return JsonResponse({
        'success': True,
        'cart_count': cart_count,
        'item_subtotal': f"${subtotal_updated:.2f}",
        'subtotal': f"${subtotal:.2f}",
        'delivery_fee': f"${delivery_fee:.2f}",
        'grand_total': f"${grand_total:.2f}",
        'removed': quantity <= 0
    })

@require_POST
def remove_from_cart_view(request):
    """AJAX post to remove an item from the cart."""
    session_key = get_or_create_session_id(request)
    item_id = request.POST.get('item_id')
    
    cart_item = get_object_or_404(CartItem, id=item_id, user_session=session_key)
    cart_item.delete()
    
    cart_count, subtotal = get_cart_stats(session_key)
    delivery_fee = 3.99 if cart_count > 0 else 0.00
    grand_total = float(subtotal) + delivery_fee
    
    return JsonResponse({
        'success': True,
        'cart_count': cart_count,
        'subtotal': f"${subtotal:.2f}",
        'delivery_fee': f"${delivery_fee:.2f}",
        'grand_total': f"${grand_total:.2f}"
    })

def checkout_view(request):
    """Renders dummy checkout page and clears cart on successful POST submission."""
    session_key = get_or_create_session_id(request)
    cart_items = CartItem.objects.filter(user_session=session_key)
    cart_count, subtotal = get_cart_stats(session_key)
    
    if cart_count == 0:
        return redirect('store:cart')
        
    delivery_fee = 3.99
    grand_total = float(subtotal) + delivery_fee
    
    if request.method == 'POST':
        # Collect shipping/billing inputs
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        
        # In a real app we would create an Order, handle stripe, etc.
        # For our dummy checkout: clear the user's cart
        cart_items.delete()
        
        # Save order details in session to present receipt on the success page
        request.session['receipt_name'] = name
        request.session['receipt_email'] = email
        request.session['receipt_address'] = f"{address}, {city}, {zip_code}"
        request.session['receipt_total'] = f"${grand_total:.2f}"
        
        return redirect('store:checkout_success')
        
    context = {
        'cart_count': cart_count,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)

def checkout_success_view(request):
    """Renders checkout success receipt then clears receipt session details."""
    receipt_name = request.session.pop('receipt_name', 'Valued Customer')
    receipt_email = request.session.pop('receipt_email', '')
    receipt_address = request.session.pop('receipt_address', '')
    receipt_total = request.session.pop('receipt_total', '$0.00')
    
    context = {
        'receipt_name': receipt_name,
        'receipt_email': receipt_email,
        'receipt_address': receipt_address,
        'receipt_total': receipt_total,
        'cart_count': 0,
    }
    return render(request, 'store/checkout_success.html', context)

@require_POST
def subscribe_view(request):
    """AJAX post view for newsletter registration."""
    email = request.POST.get('email', '').strip().lower()
    if not email:
        return JsonResponse({'success': False, 'message': 'Email address cannot be empty.'})
        
    subscriber, created = Subscriber.objects.get_or_create(email=email)
    if created:
        message = "Thank you for subscribing! Keep an eye on your inbox for our latest updates and book recommendations."
    else:
        message = "You are already in our list of premium bookworms. Stay tuned for exciting newsletters!"
        
    return JsonResponse({'success': True, 'message': message})

