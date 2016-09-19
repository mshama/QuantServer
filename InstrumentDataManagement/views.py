from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.db.models import Max
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# build in libraries
import pandas as pd
from _datetime import datetime

# own libraries
from dataconnections.datasource import get_metaData, get_PriceData

# models import

# forms import
from .forms import newMarketDataTypeForm,newMarketForm,newInstrumentForm

# Create your views here.

def index(request):
    context = {'message': 'this is the data management home'}
    return render(request, 'InstrumentDataManagement/index.html', context)

def newInstrument(request):
    if request.method == 'POST':
        if 'newInstrument' in request.POST:
            form = newInstrumentForm(request.POST)            
        elif 'newMarketDataType' in request.POST:
            newMarketDataType(request)
        elif 'newMarket' in request.POST:
            newMarket(request)
    instrumentForm = newInstrumentForm()
    marketDataTypeForm = newMarketDataTypeForm()
    marketForm = newMarketForm()
    
    context = {
               'message': 'this is the data management home',
               'instrumentForm': instrumentForm,
               'marketDataTypeForm': marketDataTypeForm,
               'marketForm': marketForm,
               }
    return render(request, 'InstrumentDataManagement/newInstrument.html', context)

def newMarketDataType(request):
        form = newMarketDataTypeForm(request.POST)
        if not form.save():
            return False
        
def newMarket(request):
        form = newMarketForm(request.POST)
        if not form.save():
            return False
    