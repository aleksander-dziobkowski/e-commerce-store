from django.urls import path
from . import views 

urlpatterns = [
    path('products/',views.ProductsList.as_view(),name='api-products-list'),
    path('products/<int:pk>/',views.ProductDetail.as_view(),name='api-product-detail'),
    path('products/<int:pk>/reviews/',views.ReviewsList.as_view(),name='api-product-reviews'),
    path('reviews/<int:pk>/',views.ReviewDetail.as_view(),name='api-review-detail'),
    path('reviews/<int:pk>/comments/',views.ReviewCommentsList.as_view(),name='api-review-comments-list'),
    path('comments/<int:pk>/',views.ReviewCommentDetail.as_view(),name='api-review-comment-detail'),
]
