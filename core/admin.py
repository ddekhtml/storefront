from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem

class TaggedItemInline(GenericTabularInline):
    model = TaggedItem

class CustomProductAdmin(ProductAdmin):
    inlines = [TaggedItemInline] 

admin.site.unregister(Product)              # ❌ lepas admin default
admin.site.register(Product, CustomProductAdmin)   # ✅ pasang admin baru
