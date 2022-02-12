from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required #для функций
from django.http import QueryDict
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from .models import Good
from .forms import GoodForm

# Create your views here.
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
    if request.method == "POST":
        if form.is_valid():
            form.save()
            form = GoodForm()
    return redirect("goods")

@login_required
def update_good(request, pk):
    good = get_object_or_404(Good, pk=pk)
    form = GoodForm(instance=good)
    if request.method == "PUT":
        data = QueryDict(request.body).dict()
        form = GoodForm(data, instance=good)
        if form.is_valid():
            form.save()
            return render(request, "goods/partials/good_detail.html", {"good": good})
    return render(request, "goods/partials/good_update.html", {"form": form, "good": good})

@login_required
def delete_good(request, pk):
    try:
        good = Good.objects.get(id = pk)
        good.delete()
    except:
        print("Record doesn't exists")
    return HttpResponse('')