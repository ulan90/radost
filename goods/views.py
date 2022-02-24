from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required #для функций
from django.http import QueryDict
from django.http.response import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from .models import Good, Barcode
from .forms import GoodForm, BarcodeForm


@login_required
def good_list(request):
    q = request.GET.get('search_good')
    page = request.GET.get('page')
    form = GoodForm(request.POST or None)
    if q:
        p = Paginator(Good.objects.filter(name__icontains=q).order_by('name'), 2)
        goods = p.get_page(page)
        return render(request, "goods/partials/goods_search.html", {"goods": goods})
    elif page or q=="":
        p = Paginator(Good.objects.all().order_by('name'), 2)
        goods = p.get_page(page)
        return render(request, "goods/partials/goods_search.html", {"goods": goods})
    else:
        p = Paginator(Good.objects.all().order_by('name'), 2)
        goods = p.get_page(page)
        return render(request, "goods/goods.html", {"goods": goods, "form": form})

@login_required
def create_good(request):
    form = GoodForm(request.POST or None)
    barcodes = request.POST.getlist('barcode')
    for bar in barcodes:
        found_barcode = Barcode.objects.filter(barcode=bar).first()
        if found_barcode:
            context = {"barcode": found_barcode.barcode, "id": found_barcode.good_id, "name": str(found_barcode)}
            return render(request, "goods/partials/barcode_duplicate.html", context)
    
    if request.method == "POST":
        if form.is_valid():
            new_good = form.save()
            for barcode in barcodes:
                Barcode.objects.create(good_id=new_good.pk, barcode=barcode)
    return redirect("goods")

@login_required
def edit_good(request, pk):
    good = get_object_or_404(Good, pk=pk)
    form = GoodForm(instance=good)
    barcodes = Barcode.objects.filter(good_id=pk)
    return render(request, "goods/partials/good_create.html", {"form": form, "good": good, "barcodes": barcodes })

@login_required
def update_good(request, pk):
    good = get_object_or_404(Good, pk=pk)
    barcodes = request.POST.getlist('barcode')
    for bar in barcodes:
        found_barcode = Barcode.objects.filter(barcode=bar).first()
        if found_barcode and found_barcode.good_id != pk:
            context = {"barcode": found_barcode.barcode, "id": found_barcode.good_id, "name": str(found_barcode)}
            return render(request, "goods/partials/barcode_duplicate.html", context)
    
    if request.method == "POST":
        data = QueryDict(request.body).dict()
        form = GoodForm(data, instance=good)
        if form.is_valid():
            form.save()
            Barcode.objects.filter(good_id=pk).delete()
            for barcode in barcodes:
                Barcode.objects.create(good_id=pk, barcode=barcode)
    return redirect("goods")

@login_required
def delete_good(request, pk):
    try:
        good = Good.objects.get(id = pk)
        good.delete()
    except:
        print("Record doesn't exists")
    return HttpResponse('')

@login_required
def check_barcode(request):
    if request.method == "POST":
        barcodes = request.POST.getlist('barcode')
        good_id = request.POST.get('gid')
        if not good_id:
            good_id=0
        for barcode in barcodes:
            found_barcode = Barcode.objects.filter(barcode=barcode).first()
            if found_barcode and int(good_id) != found_barcode.good_id:
                good = 'код:' + str(found_barcode.good_id) + ' наименование:' + str(found_barcode)
                return JsonResponse({'status': 1, 'good': good})
    return JsonResponse({'status':0})