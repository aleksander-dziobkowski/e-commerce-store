from django.urls import path
from . import views, payu_views

urlpatterns = [
    path('',views.MainPageView.as_view(),name='store'),
    path('products/',views.FilteredProductsView.as_view(),name='products'),
    path('products/<int:pk>',views.ProductDetailView.as_view(),name='product-detail'),
    path('cart/',views.CartView.as_view(),name='cart'),
    path('cart/add/',views.AddToCartView.as_view(),name='add-to-cart'),
    path('cart/remove/',views.RemoveFromCartView.as_view(),name='remove-from-cart'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('products/liked/',views.LikedProductsView.as_view(),name='liked-products'),
    path('products/<int:product_id>/like/', views.ToggleLikeView.as_view(), name='toggle_like'),
    path('payu-create-order/', payu_views.payu_create_order, name='payu-create-order'),
    path('payu-notify/', payu_views.payu_notify, name='payu_notify'),
    path('orders/',views.OrdersView.as_view(),name='orders'),
]