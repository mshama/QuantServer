'''
Created on 15.09.2016

@author: Moustafa Shama
'''
from django.utils.translation import ugettext_lazy as _

from django import forms

from .models import Marketdatatype, Market, Currency, Instrument, Codification, Country

class newMarketDataTypeForm(forms.ModelForm):
    class Meta:
        model = Marketdatatype
        fields = ('name_c', 'type_c')
        widgets = {
            'type_c': forms.Select(choices = ([('Stock','Stock'), ('Bond','Bond'),('Derivative','Derivative'), ('InterestRate','InterestRate'), ]))
        }
        labels = {
            'name_c': _('Name:'),
            'type_c': _('Choose type:')
        }
        
class newMarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ('iso_code_c', 'name_c', 'denomination_c')
        labels = {
            'iso_code_c': _('ISO Code:'),
            'name_c': _('Name:'),
            'denomination_c': _('Denomination:'),
        }
        
class codificationForm(forms.Form):
    codification = forms.ModelChoiceField(label='Code type:', queryset=Codification.objects.all())
    code = forms.CharField(label='Code:')
    
class newCodificationForm(forms.ModelForm):
    class Meta:
        model = Codification
        fields = ('name_c', 'denomination_c')
        labels = {
            'name_c': _('Name:'),
            'denomination_c': _('Denomination:'),
        }

class newCurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ('isocode_c', 'name_c', 'denomination_c')
        labels = {
            'isocode_c': _('ISO Code:'),
            'name_c': _('Name:'),
            'denomination_c': _('Denomination:'),
        }

class newInstrumentForm(forms.Form):
    codification = forms.ModelChoiceField(label='Code type:', queryset=Codification.objects.all())
    market = forms.ModelChoiceField(label='Market:', queryset=Market.objects.all())
    marketdatatype = forms.ModelChoiceField(label='Market Data Type:', queryset=Marketdatatype.objects.all())
    currency = forms.ModelChoiceField(label='Currency:', queryset=Currency.objects.all())
    undercurrency = forms.ModelChoiceField(label='Currency:', queryset=Currency.objects.all())
    country = forms.ModelChoiceField(label='Country:', queryset=Country.objects.all())
    names = forms.CharField(label='Instruments:', widget=forms.Textarea)