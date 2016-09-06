from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
def home(request):
    # reset session for debugging
    request.session['voted'] = [];
    context = {}
    return render(request, "main/index.html", context)