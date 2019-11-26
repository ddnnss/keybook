from django.forms import ModelForm
from .models import *

class HouseForm(ModelForm):
     class Meta:
         model = House
         fields = ['category', 'client', 'name', 'town','address','short_description','image','price','info']