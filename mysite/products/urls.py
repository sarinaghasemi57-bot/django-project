from django.urls import path
from . import views

urlpatterns = [
    path("", views.products, name="products"),
    path("about/", views.about, name="about"),
    path("<int:id>/", views.product_detail, name="product_detail"),
    path("add-product/", views.add_product, name="add_product"),
    path("edit/<int:id>/",views.edit_product,name="edit_product"),
    path("delete/<int:id>/", views.delete_product, name="delete_product"),
    path("cart/add/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/remove/<int:id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/increase/<int:id>/", views.increase_cart, name="increase_cart"),
    path("cart/decrease/<int:id>/", views.decrease_cart, name="decrease_cart"),
    ]