from django.http import JsonResponse
from products.models import Product

def product_list_api(request):
    products = Product.objects.all()
    data = [p.as_dict() for p in products]
    return JsonResponse(data, safe=False)