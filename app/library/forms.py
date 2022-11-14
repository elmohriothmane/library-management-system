from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Utilisateur, Livre, Librairie, Message

ROLE = (
    ('libraire', 'ROLE_LIBRRAIRE'),
    ('client', 'ROLE_CLIENT')
)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=12, min_length=4, required=True, error_messages={
        "required": "First Name is required",
        "max_length": "First Name is required", })

    last_name = forms.CharField(max_length=12, min_length=4, required=True, error_messages={
        "required": "Last Name is required",
        "max_length": "Last Name is required", })

    username = forms.CharField(max_length=12, min_length=4, required=True, error_messages={
        "required": "User Name is required",
        "max_length": "User Name is required", })

    email = forms.EmailField(required=True, error_messages={
        "required": "Email Name is required", })

    numero_telephone = forms.CharField(max_length=10, required=False, error_messages={
        "required": "Phone Number is required", })

    role = forms.ChoiceField(choices=ROLE, label="", initial='', widget=forms.Select(), required=True)

    class Meta:
        model = Utilisateur
        fields = ('first_name', 'last_name', 'username', 'email', 'numero_telephone', 'password1', 'password2', 'role')


class LivreForm(ModelForm):
    nom = forms.CharField(max_length=200, required=True, error_messages={
        "required": "Title is required",
        "max_length": "Title is required", })

    auteur = forms.CharField(max_length=50, required=True, error_messages={
        "required": "Author is required",
        "max_length": "Author is required", })

    jaquette = forms.CharField(max_length=100, required=True, error_messages={
        "required": "Description is required",
        "max_length": "Description is required", })

    editeur = forms.CharField(max_length=100, required=True, error_messages={
        "required": "Editor is required",
        "max_length": "Editor is required", })

    collection = forms.CharField(max_length=100, required=True, error_messages={
        "required": "Collection is required",
        "max_length": "Collection is required", })

    genre = forms.CharField(max_length=100, required=True, error_messages={
        "required": "Genre is required",
        "max_length": "Genre is required", })

    is_disponible = forms.BooleanField(required=False)

    librairie = forms.ModelChoiceField(queryset=Librairie.objects.all(), required=True, error_messages={
        "required": "Library is required", })

    class Meta:
        model = Livre
        fields = ('nom', 'auteur', 'jaquette', 'editeur', 'collection', 'genre', 'is_disponible', 'librairie')


class MessageForm(ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=True, error_messages={
        "required": "Message is required", })

    class Meta:
        model = Message
        fields = ('content',)
