from rest_framework import serializers
from decimal import Decimal
from .models import Collection, Product, Review
from django.db.models import Count
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

class ReviewSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Review
        fields =['id', 'name', 'description']
    def create(self, validated_data):
        product_id =self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length = 255)
#     price= serializers.DecimalField(max_digits=6, decimal_places=2)
#     price_with_tax = serializers.SerializerMethodField(method_name="price_tax")
#     # collection = serializers.PrimaryKeyRelatedField(queryset = Collection.objects.all())
#     collection= serializers.StringRelatedField()
#     def price_tax(self, product):
#         return product.price * Decimal(1.1)