from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Count
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemsSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from .models import Product, Collection, OrderItems, Review, Cart, CartItems
from .filters import ProductFilter
from .pagination import DefaultPagination

class CartItemViewSet(ModelViewSet):
    lookup_field= 'pk'
    http_method_names=['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemsSerializer
    def get_queryset(self):
        return CartItems.objects.select_related("product").filter(cart_id=self.kwargs["cart_id"])
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_id"]}
    
class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer
    lookup_field="id"


class ProductViewSet(ModelViewSet):
    queryset= Product.objects.select_related("collection").all()
    serializer_class = ProductSerializer 
    lookup_field="pk"
    filter_backends =[DjangoFilterBackend, SearchFilter]
    # filterset_fields =["collection_id"]
    # pagination_class= DefaultPagination
    filterset_class = ProductFilter 
    search_fields= ["title", "description"]

    # def get_queryset(self):
    #     queryset= Product.objects.select_related("collection").all()
    #     collection_id = self.request.query_params.get("collection_id")
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id= collection_id)
    #     return queryset
    def get_serializer_context(self):
        return {"request": self.request}
    def destroy(self, request, *args, **kwargs):
        if OrderItems.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':"Product can't be deleted cause associated with orderitem"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    # def destroy(self,request,pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitems_set.count()>0:
    #         return Response({'error':"Product can't be deleted cause associated with orderitem"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
    queryset= Collection.objects.annotate(product_count =Count("product")).all()
    serializer_class= CollectionSerializer
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id= kwargs["pk"]).count()>0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    # def destroy(self, request, pk):
    #     collection = Collection.objects.annotate(product_count=Count("product")).get(pk=pk)
    #     if collection.product_count> 0:
    #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    
    serializer_class= ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

# # Create your views here.
# class ProductList(ListCreateAPIView):
#     queryset= Product.objects.select_related("collection").all()
#     serializer_class = ProductSerializer 
#     # def get_queryset(self):
#     #     return Product.objects.select_related("collection").all()
#     # def get_serializer_class(self):
#     #     return ProductSerializer
#     def get_serializer_context(self):
#         return {"request": self.request}
    

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset= Product.objects.all()
#     serializer_class = ProductSerializer
#     def delete(self,request,pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems_set.count()>0:
#             return Response({'error':"Product can't be deleted cause associated with orderitem"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# class CollectionList(ListCreateAPIView):
#     queryset= Collection.objects.annotate(product_count =Count("product")).all()
#     serializer_class= CollectionSerializer

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(product_count= Count("product")).all()
#     serializer_class= CollectionSerializer
#     lookup_field= 'pk'
#     def delete(self, request, pk):
#         collection = Collection.objects.annotate(product_count=Count("product")).get(pk=pk)
#         if collection.product_count> 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# class ProductList(APIView):
#     def get(self, request):
#         products = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(products, many=True, context={"request": request})
#         return Response(serializer.data)
#     def post(self,request):
#         serializer= ProductSerializer(data=request.data)
#         # print (serializer)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()
#         # print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED )

# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, context={"request": request})
#         return Response(serializer.data)
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer=ProductSerializer(product, data=request.data,  context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self,request,id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems_set.count()>0:
#             return Response({'error':"Product can't be deleted cause associated with orderitem"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

        

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method =='GET':
#         products = Product.objects.select_related("collection").all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#     elif request.method=='POST':
#         # print(request.data)
#         serializer= ProductSerializer(data=request.data)
#         # print (serializer)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()
#         # print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED )

# @api_view(['GET', 'PUT','DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method =='GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method =='PUT':
#         serializer=ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method =='DELETE':
#         if product.orderitems_set.count()>0:
#             return Response({'error':"Product can't be deleted cause associated with orderitem"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method =='GET':
#         collection = Collection.objects.annotate(product_count =Count("product")).all()
#         serializer = CollectionSerializer(collection, many=True)
#         return Response(serializer.data)
#     elif request.method =='POST':
#         serializer= CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()
#         return Response("Collection has been created", status=status.HTTP_201_CREATED)


# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = Collection.objects.annotate(product_count=Count("product")).get(pk=pk)
#     if request.method =='GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method =='PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()
#         return Response("Collection has been updated", status= status.HTTP_200_OK)
#     elif request.method =='DELETE':
#         if collection.product_count> 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)