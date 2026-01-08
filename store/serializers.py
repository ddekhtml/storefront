from django.db.models import Count, Sum
from django.db import transaction
from rest_framework import serializers
from decimal import Decimal
from .models import Collection, Product, Review, Cart, CartItems, Customer, Order, OrderItems, ProductImage
from .signals import order_created

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = ["payment_status"]
        
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductImage
        fields = ['id', 'image']
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return ProductImage.objects.create(product_id=product_id, **validated_data)

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    def validate_cart_id(self, cart_id):
        if Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with given ID was found')
        if CartItems.objects.filter(cart_id= cart_id).count()==0:
            raise serializers.ValidationError('The cart is empty')
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            # print(self.validated_data['cart_id'])
            # print(self.context['user_id'])
            customer_id= Customer.objects.get(user_id= user_id)
            order = Order.objects.create(customer=customer_id)
            cart_items = CartItems.objects.\
                select_related('product').\
                    filter(cart_id=cart_id)
            order_items = [
                    OrderItems(
                    order=order, 
                    product = item.product, 
                    unit_price = item.product.price,
                    quantity = item.quantity
                ) for item in cart_items
            ]
            OrderItems.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()
            order_created.send_robust(self.__class__, order=order)
            return order
            

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =["id", "title", "price"]

class OrderItemsSerializer(serializers.ModelSerializer):
    product= SimpleProductSerializer()
    class Meta:
        model = OrderItems
        fields =["id", "product", "quantity", 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)
    class Meta: 
        model=Order 
        fields =['id', 'customer', 'placed_at', 'payment_status', "items"]
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model= Customer
        fields =['id', 'user_id', 'phone', 'birth_date', 'membership']

class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Collection
        fields = ["id", "title", "product_count"]
    
class ProductSerializer(serializers.ModelSerializer):
    images= ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title','description', 'slug', 'inventory', 'price_with_tax', 'price', 'collection', 'images']
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