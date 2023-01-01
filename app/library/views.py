from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import Librairie, Livre, Emprunt,Utilisateur, Message, Groupe, Utilisateur
from .forms import SignUpForm, LivreForm, MessageForm, GroupeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.db.models import Q


# Create your views here.

def index(request):
    if request.user.is_authenticated and request.user.role == "client":
        query = request.GET.get('search-input')
        livres_list= Livre.objects.all()
        groupes_list = Groupe.objects.all()
        emprunts_list = Emprunt.objects.filter(user=request.user)
        data = {
            "emprunts_list": emprunts_list,
            'groupes_list': groupes_list,
            'livres_list': livres_list,
        }
        return render(request, 'index.html', data)

    return render(request, 'index.html')

def search(request):
    search_by = request.GET.get('search_by')
    search_query = request.GET.get('search-query')
    livres_list = []
    if search_by == 'nom':
        # Perform search by Livre nom or auteur
        livres_list = Livre.objects.filter(Q(nom__icontains=search_query) | Q(auteur__icontains=search_query)| Q(genre__icontains=search_query))
    elif search_by == 'adresse':
        # Perform search by ville, code postal, or adresse
        librairies = Librairie.objects.filter(Q(ville__icontains=search_query) | Q(code_postal__icontains=search_query) | Q(adresse__icontains=search_query))
        livres_list = Livre.objects.filter(librairie__in=librairies)


    print(livres_list)
    context = {'livres_list': livres_list}

    return render(request,'index.html',context)


def all_libraries(request):
    librairies_list = Librairie.objects.all()
    output = ', '.join([q.label for q in librairies_list])
    data = {
        'librairies_list': librairies_list
    }
    return render(request, 'library/index.html', data)


def detail_livre(request, livre_id):
    livre = Livre.objects.get(pk=livre_id)
    messages = Message.objects.filter(livre=livre_id)
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
        'commentaires': messages,
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
                form = LivreForm(request.POST,request.FILES)
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
            return redirect('all_libraries')

    return redirect('all_libraries')


def delete_livre(request, livre_id):
    if request.user.is_authenticated and request.user.role == "libraire":
        livre = Livre.objects.get(pk=livre_id)
        livre.delete()
        return HttpResponseRedirect("/libraries/" + str(livre.librairie.id) + "/livres")

    return redirect('all_libraries')


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
                return redirect('all_libraries')
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
    return redirect('all_libraries')


def all_emprunts(request):
    if request.user.is_authenticated and request.user.role == "libraire":
        emprunts_list = Emprunt.objects.all()
        data = {
            'emprunts_list': emprunts_list,
            'now': datetime.now(),
        }
        return render(request, 'emprunt/index_emprunts.html', data)
    return redirect('index')


def profile(request,username):
    user = Utilisateur.objects.get(username=username)
    data = {
            'user': user,
        }
    return render(request, 'library/profile.html',data)

def new_message(request, livre_id):
    if request.user.is_authenticated:
        livre = Livre.objects.get(pk=livre_id)
        user = request.user
        now = datetime.now()

        message = Message()
        message.contenu = request.POST.get('content-msg')
        message.date = now
        message.user = user
        message.livre = livre
        message.save()

    return HttpResponseRedirect("/livres/" + str(livre_id) + "/")


def all_groupes(request):
    groupes_list = Groupe.objects.all()
    data = {
        'groupes_list': groupes_list,
    }
    return render(request, 'groupe/index_groupes.html', data)


def new_message_groupe(request, groupe_id):
    if request.user.is_authenticated:
        groupe = Groupe.objects.get(pk=groupe_id)
        user = request.user
        now = datetime.now()

        message = Message()
        message.contenu = request.POST.get('content-msg')
        message.date = now
        message.user = user
        message.groupe = groupe
        message.save()

    return HttpResponseRedirect("/lectures/" + str(groupe_id) + "/")


def detail_groupe(request, groupe_id):
    groupe = Groupe.objects.get(pk=groupe_id)
    messages = Message.objects.filter(groupe=groupe_id)
    data = {
        'groupe': groupe,
        'total_users': groupe.users.count(";") - 1,
        "commentaires": messages,
    }

    if request.user.is_authenticated:
        user = request.user
        data = {
            'groupe': groupe,
            'user_search': ";" + str(user.id) + ";",
            'total_users': groupe.users.count(";") - 1,
            "commentaires": messages,
        }

    return render(request, 'groupe/show_groupe.html', data)


def new_groupe(request):
    if request.user.is_authenticated and request.user.role == "libraire":
        if request.method == 'POST':
            form = GroupeForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/lectures/")
        else:
            form = GroupeForm()
        return render(request, 'groupe/new_groupe.html', {'form': form})
    return HttpResponseRedirect("/lectures/")


def edit_groupe(request, groupe_id):
    groupe = Groupe.objects.get(pk=groupe_id)
    if request.user.is_authenticated and request.user.role == "libraire":
        if request.method == 'POST':
            form = GroupeForm(request.POST, instance=groupe)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/lectures/" + str(groupe.id) + "")
        else:
            form = GroupeForm(instance=groupe)
        return render(request, 'groupe/new_groupe.html', {'form': form})
    return HttpResponseRedirect("/lectures/" + str(groupe.id) + "")


def inscription_groupe(request, groupe_id):
    groupe = Groupe.objects.get(pk=groupe_id)
    if request.user.is_authenticated:
        user = request.user
        print("####################################")
        print(request.method)
        print("####################################")
        print(user.id)
        groupe.users += str(user.id) + ";"
        groupe.save()
        return HttpResponseRedirect("/lectures/" + str(groupe.id) + "")



@login_required
def edit_comment(request, message_id):
    comment = get_object_or_404(Message, pk=message_id)
    book_id = comment.livre.id
    if request.method == 'POST':
        comment.contenu = request.POST['content-msg']
        comment.save()
        print(comment)
        return HttpResponseRedirect("/livres/" + str(book_id) + "/")
        
    return HttpResponseRedirect("/livres/" + str(book_id) + "/")

def delete_comment(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    book_id = message.livre.id
    if request.method == 'POST':
        message.delete()
        return HttpResponseRedirect("/livres/" + str(book_id) + "/")

    return  HttpResponseRedirect("/livres/" + str(book_id) + "/")
