from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView, DetailView, View, ListView
from django_filters.views import FilterView
from .filters import ProductFilter
from .models import Product, Order
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm

class MainPageView(TemplateView):
    template_name = "store/main_page.html"

class FilteredProductsView(FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name = "store/products.html"
    context_object_name = "products"
    paginate_by = 8
    
    def get_queryset(self):
        qs = super().get_queryset()
        sort = self.request.GET.get('sort')
        if sort == 'asc':
            qs = qs.order_by('price')
        elif sort == 'desc':
            qs = qs.order_by('-price')
        else:
            qs = qs.order_by('id')
        return qs
    
class ProductDetailView(DetailView):
    sizes = ["S","M","L","XL","XXL"]
    template_name = "store/product_detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        liked = False
        if user.is_authenticated:
            liked = self.object.liked_by.filter(id=user.profile.id).exists()

        context['sizes'] = ProductDetailView.sizes
        context['liked'] = liked
        return context

class CartView(View):
    def get(self, request):
        cart = request.session.get("cart", {})
        items = []
        total_price = 0

        for product_id, sizes in cart.items():
            product = get_object_or_404(Product, id=product_id)

            for size, quantity in sizes.items():
                subtotal_price = product.price * quantity
                total_price += subtotal_price
                items.append({
                    "product": product,
                    "size": size,
                    "quantity": quantity,
                    "subtotal_price": subtotal_price,
                })

        return render(request, "store/cart.html", {
            "cart_items": items,
            "total_price": total_price,
        })


class AddToCartView(View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        size = request.POST.get("size")

        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get("cart", {})

        if product_id not in cart:
            cart[product_id] = {}

        cart[product_id][size] = cart[product_id].get(size, 0) + 1

        request.session["cart"] = cart
        messages.success(request, "✅ Produkt został dodany do koszyka!")
        return redirect("product-detail", pk=product.id)


class RemoveFromCartView(View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        size = request.POST.get("size")

        cart = request.session.get("cart", {})

        if product_id in cart and size in cart[product_id]:
            
            if cart[product_id][size] > 1:
                print('-1')
                cart[product_id][size] -= 1
            else:
                print('del')
                del cart[product_id][size]

                if not cart[product_id]:
                    del cart[product_id]

            request.session["cart"] = cart

        return redirect("cart")

class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        profile = request.user.profile
        profile_form = ProfileForm(instance=profile)
        return render(request,'store/profile.html',{
            'profile_form':profile_form
        })
    
    def post(self,request):
        profile = request.user.profile
        profile_form = ProfileForm(request.POST, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        
        return render(request,'store/profile.html',{
            'profile_form':profile_form
        })


class LikedProductsView(LoginRequiredMixin,ListView):
    template_name = "store/liked_products.html"
    model = Product
    context_object_name = "products"

    def get_queryset(self):
        profile = self.request.user.profile
        return profile.liked_products.all()
    
class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        profile = request.user.profile
        product = get_object_or_404(Product, pk=product_id)

        if profile.liked_products.filter(pk=product.pk).exists():
            profile.liked_products.remove(product)
            liked = False
        else:
            profile.liked_products.add(product)
            liked = True

        return JsonResponse({'liked': liked})

class OrdersView(ListView):
    template_name = 'store/orders.html'
    model = Order
    context_object_name = 'orders'
    ordering = ['-created_at']