from django.contrib import admin
from .models import User,ProductCategory,BrandProductCategory,BrandProductList


admin.site.register([User,ProductCategory,BrandProductCategory,BrandProductList])