from django.db import models

class Members(models.Model):
    class MemberRole(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        DELIVERY_CREW = 'DELIVERY_CREW', 'Delivery Crew'
        CUSTOMER = 'CUSTOMER', 'Customer'

    username = models.CharField(max_length=100);
    password = models.CharField(max_length=100);
    role = models.CharField(max_length=100, choices=MemberRole.choices, default=MemberRole.ADMIN);
    city = models.CharField(max_length=100);
    
    def __str__(self):
        return self.username

class Order(models.Model):
    name = models.CharField(max_length=225);
    category = models.CharField(max_length=100);
    price = models.DecimalField(max_digits=5, decimal_places=2);
    city = models.CharField(max_length=100);
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MenuItems(models.Model):
    title = models.CharField(max_length=225);
    price = models.DecimalField(max_digits=5, decimal_places=2);
    category = models.IntegerField();
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
