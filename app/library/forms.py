from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

ROLE = (
        ('libraire', 'ROLE_LIBRRAIRE'),
        ('client', 'ROLE_CLIENT')
    )

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=12, min_length=4, required=True,error_messages={
        "required":"First Name is required",
        "max_length":"First Name is required",})
    
    last_name = forms.CharField(max_length=12, min_length=4, required=True,error_messages={
        "required":"Last Name is required",
        "max_length":"Last Name is required",})
    
    username = forms.CharField(max_length=12, min_length=4, required=True,error_messages={
        "required":"User Name is required",
        "max_length":"User Name is required",})

    email = forms.EmailField(required=True,error_messages={
        "required":"Email Name is required",})

    numero_telephone=forms.CharField(max_length=10,required=False,error_messages={
        "required":"Phone Number is required",})

    role =forms.ChoiceField(choices = ROLE, label="", initial='', widget=forms.Select(), required=True)

    class Meta:
        model = Utilisateur
        fields = ('first_name', 'last_name', 'username', 'email','numero_telephone', 'password1', 'password2', 'role')


