import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    main_category_id = django_filters.NumberFilter(field_name="category__main_category_id")
    category_id = django_filters.NumberFilter(field_name="category_id")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ["main_category_id", "category_id", "min_price", "max_price"]