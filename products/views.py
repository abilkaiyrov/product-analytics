from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from django.views.generic import TemplateView

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class IndexView(TemplateView):
    template_name = 'products/index.html'
