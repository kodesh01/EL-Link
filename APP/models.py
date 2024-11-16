from django.db import models
import time, os



def generate_filename_with_timestamp(instance, filename):
    timestamp = time.strftime('%Y%m%d_%H%M%S')  
    file_extension = filename.split('.')[-1]  
    return os.path.join(f'{timestamp}_{filename}') 



class User(models.Model):
    fullname = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    def __str__(self):
        return self.email  # Or return a combination of fields

class ProductCategory(models.Model):
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to=generate_filename_with_timestamp, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

class BrandProductCategory(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to=generate_filename_with_timestamp, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)  
    description = models.TextField()




class BrandProductList(models.Model):
    brand_product_category = models.ForeignKey(BrandProductCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to=generate_filename_with_timestamp, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    pdf = models.FileField(upload_to=generate_filename_with_timestamp, blank=True, null=True)
