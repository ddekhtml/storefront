from django.contrib import admin
from .models  import Collection, Product, Customer, Address, Cart, Order, OrderItems, ProductImage
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
# Register your models here.
class InvetoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name="inventory"
    def lookups(self, request, model_admin):
        return [
            (
            '<10', 'Low'
            ), (
            '>=25', 'High'
            ), (
            '<25', 'Ok'
            )
        ]
    def queryset(self, request, queryset):
        if self.value()=='<10':
            return queryset.filter(inventory__lte=10)
        elif self.value()== '>=25':
            return queryset.filter(inventory__gte=25)
        elif self.value()=='<25':
            return queryset.filter(inventory__range=(11,24))

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields=['thumbnail'] 
    def thumbnail(self, instance):
        if instance.image:
            return format_html(
                '<img src="{}" class="thumbnail" />',
                instance.image.url
            )
        return "-"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields= ["title", "slug", "description", "price" ,"inventory", "last_update", "collection", "promotion"]
    prepopulated_fields = {
        'slug': ['title']
    }
    search_fields = ["title"]
    readonly_fields = ["last_update"]
    autocomplete_fields= ["collection"]
    actions = ["inventory_to_ten"]
    list_display = ['title', 'price', 'inventory_status', "collection_title"]
    list_editable = ['price']
    ordering = ["title", "collection"]
    list_select_related = ["collection"]
    list_filter = ["collection", "last_update", InvetoryFilter]
    inlines =[ProductImageInline]
    def collection_title(self, product):
        return product.collection.title
    def inventory_status(self, product):
        if product.inventory <=10 :
            return 'LOW'
        elif product.inventory>=25:
            return 'HIGH'
        else :
            return 'OK'
    
    @admin.action(description="Inventory To Ten")
    def inventory_to_ten(self, request, queryset):
        updated_count= queryset.update(inventory= 10)
        self.message_user(request, f"{updated_count} has changed")
    
    class Media:
        css ={
            'all': ['store/styles.css']
        }
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display= ["title", "product_count"]
    search_fields = ["title"]
    def product_count(self, collection):
        url = reverse("admin:store_product_changelist"
                      ) + "?" + urlencode({
                          "collection__id" : collection.id
                      })
        return format_html("<a href={}>{}</a>", url, collection.product_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count = Count("product"))
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display =["first_name", "last_name","membership"]
    ordering = ["membership"]
    list_select_related=["user"]
    search_fields =["first_name__istartswith", "last_name__istartswith"]
    @admin.display(ordering=["full_name", "membership"])
    def full_name(self, customer):
        return f"{customer.first_name} {customer.last_name}"

class OrderItemsInline(admin.TabularInline):
    model = OrderItems  
    autocomplete_fields = ["product"]
    
    
@admin.register(Order)
class OrderAdmin (admin.ModelAdmin):
    fields = ["customer", "placed_at", "payment_status"]
    readonly_fields = ["placed_at"]
    autocomplete_fields = ["customer"]
    list_display = ["placed_at", "customer_email", "payment_status"]
    list_editable = ["payment_status"]
    list_select_related = ["customer"]
    inlines = [OrderItemsInline]

    def customer_email(self, order):
        return order.customer.email



@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    search_fields =["product"]
    select_related = ["product"]