from django.urls import path
from . import views



app_name = "cart"

urlpatterns = [
    path('detail', views.CartDetailView.as_view(), name= "cart_detail"),
    path('add/<int:pk>', views.CartAddView.as_view(), name= "cart_add"),
    path('delete/<str:id>', views.CartDeleteView.as_view(), name= "cart_delete"),
    path('empty', views.CartEmptyView.as_view(), name= "cart_empty"),
    path('order/detail<int:pk>', views.OrderDetailView.as_view(), name="order_detail"),
    path('apply/', views.OrderCreationView.as_view(), name="order_create"),
    path('order/<int:pk>', views.ApplyDiscountView.as_view(), name="discount_code"),
    path('request/<int:pk>', views.request_payment, name='request'),
    path('verify/', views.VerifyView.as_view(), name='verify'),
   ]