from django.db import models
from store.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Review(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    content = models.TextField(max_length=500)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

class ReviewComment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews_comments')
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField(max_length=500)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)