from django.shortcuts import render
from django.contrib.auth.decorators import login_required #для функций

# Create your views here.
@login_required
def sale(request):
    context = {}
    return render(request, 'sale/sale.html', context)