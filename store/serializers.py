from rest_framework import serializers
from decimal import Decimal
from .models import Collection, Product, Review, Cart, CartItems
from django.db.models import Count, Sum

class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Collection
        fields = ["id", "title", "product_count"]
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','description', 'slug', 'inventory', 'price_with_tax', 'price', 'collection']
    price_with_tax = serializers.SerializerMethodField(method_name="price_tax")
    # collection= serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(), 
    #     view_name= "collection-detail", 

    # )
    def price_tax(self, product):
        return product.price * Decimal(1.1)

class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =["id", "title", "price"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields =["quantity"]
    

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItems
        fields =["id", "product_id", "quantity"]

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with that value')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try: 
            cart_item=CartItems.objects.get(cart_id= cart_id, product_id= product_id)
            cart_item.quantity+=quantity
            cart_item.save()
            self.instance = cart_item
        except CartItems.DoesNotExist:
            self.instance= CartItems.objects.create(cart_id= cart_id, **self.validated_data)
        return self.instance
    # biar hasilnya langsung diambil/ disimpan jadi engga cuma action aja
    
class CartItemsSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price= serializers.SerializerMethodField()
    def get_total_price(self, cartitem):
        return cartitem.product.price * cartitem.quantity
    class Meta:
        model = CartItems
        fields =["id", "product", "quantity", "total_price"]

class ReviewSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Review
        fields =['id', 'name', 'description']
    def create(self, validated_data):
        product_id =self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemsSerializer(many=True, read_only= True)
    total_price= serializers.SerializerMethodField()
    def get_total_price(self, cart:Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model= Cart
        fields = ["id", "items", "total_price"]
# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length = 255)
#     price= serializers.DecimalField(max_digits=6, decimal_places=2)
#     price_with_tax = serializers.SerializerMethodField(method_name="price_tax")
#     # collection = serializers.PrimaryKeyRelatedField(queryset = Collection.objects.all())
#     collection= serializers.StringRelatedField()
#     def price_tax(self, product):
#         return product.price * Decimal(1.1)