from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

ROLE = (
    ('libraire', 'ROLE_LIBRRAIRE'),
    ('client', 'ROLE_CLIENT'),
    ('admin', 'ROLE_ADMIN'),
)


class Utilisateur(AbstractUser):
    role = models.CharField(choices=ROLE, default='client', max_length=10)
    numero_telephone = models.CharField(max_length=10)

    # add additional fields in here

    def __str__(self):
        return self.username


class Librairie(models.Model):
    label = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    code_postal = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    telephone = models.BigIntegerField()

    def __str__(self):
        return self.label

    def get_ville(self):
        return self.ville

    def get_code_postal(self):
        return self.code_postal

    def get_adresse(self):
        return self.adresse


class Livre(models.Model):
    nom = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    jaquette = models.CharField(max_length=200, default='')
    editeur = models.CharField(max_length=200, default='')
    collection = models.CharField(max_length=200, default='')
    genre = models.CharField(max_length=200, default='')
    is_disponible = models.BooleanField(default=True)
    librairie = models.ForeignKey(Librairie, on_delete=models.CASCADE, related_name='livres')

    def __str__(self):
        return self.nom

    def get_nom(self):
        return self.nom

    def get_auteur(self):
        return self.Auteur

    def get_is_disponible(self):
        return self.is_disponible

    def set_is_disponible(self, is_disponible):
        self.is_disponible = is_disponible

    def get_jaquette(self):
        return self.jaquette

    def get_editeur(self):
        return self.editeur

    def get_collection(self):
        return self.collection

    def get_genre(self):
        return self.genre

    def get_librairie(self):
        return self.librairie


class Emprunt(models.Model):
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_limite = models.DateTimeField(auto_now_add=False, null=True)
    date_retour = models.DateTimeField(auto_now_add=False, null=True)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='livre_emprunte')
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='emprunts',
                             related_query_name="user_emprunte")

    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emprunts')

    def __str__(self):
        return self.livre.nom

    def get_date_emprunt(self):
        return self.date_emprunt

    def get_date_retour(self):
        return self.date_retour

    def get_livre(self):
        return self.livre


class Message(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='messages')
    # groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='messages')
    date = models.DateTimeField(auto_now_add=True)
    contenu = models.TextField()

    def __str__(self):
        return self.contenu

    def get_date(self):
        return self.date

    def get_user(self):
        return self.user

    def get_livre(self):
        return self.livre
