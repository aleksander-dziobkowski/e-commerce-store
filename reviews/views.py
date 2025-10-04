from django.shortcuts import render
from rest_framework import generics
from .models import Review, ReviewComment
from store.models import Product
from .serializers import ReviewSerializer, ProductSerializer, ReviewCommentSerializer, MyTokenObtainPairSerializer
from .permissions import IsAuthor
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView

class ProductsPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size" 
    max_page_size = 9

class ReviewsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10
    
class ReviewCommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10

@extend_schema(tags=['Product'])
class ProductsList(generics.ListAPIView):
    """ Returns list of products by main category and category """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "category__main_category"]
    pagination_class = ProductsPagination
    
@extend_schema(tags=['Product'])
class ProductDetail(generics.RetrieveAPIView):
    """ Returns product by ID """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

@extend_schema(tags=['Review'])
class ReviewsList(generics.ListCreateAPIView):
    """
        GET: Returns products reviews list\n
        POST: Add a new review for product
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ReviewsPagination

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['pk'])
    
    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs['pk'])
        user = self.request.user

        if product.reviews.filter(author=user).exists():
            raise ValidationError('Review for this product already exists')

        product.update_rating_on_review_add(serializer.validated_data['rating'])
        serializer.save(product=product, author=user)
    
@extend_schema(tags=['Review'])
class ReviewDetail(generics.RetrieveDestroyAPIView):
    """
        GET: Returns review by ID\n
        DELETE: Delete the review by ID (Only owner can delete the review)
    """
    permission_classes = [IsAuthor]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_destroy(self, instance):
        product = instance.product
        product.update_rating_on_review_delete(instance.rating)
        instance.delete()
        
@extend_schema(tags=['Comment'])        
class ReviewCommentsList(generics.ListCreateAPIView):
    """
        GET: Returns review comments list\n
        POST: Add a new comment for review
    """
    serializer_class = ReviewCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ReviewCommentPagination
    
    def get_queryset(self):
        review_pk = self.kwargs['pk']
        review_comments = ReviewComment.objects.filter(review_id=review_pk)
        return review_comments

    def perform_create(self, serializer):
        review_pk = self.kwargs.get('pk')

        review = Review.objects.get(pk=review_pk)
        
        user = self.request.user
        review_comment = review.comments.filter(author=user)
        if review_comment.exists():
            raise ValidationError('Review for this movie exists')
        
        serializer.save(review=review,author=user)
        
@extend_schema(tags=['Comment'])         
class ReviewCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        GET: Returns comment by ID\n
        DELETE: Delete the comment by ID (Only owner can delete the comment)\n
        PATCH: Update content of the comment
    """
    permission_classes = [IsAuthor]
    serializer_class = ReviewCommentSerializer
    queryset = ReviewComment.objects.all()
    http_method_names = ['get', 'patch', 'delete']
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer