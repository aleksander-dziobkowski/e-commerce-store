from django.db import models
from django.contrib.auth.models import User

class MainCategory(models.Model):
    name = models.CharField(max_length=100,unique=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    main_category = models.ForeignKey(MainCategory,on_delete=models.CASCADE,related_name='categories')

    def __str__(self):
        return self.name + " " + f"({self.main_category.name})"

class Product(models.Model):
    IMAGES_LIMIT = 5

    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    avg_rating = models.FloatField(default=0)
    sum_rating = models.IntegerField(default=0)

    @property
    def thumb(self):
        return self.images.order_by('order').first()


    def __str__(self):
        return self.name

    def update_rating_on_review_delete(self, rating_to_remove):
        if self.sum_rating > 1:
            total_sum = self.avg_rating * self.sum_rating
            total_sum -= rating_to_remove
            self.sum_rating -= 1
            self.avg_rating = total_sum / self.sum_rating
        else:
            self.sum_rating = 0
            self.avg_rating = 0
        self.save()

    def update_rating_on_review_add(self, new_rating):
        total_sum = self.avg_rating * self.sum_rating
        total_sum += new_rating
        self.sum_rating += 1
        self.avg_rating = total_sum / self.sum_rating
        self.save()
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    order = models.PositiveIntegerField(default=0)
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image {self.order} for {self.product.name}"

    def save(self, *args, **kwargs):

        if self.product.images.count() >= Product.IMAGES_LIMIT and not self.pk:
            raise ValueError("Możesz dodać maksymalnie 5 zdjęć dla produktu.")
        
        if not self.alt_text:
            self.alt_text = self.product.name

        super().save(*args, **kwargs)

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Mężczyzna'),
        ('F', 'Kobieta'),
        ('O', 'Inne'),        
    ]

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES, blank=True, null=True)
    creation_date = models.DateField(auto_now=True)
    liked_products = models.ManyToManyField(Product,related_name="liked_by",blank=True, null=True)

class Order(models.Model):
    PAYMENT_STATUS_MAP = {
        "NEW": "Oczekuje na płatność",
        "PENDING": "Przetwarzanie płatności",
        "WAITING_FOR_CONFIRMATION": "Oczekuje na potwierdzenie",
        "COMPLETED": "Opłacone",
        "CANCELED": "Anulowane",
    }
    PAYMENT_STATUS_COLOR = {
        "NEW": "warning",     
        "PENDING": "warning",    
        "WAITING_FOR_CONFIRMATION": "warning", 
        "COMPLETED": "success",
        "CANCELED": "danger",   
    }
    
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    payu_order_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default="NEW")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"ORDER:{self.id}"

    def get_status_display(self):
        return self.PAYMENT_STATUS_MAP.get(self.status, self.status)
    
    def get_status_color(self):
        return self.PAYMENT_STATUS_COLOR.get(self.status, "secondary")
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    size = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"ORDER ITEM {self.product.name} x{self.quantity} (rozmiar: {self.size})"

