from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse
from jsonfield import JSONField


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    icon = models.ImageField(blank=True)
    is_public = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_detail', kwargs={"pk": self.pk})
    

class Shop(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    desc = models.TextField(blank=True)
    latlng = models.CharField(max_length=100, blank=True) ##Geojango 활용해서 바꿔보기 나중에일!
    photo = models.ImageField(blank=True)
    is_public = models.BooleanField(default=False, db_index=True)
    meta = JSONField()   #NoSQL적 특성
                        #PostgreSQL의 JSONField와 다르다.

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:shop_detail', kwargs={"pk": self.pk})
    

    @property
    def address(self):
        return self.meta.get('address')

class Review(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True)
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    massage = models.TextField()

    def __str__(self):
        return self.author

class Item(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    desc = models.TextField(blank=True)
    amount = models.PositiveIntegerField()
    photo = models.ImageField(blank=True)
    is_public = models.BooleanField(default=False, db_index=True)     
    meta = JSONField()

    def __str__(self):
        return self.name

#class Order(models.Model):
 #   pass      
