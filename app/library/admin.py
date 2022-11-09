from django.contrib import admin

from .models import Librairie
from .models import Livre

# Register your models here.
admin.site.register(Librairie)
admin.site.register(Livre)

