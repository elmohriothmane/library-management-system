from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Librairie, Livre, Emprunt
from .forms import SignUpForm, LivreForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


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
    desc_msg = ""
    success_msg = ""
    msg_class = ""
    if request.user.is_authenticated:
        current_user = request.user
        existing_emprunt = Emprunt.objects.filter(livre=livre, user=current_user)
        emprunt = None
        if existing_emprunt:
            emprunt = existing_emprunt[0]
            if emprunt.user == current_user:
                success_msg = 'Vous empruntez actuellement ce livre.'
                desc_msg = 'Vous avez jusqu\'au ' + emprunt.date_limite.strftime(
                    '%d/%m/%Y à %H:%m') + ' pour le rendre. Si vous dépassez cette date, vous aurez des pénalités.'
                msg_class = 'info'
    else:
        emprunt = None

    data = {
        'livre': livre,
        'emprunt': emprunt,
        'desc_msg': desc_msg,
        'success_msg': success_msg,
        'msg_class': msg_class,
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


def emprunter_livre(request, livre_id):
    current_user = request.user
    livre = Livre.objects.get(pk=livre_id)
    livre.set_is_disponible(False)
    livre.save()

    existing_emprunt = Emprunt.objects.filter(livre=livre)
    if not existing_emprunt:
        emprunt = Emprunt()
        emprunt.user = current_user
        emprunt.livre = livre
        emprunt.date_limite = datetime.now() + relativedelta(months=+1)
        emprunt.save()

        success_msg = 'Vous avez bien emprunté le livre "' + livre.nom + '".'
        desc_msg = 'Vous avez 1 mois avant de devoir le rendre à la librairie "' + livre.librairie.label + '".'
        msg_class = 'success'
    else:
        emprunt = existing_emprunt[0]

        if emprunt.user != current_user:
            success_msg = 'Impossible d\'emprunter ce livre.'
            desc_msg = 'Ce livre est déjà emprunté par un autre client.'
            msg_class = 'error'
        else:
            success_msg = 'Vous avez déjà emprunté ce livre.'
            desc_msg = 'Vous avez jusqu\'au ' + emprunt.date_limite.strftime(
                '%d/%m/%Y à %H:%m') + ' pour le rendre. Si vous dépassez cette date, vous aurez des pénalités.'
            msg_class = 'success'

    data = {
        'livre': livre,
        'success_msg': success_msg,
        'desc_msg': desc_msg,
        'emprunt': emprunt,
        'msg_class': msg_class,
    }
    return render(request, 'library/show_livre.html', data)


def rendre_livre(request, livre_id):
    current_user = request.user
    livre = Livre.objects.get(pk=livre_id)
    livre.set_is_disponible(True)
    livre.save()

    existing_emprunt = Emprunt.objects.filter(livre=livre, user=current_user)
    if existing_emprunt:
        emprunt = existing_emprunt[0]
        emprunt.delete()

        success_msg = 'Vous avez bien rendu le livre "' + livre.nom + '".'
        desc_msg = 'Merci de votre confiance.'
        msg_class = 'success'
    else:
        success_msg = 'Vous n\'avez pas emprunté ce livre.'
        desc_msg = 'Vous ne pouvez pas le rendre.'
        msg_class = 'error'

    data = {
        'livre': livre,
        'success_msg': success_msg,
        'desc_msg': desc_msg,
        'emprunt': None,
        'msg_class': msg_class,
    }
    return render(request, 'library/show_livre.html', data)


def new_livre(request, library_id):
    if request.user.is_authenticated:
        if request.user.role == "libraire":
            if request.method == 'POST':
                form = LivreForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/libraries/" + str(library_id) + "/livres")
            else:
                form = LivreForm()
            return render(request, 'livre/new_livre.html', {'form': form})
        else:
            return HttpResponseRedirect("/libraries/" + str(library_id) + "/livres")

    return HttpResponseRedirect("/libraries/" + str(library_id) + "/livres")


def edit_livre(request, livre_id):
    if request.user.is_authenticated:
        if request.user.role == "libraire":
            livre = Livre.objects.get(pk=livre_id)
            if request.method == 'POST':
                form = LivreForm(request.POST, instance=livre)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/libraries/" + str(livre.librairie.id) + "/livres")
            else:
                form = LivreForm(instance=livre)
            return render(request, 'livre/new_livre.html', {'form': form})
        else:
            return redirect('index_libraries')

    return redirect('index_libraries')


def delete_livre(request, livre_id):
    if request.user.is_authenticated and request.user.role == "libraire":
        livre = Livre.objects.get(pk=livre_id)
        livre.delete()
        return HttpResponseRedirect("/libraries/" + str(livre.librairie.id) + "/livres")

    return redirect('index_libraries')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            password1 = request.POST.get('password1')
            print(password1)
    else:
        form = SignUpForm()
    return render(request, 'library/registration.html', {'form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index_libraries')
            else:
                messages.info(request, "User dosn't exist")
                return render(request, "library/login.html", {"form": form})
        else:
            messages.info(request, "username or password is incorrect")
            return render(request, "library/login.html", {"form": form})
    form = AuthenticationForm()

    return render(request, "library/login.html", {"form": form})


def logout_request(request):
    logout(request)
    return redirect('index_libraries')
