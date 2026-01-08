from django.urls import path
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("product", views.ProductViewSet, basename="product")
router.register("collection", views.CollectionViewSet)
router.register("carts", views.CartViewSet)
router.register('customer', views.CustomerViewSet)
router.register('orders', views.OrderViewset, basename="orders")

carts_router= routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename="cart-items")

product_router = routers.NestedDefaultRouter(router, 'product', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename ="product-reviews")
product_router.register('images', views.ProductImageView, basename="product-images")
urlpatterns = router.urls + product_router.urls+ carts_router.urls 

# urlpatterns = [
#     # path("product/", views.product_list),
#     # path('product/<int:id>/', views.product_detail), 
#     path("product/", views.ProductList.as_view()),
#     path('product/<int:pk>/', views.ProductDetail.as_view()), 
#     path('collection/', views.CollectionList.as_view()),
#     path('collection/<int:pk>/', views.CollectionDetail.as_view(), name="collection-detail")
# ]
