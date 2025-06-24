from django.urls import path
from .views import IndexView
from .api_views import product_list_api

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/products/', product_list_api, name='product_list_api'),
]