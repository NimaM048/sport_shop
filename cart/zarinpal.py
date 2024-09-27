import requests
import json
from django.shortcuts import redirect, get_object_or_404

from cart.models import Order
from sport_shop import settings

CallbackURL = 'http://localhost:8000/cart/verify/?order_id={order_id}'



class ZarinPal:
    ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
    ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"

    def __init__(self, merchant, call_back_url):
        self.MERCHANT = merchant
        self.callbackURL = call_back_url

    def send_request(self,pk, request, description, email=None, mobile=None):
        order = get_object_or_404(Order, id=pk, user=request.user)
        request.session['order_id'] = str(order.id)

        req_data = {
            "merchant_id": self.MERCHANT,
            "amount":order.total_price,
            "callback_url": self.callbackURL,
            "description": description,
            "metadata": {"mobile": mobile, "email": email}
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req = requests.post(url=self.ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)

        if len(req.json()['errors']) == 0:
            authority = req.json()['data']['authority']
            return redirect(self.ZP_API_STARTPAY.format(authority=authority))

        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return {"message": e_message, "error_code": e_code}
#
    def verify(self, request, **kwargs):

        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        order_id = request.session["order_id"]
        order = Order.objects.get(id=int(order_id))

        if t_status == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": self.MERCHANT,
                "amount": order.total_price,
                "authority": t_authority
            }
            req = requests.post(url=self.ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:

                    return {"transaction": True, "pay": True, "RefID": req.json()['data']['ref_id'], "message": None}

                elif t_status == 101:

                    return {"transaction": True, "pay": False, "RefID": None, "message": req.json()['data']['message']}

                else:
                    return {"transaction": False, "pay": False, "RefID": None, "message": req.json()['data']['message']}

            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']

                return {"status": 'ok', "message": e_message, "error_code": e_code}
        else:
            return {"status": 'cancel', "message": 'transaction failed or canceled by user'}

