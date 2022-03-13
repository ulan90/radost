from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required #для функций
from django.http.response import JsonResponse
from goods.models import Barcode, Good, Balance, IzlishkiTovara
from .models import SoldGoods
import datetime

# Create your views here.
@login_required
def sale(request):
    if request.method == 'POST':
        good_id = request.POST.getlist('good_id')
        good_qty = request.POST.getlist('good_quantity')
        try:
            new_receipt = SoldGoods.objects.last().receipt_id + 1
        except AttributeError:
            new_receipt = 1
        if(len(good_id) == len(good_qty)):
            same_receipt = SoldGoods.objects.filter(receipt_id=new_receipt).first()
            if not same_receipt:
                for i in range(len(good_id)):
                    good = get_object_or_404(Good, pk=good_id[i])
                    create_receipt = SoldGoods(
                        receipt_id = new_receipt,
                        good_id = good_id[i],
                        quantity = good_qty[i],
                        sold_price = good.price,
                        sold_sum = good.price * int(good_qty[i]),
                        datetime = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M:%S")
                    )
                    create_receipt.save()

                    try:
                        balance_good = Balance.objects.get(good_id=good_id[i])
                    except Balance.DoesNotExist:
                        balance_good = None
                    
                    if balance_good:
                        balance_qty = balance_good.quantity - int(good_qty[i])
                        if balance_qty > 0:
                            balance_good.quantity = balance_qty
                            balance_good.save()
                        elif balance_qty == 0:
                            balance_good.delete()
                        else:
                            balance_good.delete()
                            _izlishka_insert_update(good_id[i], balance_qty)
                    else:
                        _izlishka_insert_update(good_id[i], int(good_qty[i]))

        return redirect("sale")
    
    return render(request, 'sale/sale.html')


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


def _izlishka_insert_update(myId, myQty):
    try:
        izlishka = IzlishkiTovara.objects.get(good_id=myId)
    except IzlishkiTovara.DoesNotExist:
        izlishka = None
    if izlishka:
        izlishka.quantity += abs(myQty)
        izlishka.save()
    else:
        izlishka_insert = IzlishkiTovara(good_id=myId, quantity=abs(myQty))
        izlishka_insert.save()