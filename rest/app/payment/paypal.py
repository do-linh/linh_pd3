import requests

from django.conf import settings
import base64
from .models import PaypalToken,PaypalOrder, Payment
from ..checkout.models import Checkout
from ..checkout.utils import complete_checkout
from ..order.models import Order
  
class Paypal:
    def __init__(self, client_id, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

def authorize() -> dict:
    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    payload='grant_type=client_credentials&ignoreCache=true&return_authn_schemes=true&return_client_metadata=true&return_unconsented_scopes=true'
    s = settings.PAYPAL_CLIENT_ID + ":" +settings.PAYPAL_CLIENT_SECRET
    s_bytes = s.encode("ascii")
    
    base64_bytes = base64.b64encode(s_bytes)
    base64_string = base64_bytes.decode("ascii")

    headers = {
    'Authorization': f'Basic {base64_string}',
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    """dict_keys(['scope', 'access_token', 'token_type', 'app_id',
     'expires_in', 'supported_authn_schemes', 'nonce', 'client_metadata']"""
    if response.status_code == 200:
        return response.json()

def get_access_token():
    if PaypalToken.objects.first().still_valid():
        return PaypalToken.objects.first().access_token
    else:
        r = authorize()
        if r:
            PaypalToken.objects.create(
            access_token=r.get("access_token")
            , token_type=r.get('token_type')
            , expires_in=r.get('expires_in')

            )
            return r['access_token']
        else:
            raise KeyError("Could not obtainn token")

def create_an_paypal_order(checkout: "Checkout"):
    url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : f'Bearer {get_access_token()}'
    }
    payload = {
        "intent": "CAPTURE",
        "purchase_units" : [ 
            {
                "items": [
                    {
                        "name": line.book.get_display(),
                        "description": line.book.get_description(),
                        "quantity" : str(line.quantity),
                        "unit_amount": {
                            "currency_code": "USD",
                            "value": line.book.get_price_for_paypal()  #default rate
                        }
                    }
                    for line in checkout
                ],
                "amount" : {
                    "currency_code" : "USD",
                    "value" : checkout.get_paypal_total_amout(),
                    "breakdown": {
                        "item_total": {
                        "currency_code": "USD",
                        "value": checkout.get_paypal_total_amout()
                        }
                }
                }
            } 
        ],
        "application_context": {
            "brand_name": "D-Linh Store",
            "return_url": "http://localhost:8000/paypal/checkout",
            "cancel_url": "https://example.com/cancel"
        }
    }
    response = requests.post(url,headers=headers, json=payload)
    if response.status_code == 201:
        data = response.json()
        data['checkout'] = checkout
        data['paypal_order_id'] = data.pop('id')
        # links: list[dict]= data.get('links')
        return data
    else:

        raise Exception(f'Can not create paypal order. {response.text}')
        
        # for link in links:
        #     if link.get('rel') == 'approve':
        #         out.update({'approve_link': link}) 

def capture_a_paypal_order(paypal_order: "PaypalOrder"):
    url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order.pk}/capture"
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : f'Bearer {get_access_token()}'
    }
    data = {'id': '4PX51351985684432', 'status': 'COMPLETED', 'payment_source': {'paypal': {'email_address': 'sb-ccbfs8302732@personal.example.com', 
    'account_id': 'UWEN2PPMUYS2S', 'name': {'given_name': 'John', 'surname': 'Doe'}, 'address': {'country_code': 'US'}}}, 'purchase_units': [{'reference_id': 'default', 'shipping': {'name': {'full_name': 'John Doe'}, 'address': {'address_line_1': '1 Main St', 'admin_area_2': 'San Jose',
     'admin_area_1': 'CA', 'postal_code': '95131', 'country_code': 'US'}}, 'payments': {'captures': [{'id': '3LJ93329BL502243D', 'status': 'COMPLETED', 
     'amount': {'currency_code': 'USD', 'value': '4.80'}, 'final_capture': True, 'seller_protection': {'status': 'ELIGIBLE', 
     'dispute_categories': ['ITEM_NOT_RECEIVED', 'UNAUTHORIZED_TRANSACTION']}, 'seller_receivable_breakdown': {'gross_amount': {'currency_code': 'USD', 'value': '4.80'}, 
     'paypal_fee': {'currency_code': 'USD', 'value': '0.66'}, 'net_amount': {'currency_code': 'USD', 'value': '4.14'}}, 
     'links': [{'href': 'https://api.sandbox.paypal.com/v2/payments/captures/3LJ93329BL502243D', 'rel': 'self', 'method': 'GET'}, 
     {'href': 'https://api.sandbox.paypal.com/v2/payments/captures/3LJ93329BL502243D/refund', 'rel': 'refund', 'method': 'POST'}, 
     {'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/4PX51351985684432', 'rel': 'up', 'method': 'GET'}], 'create_time': '2022-09-02T14:22:49Z', 
     'update_time': '2022-09-02T14:22:49Z'}]}}], 'payer': {'name': {'given_name': 'John', 'surname': 'Doe'}, 'email_address': 'sb-ccbfs8302732@personal.example.com', 'payer_id': 'UWEN2PPMUYS2S', 'address': {'country_code': 'US'}}, 'links': [{'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/4PX51351985684432', 'rel': 'self', 'method': 'GET'}]}
    # res = requests.post(url, headers=headers)
    # if res.status_code == 201:
    #     data= res.json()
    if True:
        checkout = paypal_order.checkout
        payment = Payment.objects.create(
            checkout= checkout,
            paypal_order = paypal_order,
            status = data['status'],
            first_name = data['payer']['name']['given_name'],
            last_name = data['payer']['name']['surname'],
            email = data['payer']['email_address'],
            address_line_1 = data['purchase_units'][0]['shipping']['address']['address_line_1'],
            admin_area_2 = data['purchase_units'][0]['shipping']['address']['admin_area_2'],
            admin_area_1 = data['purchase_units'][0]['shipping']['address']['admin_area_1'],
            postal_code = data['purchase_units'][0]['shipping']['address']['postal_code'],
            country_code = data['purchase_units'][0]['shipping']['address']['country_code']
        )
        order = complete_checkout(checkout, payment)
        return order
    else:
        raise Exception(f'Can not capture the paypal order. {res.text}')



    