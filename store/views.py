from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Product, Category, Cart, Order, OrderItem, Review, Wishlist
from .forms import CheckoutForm, ReviewForm


def home(request):
    """Trang chủ hiển thị sản phẩm nổi bật"""
    featured_products = Product.objects.filter(is_available=True)[:8]
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    """Danh sách tất cả sản phẩm"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    # Lọc theo danh mục
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Tìm kiếm
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """Chi tiết sản phẩm"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'average_rating': average_rating,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'store/product_detail.html', context)


@login_required
def cart_view(request):
    """Xem giỏ hàng"""
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.get_total() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Thêm sản phẩm vào giỏ hàng"""
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'Đã thêm {product.name} vào giỏ hàng!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def update_cart(request, cart_id):
    """Cập nhật số lượng trong giỏ hàng"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Đã cập nhật giỏ hàng!')
        else:
            cart_item.delete()
            messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
    
    return redirect('cart')


@login_required
def remove_from_cart(request, cart_id):
    """Xóa sản phẩm khỏi giỏ hàng"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Đã xóa {product_name} khỏi giỏ hàng!')
    return redirect('cart')


@login_required
def checkout(request):
    """Thanh toán"""
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('cart')
    
    total = sum(item.get_total() for item in cart_items)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Tạo đơn hàng
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                note=form.cleaned_data['note'],
                total_amount=total
            )
            
            # Tạo chi tiết đơn hàng
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Xóa giỏ hàng
            cart_items.delete()
            
            messages.success(request, f'Đặt hàng thành công! Mã đơn hàng: #{order.id}')
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm(initial={
            'full_name': request.user.get_full_name(),
        })
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_success(request, order_id):
    """Đặt hàng thành công"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'store/order_success.html', context)


@login_required
def order_list(request):
    """Danh sách đơn hàng của người dùng"""
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'store/order_list.html', context)


@login_required
def order_detail(request, order_id):
    """Chi tiết đơn hàng"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'store/order_detail.html', context)


def register_view(request):
    """Đăng ký tài khoản"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Đăng ký thành công!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'store/register.html', context)


def login_view(request):
    """Đăng nhập"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Chào mừng {username}!')
                return redirect(request.GET.get('next', 'home'))
    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'store/login.html', context)


def logout_view(request):
    """Đăng xuất"""
    logout(request)
    messages.success(request, 'Đã đăng xuất!')
    return redirect('home')


@login_required
def add_review(request, product_id):
    """Thêm đánh giá sản phẩm"""
    product = get_object_or_404(Product, id=product_id)
    
    # Kiểm tra user đã review chưa
    existing_review = Review.objects.filter(user=request.user, product=product).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if existing_review:
                # Cập nhật review cũ
                existing_review.rating = form.cleaned_data['rating']
                existing_review.comment = form.cleaned_data['comment']
                existing_review.save()
                messages.success(request, 'Đã cập nhật đánh giá của bạn!')
            else:
                # Tạo review mới
                Review.objects.create(
                    user=request.user,
                    product=product,
                    rating=form.cleaned_data['rating'],
                    comment=form.cleaned_data['comment']
                )
                messages.success(request, 'Cảm ơn bạn đã đánh giá sản phẩm!')
            
            return redirect('product_detail', slug=product.slug)
    
    return redirect('product_detail', slug=product.slug)


@login_required
def delete_review(request, review_id):
    """Xóa đánh giá"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, 'Đã xóa đánh giá của bạn!')
    return redirect('product_detail', slug=product_slug)


@login_required
def wishlist_view(request):
    """Xem danh sách yêu thích"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'store/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    """Thêm sản phẩm vào danh sách yêu thích"""
    product = get_object_or_404(Product, id=product_id)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'Đã thêm {product.name} vào danh sách yêu thích!')
    else:
        messages.info(request, f'{product.name} đã có trong danh sách yêu thích!')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def remove_from_wishlist(request, wishlist_id):
    """Xóa sản phẩm khỏi danh sách yêu thích"""
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    product_name = wishlist_item.product.name
    wishlist_item.delete()
    messages.success(request, f'Đã xóa {product_name} khỏi danh sách yêu thích!')
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))
