from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv
import requests
import json
from .models import Product,Order,OrderItem

load_dotenv()

def get_payu_access_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("PAYU_CLIENT_ID"),
        "client_secret": os.getenv("PAYU_CLIENT_SECRET")
    }

    response = requests.post(
        f"{os.getenv('PAYU_SANDBOX_URL')}/pl/standard/user/oauth/authorize",
        data=payload
    )

    return response.json().get("access_token")

@csrf_exempt
def payu_create_order(request):
    cart = request.session['cart']

    products = []
    price = 0
    for product_id,sizes in cart.items():
        for size,quantity in sizes.items():
            product = get_object_or_404(Product,id=product_id)
            product_price = product.price

            price = price + quantity*product_price
            
            product_item = {
                "id":product_id,
                "size":size,
                "name":product.name,
                "quantity":quantity,
                "unitPrice":str(int(quantity*product_price*100))
            }

            products.append(product_item)

    access_token = get_payu_access_token()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "notifyUrl": "http://localhost:8000/store/payu-notify/",
        "continueUrl": "http://localhost:8000/store/",
        "customerIp": "1.12.123.255",
        "merchantPosId": "300746",
        "description": "Test order",
        "currencyCode": "EUR",
        "totalAmount": str(int(price*100)),  
        "products": products,
        "language": "en"
    }

    response = requests.post(
        f"{os.getenv('PAYU_SANDBOX_URL')}/api/v2_1/orders",
        headers=headers,
        json=payload,
        allow_redirects=False
    )

    result = response.json()
    redirect_url = result.get("redirectUri")
    print(result)
    if 'orderId' in result and request.user.is_authenticated:
        print('suc')
        order = Order.objects.create(
            profile=request.user.profile,
            payu_order_id=result['orderId'],
            status="NEW",
            amount=price
        )
        order_items = [
            OrderItem(
                order=order,
                product=get_object_or_404(Product,id=p['id']),
                size=p['size'],
                quantity=p['quantity'],
                price = int(p['unitPrice']) / 100
            ) for p in products
        ]
        OrderItem.objects.bulk_create(order_items)

    return JsonResponse({"redirectUri": redirect_url})

@csrf_exempt
def payu_notify(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "invalid_json"}, status=400)

    order_data = data.get("order", {})
    payu_order_id = order_data.get("orderId")
    status = order_data.get("status")

    if not payu_order_id:
        return JsonResponse({"error": "missing_order_id"}, status=400)

    try:
        order = Order.objects.get(payu_order_id=payu_order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "order_not_found"}, status=404)

    if status == "COMPLETED":
        order.status = "COMPLETED"
        order.save()

        # Wyczyść koszyk
        if request.session.get("cart"):
            request.session["cart"] = {}
            request.session.modified = True

    return JsonResponse({"status": "ok"})

