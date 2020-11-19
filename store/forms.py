from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class checkoutForm(forms.Form):

    country = CountryField().formfield(widget=CountrySelectWidget())
    address = forms.CharField()
    rest_address = forms.CharField(required=False)
    city = forms.CharField()
    state = forms.CharField()
    postal_code = forms.CharField()
    