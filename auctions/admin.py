from django.contrib import admin

from .models import Listing,User,Category

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Category)


# Register your models here.
