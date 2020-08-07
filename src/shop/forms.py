from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseRegistrationForm
from django.contrib.auth import get_user_model

from .models import Order


User = get_user_model()


class AddToCartForm(forms.Form):
    """Form to add product to cart."""
    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )
    quantity = forms.IntegerField(
        widget=forms.HiddenInput(),
    )


class OrderForm(forms.ModelForm):
    """For for create order from cart."""
    class Meta:
        model = Order
        fields = (
            'first_name',
            'patronymic_name',
            'last_name',
            'address',
            'phone',
            'email',
        )


class RegistrationForm(BaseRegistrationForm):
    """Form for user registrations."""
    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
        )


class ProfileEditForm(forms.ModelForm):
    """Form for user registrations."""
    class Meta:
        model = User
        fields = (
            'first_name',
            'patronymic_name',
            'last_name',
            'address',
            'phone',
            'email',
        )
