from django.shortcuts import render_to_response
from django.http import HttpResponse
import requests

from .models import HoustonListings

# Create your views here.
def index(request):
    return render_to_response('template.tmpl', {'obj': HoustonListings.objects.all()})