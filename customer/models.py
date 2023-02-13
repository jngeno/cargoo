from django.db import models

class ServiceItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='service_images/')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='items')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
 
class ServiceModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('ServiceItem', related_name='service', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    town = models.CharField(max_length=50, blank=True)
    county = models.CharField(max_length=20, blank=True)
    number = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    

    def __str__(self):
        return f'Service: {self.created_on.strftime("&b %d %I: %M %p")}'