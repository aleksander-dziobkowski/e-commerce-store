from .models import MainCategory, Category, Product
from django.db.models import Prefetch
from django.db.models import Count

def main_categories_context(request):
    RECOMMENED_PRODUCTS = 5

    main_categories = MainCategory.objects.prefetch_related(
        Prefetch('categories', queryset=Category.objects.all())
    )

    recommended_products = Product.objects.all()[:RECOMMENED_PRODUCTS]

    cart = request.session.get('cart', {})
    items = []
    for product_id, sizes in cart.items():
        
        try:
            product = Product.objects.get(id=product_id)
            for size, quantity in sizes.items():
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'size':size
                })
        except Product.DoesNotExist:
            continue

    return {'main_categories': main_categories,
            'recommended_products':recommended_products,
            'cart_items_preview': items,
            'cart_items_count':len(items)
            }
