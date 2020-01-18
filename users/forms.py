from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length = 20, widget = forms.TextInput(attrs ={ 'class':'form-control', 'placeholder':'username'}
    ))
    first_name = forms.CharField(max_length = 20,  widget = forms.TextInput(attrs ={ 'class':'form-control', 'placeholder':'First Name'}
    ))
    last_name = forms.CharField(max_length = 20, widget = forms.TextInput(attrs ={ 'class':'form-control', 'placeholder':'Last Name'}
    ) )
    email = forms.CharField(max_length = 50, widget = forms.TextInput(attrs ={ 'class':'form-control', 'placeholder': 'some@email.address'}
    ))
    password1 = forms.CharField(widget = forms.TextInput(attrs ={ 'class':'form-control', 'placeholder': 'password', 'type': 'password'}
    ))
    password2 = forms.CharField(widget = forms.TextInput(attrs ={ 'class':'form-control', 'placeholder': 'repeat password', 'type':'password'}
    ))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name', 'password1','password2']


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'phone', 'birth_date', 'address', 'street_address', 'bio']

class UserUpdate(forms.ModelForm):
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    email = forms.CharField(max_length = 50)
    class Meta:
        model = User
        fields= ['username','first_name', 'last_name', 'email']