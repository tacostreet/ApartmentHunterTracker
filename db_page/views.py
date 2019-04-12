from django.shortcuts import render_to_response
from django.http import HttpResponse

from .models import HoustonListings

# Create your views here.
def index(request):
    return render_to_response('db_page.tmpl', {'obj': HoustonListings.objects.all()})