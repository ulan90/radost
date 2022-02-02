from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.decorators import login_required #для функций
from django.core.paginator import Paginator
from .models import Good

# Create your views here.
class GoodListView(LoginRequiredMixin, ListView):
    model = Good
    paginate_by = 2 #use your paginated  value here
    ordering = ['name']
    template_name = 'goods/goods.html' # your own template
    context_object_name = "goods"
    
    def get_queryset(self):
        query = self.request.GET.get('search_good')
        if query:
            good_list = self.model.objects.filter(name__icontains=query).order_by('name')
        else:
            good_list = self.model.objects.all().order_by('name')
        return good_list