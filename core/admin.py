from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets =(
        (
            None, {
                'classes': ('wide',), 
                'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'), 
            }
        ),
    )

class TaggedItemInline(GenericTabularInline):
    model = TaggedItem

class CustomProductAdmin(ProductAdmin):
    inlines = [TaggedItemInline] 

admin.site.unregister(Product)              # ❌ lepas admin default
admin.site.register(Product, CustomProductAdmin)   # ✅ pasang admin baru
