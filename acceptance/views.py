from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def new_acceptance(request):
    return render(request, 'acceptance/new_acceptance.html')