from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('esewa', 'eSewa'),
    ('stripe', 'Debit/Credit Card')
)

class CheckOutForm(forms.Form):
    country = CountryField(blank_label="Select a country.").formfield(required=False,
                                            widget=CountrySelectWidget(attrs={
                                            'class': 'form-control'
                                            }))
    street_address = forms.CharField(widget=forms.TextInput(attrs = {'type':"text",
                        "class":"form-control",
                        'placeholder':"House number and street name"
                        }))
    appartment_address = forms.CharField(widget=forms.TextInput(attrs = {'type':"text",
                        "class":"form-control",
                        'placeholder':"Appartment or suite"
                        }))
    town = forms.CharField(widget=forms.TextInput(attrs = {'type':"text",
                        "class":"form-control",
                        'placeholder':"City/Town"
                        }))
    zip_code = forms.CharField(widget=forms.TextInput(attrs = {'type':"text",
                        "class":"form-control",
                        'placeholder':"ZIP/Postal Code"
                        }))
    save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    ship_to_different_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
    

    def __init__(self, *args, **kwargs):
        super(CheckOutForm, self).__init__(*args, **kwargs)

        self.fields['save_info'].widget.attrs['type'] = 'checkbox'
        self.fields['payment_option'].widget.attrs['type'] = 'radio'
       
class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.TextInput())

class Query(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs = {'type':"text",
                        "class":"form-group",
                        'placeholder':"Search products",
                        'aria-label':"search"
                        }))  