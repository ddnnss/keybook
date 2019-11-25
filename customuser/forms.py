from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class SignUpForm(UserCreationForm):
  #  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('email',  'phone',  'password1', 'password2', 'isOfferRent' )

class UpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'fio',  'phone', 'info', 'hobby','profession','study','avatar' )

        error_messages = {
             'email': {
                 'unique': "Указанный адрес уже кем-то используется",
             },
            'phone': {
                'unique': "Указанный телефон уже кем-то используется",
            },

        }
