from rest_framework import serializers
from .models import Review, ReviewComment
from store.models import Product
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class ReviewCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = ReviewComment
        exclude = ('review',)
        
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = ReviewCommentSerializer(many=True,read_only=True)
    
    class Meta:
        model = Review
        exclude = ('product',)
    
class ProductSerializer(serializers.ModelSerializer):
    #reviews = ReviewSerializer(many=True,read_only=True)
    
    class Meta:
        model = Product
        exclude = ('avg_rating','sum_rating')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  