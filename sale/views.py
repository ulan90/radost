from django.shortcuts import render
from django.contrib.auth.decorators import login_required #для функций
#from goods.models import Barcode, Good

# Create your views here.
@login_required
def sale(request):
    #context = {}
    return render(request, 'sale/sale.html')#, context)

"""@login_required
def search_good(request):
    context = {}
    book_barcode = request.POST.get('search_book')
    if book_barcode:
        try:
            barcode = Barcode.objects.get(barcode=book_barcode)
        except Barcode.DoesNotExist:
            barcode = None
        if barcode:
            good = Good.objects.get(id=barcode.good_id)
            context = {'id': good.id, 'name': good.name, 'price': good.price}
    return render(request, 'sale/partials/find_good.html', context)"""