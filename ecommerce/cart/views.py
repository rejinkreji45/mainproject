import uuid
import razorpay
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from cart.forms import OrderForm
from cart.models import Cart, Order, Order_items
from shop.models import Product
from django.views.decorators.csrf import csrf_exempt


@method_decorator(login_required, name="dispatch")
class Addtocart(View):
    def get(self, request, i):
        product = Product.objects.get(id=i)
        user = request.user

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': 1}  # ensure quantity is set
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart:cartview')



@method_decorator(login_required, name="dispatch")
class CartView(View):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total = sum(item.subtotal() for item in cart_items)
        context = {'cart': cart_items, 'total': total}
        return render(request, 'cart.html', context)



@method_decorator(login_required, name="dispatch")
class CartDecrement(View):
    def get(self, request, i):
        try:
            c = Cart.objects.get(id=i)
            if c.quantity > 1:
                c.quantity -= 1
                c.save()
            else:
                c.delete()
        except Cart.DoesNotExist:
            pass
        return redirect('cart:cartview')


@method_decorator(login_required, name="dispatch")
class CartRemove(View):
    def get(self, request, i):
        try:
            c = Cart.objects.get(id=i)
            c.delete()
        except Cart.DoesNotExist:
            pass
        return redirect('cart:cartview')



@method_decorator(login_required, name="dispatch")
class Checkout(View):
    def post(self, request):
        form_instance = OrderForm(request.POST)
        if form_instance.is_valid():
            order = form_instance.save(commit=False)
            user = request.user
            order.user = user

            cart_items = Cart.objects.filter(user=user)
            total = sum(item.subtotal() for item in cart_items)
            if total < 1:
                return render(request, 'payment_error.html', {"msg": "Minimum order amount is ₹1"})

            order.amount = float(total)
            order.save()

            # ONLINE PAYMENT
            if order.payment_method == "ONLINE":
                client = razorpay.Client(auth=('rzp_test_Rn84sLoGtHBMCk', 'QGe6jOBFuf6UJrjDAQZGPRDU'))
                amount_paise = int(order.amount * 100)
                response_payment = client.order.create({'amount': amount_paise, 'currency': 'INR'})

                order.order_id = response_payment['id']
                order.save()

                context = {'payment': response_payment, 'user': user}
                return render(request, 'payment.html', context)

            # CASH ON DELIVERY
            else:
                order.order_id = 'cod_' + uuid.uuid4().hex[:12]
                order.is_ordered = True
                order.save()

                for item in cart_items:
                    order_item = Order_items.objects.create(order=order, product=item.product, quantity=item.quantity)
                    item.product.stock -= item.quantity
                    item.product.save()

                cart_items.delete()
                return render(request, 'payment_success.html')

        return redirect('cart:checkout')

    def get(self, request):
        form_instance = OrderForm()
        return render(request, 'checkout.html', {'form': form_instance})


# ------------------------------
@method_decorator(csrf_exempt, name='dispatch')
class Payment_success(View):
    def post(self, request):
        user = request.user
        response = request.POST

        if 'razorpay_order_id' not in response:
            return render(request, 'payment_error.html', {"msg": "Razorpay order id missing"})

        order_id = response['razorpay_order_id']
        order = Order.objects.get(order_id=order_id)
        order.is_ordered = True
        order.save()

        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            order_item = Order_items.objects.create(order=order, product=item.product, quantity=item.quantity)
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()
        return render(request, 'payment_success.html')


@method_decorator(login_required, name="dispatch")
class Orders(View):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user, is_ordered=True)
        return render(request, 'order.html', {'orders': orders})
