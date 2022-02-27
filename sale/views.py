from django.shortcuts import render
from django.contrib.auth.decorators import login_required #для функций
from django.http.response import JsonResponse
from goods.models import Barcode, Good

# Create your views here.
@login_required
def sale(request):
    #context = {}
    return render(request, 'sale/sale.html')#, context)

@login_required
def search_good(request):
    context = {}
    barcode = Barcode.objects.filter(barcode=request.POST.get('search_book')).first()
    if barcode:
        context = {
            'id': barcode.good_id,
            'name': str(barcode),
            'price': barcode.good.price
        }
    return JsonResponse(context)