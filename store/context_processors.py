from .models import Cart


def cart_count(request):
    """Context processor để hiển thị số lượng sản phẩm trong giỏ hàng"""
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'cart_count': count}
