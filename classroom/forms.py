from django.forms.utils import ValidationError
from classroom.models import User, Customer
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer,User, Vehicle, ParkingLocation
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth import get_user_model
from django.core.signals import setting_changed
from django.dispatch import receiver
from .models import Payment
from .models import VehicleLocation




class CustomerForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['last_name'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['car_model'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['car_color'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['cost_per_day'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['phone_number'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['comment'].widget.attrs = {
            'class': 'form-control col-md-6'
        } 
        self.fields['is_payed'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['payment_method'].widget.attrs = {
            'class': 'form-contol col-md-6'
        }
        self.fields['payment_date'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'car_model', 'car_color', 'cost_per_day', 'phone_number', 'comment', 'is_payed','payment_method','payment_date')




class UserForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['last_name'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['email'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['password'].widget.attrs = {
            'class': 'form-control col-md-6'
        }


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'parked_at']

    parked_at = forms.ModelChoiceField(
        queryset=ParkingLocation.objects.filter(is_occupied=False),
        label="Parking Location",
        required=True,
    )

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [ 'payment_method']


class VehicleLocationForm(forms.ModelForm):
    class Meta:
        model = VehicleLocation
        fields = ['license_plate', 'latitude', 'longitude']