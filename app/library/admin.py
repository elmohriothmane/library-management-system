from django.contrib import admin

from .models import Librairie, Message, Groupe
from .models import Livre
from .models import Utilisateur
from .models import Emprunt

# Register your models here.
admin.site.register(Librairie)
admin.site.register(Livre)
admin.site.register(Utilisateur)
admin.site.register(Emprunt)
admin.site.register(Message)
admin.site.register(Groupe)

