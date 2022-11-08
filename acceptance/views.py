from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from goods.models import Barcode
from .forms import SupplierForm
from .models import AcceptanceDocs, SupplierPrice, AcceptanceGoods
from goods.models import Balance
import json
import datetime

# Create your views here.
@login_required
def new_acceptance(request):
    form = SupplierForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            rqst = request.POST
            doc = form.save()
            goods = json.loads(rqst['data'])
            for good in goods:
                save_goods = AcceptanceGoods(quantity=int(good['qty']), document_id=doc.id, good_id=int(good['id']), purchase_price=float(good['supp_price']))
                save_goods.save()
                balance_exists = Balance.objects.filter(good_id=int(good['id'])).first()
                if balance_exists:
                    new_qty = balance_exists.quantity + int(good['qty'])
                    balance_exists.quantity = new_qty
                    balance_exists.save()
                else:
                    new_balance = Balance(good_id=int(good['id']), quantity=int(good['qty']))
                    new_balance.save()
            return JsonResponse({'id': doc.id})
    context = { 'form': form }
    return render(request, 'acceptance/new_acceptance.html', context)

@login_required
def acceptance_detail(request, pk):
    if request.method == 'POST':
        post_supplier_id = int(request.POST.get('supplier'))
        post_doc_date = datetime.datetime.fromisoformat(request.POST.get('doc_date'))
        post_goods = json.loads(request.POST.get('data'))
        
        acceptance_doc = AcceptanceDocs.objects.get(pk=pk)
        acceptance_goods = AcceptanceGoods.objects.filter(document_id=pk)
        if post_supplier_id != acceptance_doc.supplier_id:
            acceptance_doc.supplier_id = post_supplier_id
        if post_doc_date != acceptance_doc.doc_date:
            acceptance_doc.doc_date = post_doc_date
        acceptance_doc.save()   

        for post_good in post_goods:
            check_same = False
            for acc_good in acceptance_goods:
                if int(post_good['id']) == acc_good.good_id:
                    check_same = True
                    if acc_good.purchase_price != float(post_good['supp_price']):
                        acc_good.purchase_price = float(post_good['supp_price'])
                        acc_good.save()
                    if acc_good.quantity != int(post_good['qty']):
                        difference = acc_good.quantity - int(post_good['qty'])
                        balance_good = Balance.objects.get(good_id=acc_good.good_id)
                        if difference > 0:
                            balance_good.quantity = balance_good.quantity - difference
                        else:
                            balance_good.quantity = balance_good.quantity + abs(difference)
                        balance_good.save()
                        acc_good.quantity = int(post_good['qty'])
                        acc_good.save()
                    break
            if not check_same:
                new_good = AcceptanceGoods(good_id=int(post_good['id']), quantity=int(post_good['qty']), document_id=pk, purchase_price=float(post_good['supp_price']))
                balance_exists = Balance.objects.filter(good_id=int(post_good['id'])).first()
                if balance_exists:
                    new_qty = balance_exists.quantity + int(post_good['qty'])
                    balance_exists.quantity = new_qty
                    balance_exists.save()
                else:
                    new_balance = Balance(good_id=int(post_good['id']), quantity=int(post_good['qty']))
                    new_balance.save()
                new_good.save()
    
        for acc_good in acceptance_goods:
            if check_same:
                check_same = False
            for post_good in post_goods:
                if acc_good.good_id == int(post_good['id']):
                    check_same = True
                    break
            if not check_same:
                print(acc_good.id)
                balance_exists = Balance.objects.get(good_id=acc_good.good_id)
                new_qty = balance_exists.quantity - acc_good.quantity
                if new_qty > 0:
                    balance_exists.quantity = new_qty
                    balance_exists.save()
                else:
                    balance_exists.delete()
                acc_good.delete()
        return JsonResponse({'status':1})


@login_required
def search_acceptance_good(request):
    if request.method == 'POST':
        context = {}
        barcode = Barcode.objects.filter(barcode=request.POST.get('search_book')).first()
        if barcode:
            supp_price_obj = SupplierPrice.objects.filter(good_id=barcode.good_id)
            if supp_price_obj:
                supp_price = supp_price_obj.order_by('-datetime')[0].price
            else:
                supp_price = 0
            context = {
                'id': barcode.good_id,
                'name': str(barcode),
                'supp_price': supp_price,
                'price': barcode.good.price
            }
        return JsonResponse(context)