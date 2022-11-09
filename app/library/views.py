from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Librairie, Livre


# Create your views here.
def index(request):
    # return render(request,"library/index.html.html")

    librairies_list = Librairie.objects.all()
    output = ', '.join([q.label for q in librairies_list])
    data = {
        'librairies_list': librairies_list
    }
    return render(request, 'library/index.html', data)


def detail_livre(request, livre_id):
    livre = Livre.objects.get(pk=livre_id)
    data = {
        'livre': livre,
    }
    return render(request, 'library/show_livre.html', data)


def detail_library(request, library_id):
    library = Librairie.objects.get(pk=library_id)
    data = {
        'library': library,
    }
    return render(request, 'library/show.html', data)


def detail_library_livres(request, library_id):
    library = Librairie.objects.get(pk=library_id)
    livres = library.livres.all()
    data = {
        'livres': livres,
        'library': library,
    }
    return render(request, 'library/livres.html', data)

