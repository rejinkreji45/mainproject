from cart.models import Cart

def count_items(request):
    total = 0
    if request.user.is_authenticated:
        u = request.user
        try:
            c = Cart.objects.filter(user=u)
            for i in c:
                total=total+i.quantity
        except:
            pass
    return {'count': total}
