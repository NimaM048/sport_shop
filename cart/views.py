from decimal import Decimal

from django.contrib import messages
from django.http import HttpResponse, HttpRequest

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from sport_shop.settings import MERCHANT
from .zarinpal import ZarinPal
import ghasedakpack as ghasedakpack

from cart.card_models import Cart
from cart.models import DiscountCode, Order, OrderItem, UserDiscountCode
from home.models import SeriesModel
import requests
import json
from sport_shop import settings

SMS = ghasedakpack.Ghasedak("449b0c736047db369720dc24a2fbea59178da5123627d6eae4279dd142aeb10")


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        if not cart.cart:
            return redirect('cart:cart_empty')
        if not request.user.is_authenticated:
            return redirect('register:register')
        cart_item_count = len(cart.cart.values())
        return render(request, 'cart/cart.html', {'cart': cart, 'cart_item_count': cart_item_count})

    def calculate_cart_items(self, request):
        cart = Cart(request)
        if not cart.cart:
            return 0
        return len(cart.cart.values())


class CartAddView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('register:register')  # redirect to login page

        product = get_object_or_404(SeriesModel, id=pk)
        cart = Cart(request)

        # Check if the user has already purchased the course
        if OrderItem.objects.filter(order__user=request.user, order__is_paid=True, product=product).exists():
            return redirect('home:series_episod', pk=pk)

        cart.add(product=product, quantity=1)
        return redirect('cart:cart_detail')


class CartDeleteView(View):

    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)

        return redirect('cart:cart_detail')


class CartEmptyView(TemplateView):
    template_name = 'cart/cart-empty.html'


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'cart/order_detail.html', {'order': order})


class OrderCreationView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total_price)
        for item in cart:
            # Clean up the item price before converting to integer
            price_cleaned = ''.join(filter(str.isdigit, item['price']))
            OrderItem.objects.create(order=order, product=item['product'],
                                     price=int(price_cleaned))

        cart.remove()
        return redirect('cart:order_detail', order.id)


class ApplyDiscountView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        code = request.POST.get('discount_code')
        try:
            discount_code = DiscountCode.objects.get(name=code)
        except DiscountCode.DoesNotExist:
            messages.error(request, 'کد وارد شده نا معتبر است.')
            return redirect('cart:order_detail', order.id)

        if discount_code.quantity == 0:
            messages.error(request, 'این کد تخفیف استفاده شده است.')
            return redirect('cart:order_detail', order.id)

        if UserDiscountCode.objects.filter(user=request.user, discount_code=discount_code).exists():
            messages.error(request, 'شما یکبار از این کد استفاده کرده اید.')
            return redirect('cart:order_detail', order.id)

        discount_amount = discount_code.percentage * order.total_price / 100
        order.total_price -= discount_amount
        order.save()

        discount_code.quantity -= 1
        discount_code.save()

        UserDiscountCode.objects.create(user=request.user, discount_code=discount_code)

        return render(request, 'cart/order_detail.html', {
            'order': order,
            'discount_amount': int(discount_amount),
        })


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/cart/verify/'


@login_required
def request_payment(request, pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    request.session['order_id'] = str(order.id)
    request.session.save()  # Ensure the session is saved

    data = {
        "MerchantID": MERCHANT,
        "Amount": order.total_price,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }

    data["Amount"] = float(order.total_price)
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return redirect(ZP_API_STARTPAY + str(response['Authority']))
            else:
                return JsonResponse({'status': False, 'code': str(response['Status'])})
        return JsonResponse(response)

    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'code': 'connection error'})


class VerifyView(View):
    def get(self, request):
        print("Session data at the start of verify:", request.session.items())
        print(
            f'DEBUG: User authenticated: {request.user.is_authenticated}, Order ID in session: {request.session.get("order_id")}')

        order_id = request.session["order_id"]
        order = Order.objects.get(id=str(order_id))
        print(order.id)

        # Initialize the SMS sender
        sms_sender = ghasedakpack.Ghasedak("449b0c736047db369720dc24a2fbea59178da5123627d6eae4279dd142aeb109")
        thank_you_message = "Thank you for your purchase! Your order ID is: {}".format(order.id)

        def verify(authority):
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": order.total_price,
                "Authority": authority,
            }
            data = json.dumps(data)
            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data))}
            response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

            if response.status_code == 200:
                order.is_paid = True
                order.save()
                response = response.json()
                if response['Status'] == 100:
                    # Send SMS after successful payment
                    user_phone = request.user.phone  # Assuming user has phone attribute
                    sms_sender.verification({
                        'receptor': user_phone,
                        'type': '1',
                        'template': 'your_template_name',
                        'param1': thank_you_message
                    })
                    return render(request, 'cart/succsses_pay.html')
                else:
                    return render(request, 'cart/fail_result.html')
            else:
                return JsonResponse({'status': False, 'code': response.status_code})

        authority = request.GET.get('Authority')
        status = request.GET.get('Status')
        if status == 'OK':
            return verify(authority)
        else:
            return render(request, 'cart/fail_result.html')
# ? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
#
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
#
# amount = 1000  # Rial / Required
# description = "نهایی کردن خرید توسط شما"  # Required
# phone = 'YOUR_PHONE_NUMBER'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://localhost:8000/account/profile_courses'

# pay = ZarinPal(merchant='c1bd626d-83bf-45b6-8b35-629a16250cdf', call_back_url="http://localhost:8000/cart/verify/")
#
#
# @login_required
# def send_request(request, pk):
#     print("Before send_request: User authenticated:", request.user.is_authenticated)
#     order = get_object_or_404(Order, id=pk, user=request.user)
#     request.session['order_id'] = str(order.id)
#     print("Session data after setting order_id:", request.session.items())
#     request.session.save()
#     print("Setting order_id in session:", order.id)
#     print("Current session:", dict(request.session))
#     # email and mobile is optimal
#     response = pay.send_request(pk, request, description='توضیحات مربوط به پرداخت', email="Example@test.com",
#                                 mobile='09123456789')
#     if response.get('error_code') is None:
#         # redirect object
#         return response
#     else:
#         return HttpResponse(f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}')
#
# def verify(request):
#
# print("Session data at the start of verify:", request.session.items())
# print(
#     f'DEBUG: User authenticated: {request.user.is_authenticated}, Order ID in session: {request.session.get("order_id")}')
#
#     if not request.user.is_authenticated:
#         return HttpResponse("You must be logged in to access this page", status=401)
#
#     order_id = request.session.get('order_id')
#     if order_id:
#         try:
#             order = get_object_or_404(Order, id=int(order_id), user=request.user)
#         except Order.DoesNotExist:
#             return HttpResponse("Order not found", status=404)
#     else:
#         return HttpResponse("Order ID not found in session", status=404)
#     response = pay.verify(request=request)
#
#
#
#     if response.get("transaction"):
#         if response.get("pay"):
#             order.is_paid = True
#             order.save()
#             return render(request, 'cart/succsses_pay.html')
#         else:
#             return HttpResponse('این تراکنش با موفقیت انجام شده است و الان دوباره verify شده است')
#     else:
#         if response.get("status") == "ok":
#             return HttpResponse(f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}')
#         elif response.get("status") == "cancel":
#             return render(request, 'cart/fail_result.html')
