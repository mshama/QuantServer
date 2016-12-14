'''
Created on 30.11.2016

@author: Moustafa Shama
'''

from django.utils.translation import ugettext_lazy as _

from django import forms

from PortfolioPositionManagement.models import Mandate, Position


class newMandateForm(forms.ModelForm):
    class Meta:
        model = Mandate
        fields = ('name_c',)
        labels = {
            'name_c': _('Name:'),
        }
        widgets = {
            'name_c': forms.TextInput(attrs={ 'required': 'true' }),
        }
        
class positionForm(forms.ModelForm):
    
    class Meta:
        model = Position
        
        fields = ('status', 'quantity_n', 'price_cost_n', 'price_valuation_kvg_n', 'currency',)