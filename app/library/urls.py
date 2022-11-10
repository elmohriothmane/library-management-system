from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_libraries'),
    path('login/', views.login_request,name="login"),
    path('signup/', views.signup,name="signup"),
    path('logout/', views.logout_request, name='logout'),
    # ex : /livres/5/
    path('livres/<int:livre_id>/', views.detail_livre, name='detail_livre'),
    # ex : /libraries/5/
    path('libraries/<int:library_id>/', views.detail_library, name='detail_library'),
    path('libraries/<int:library_id>/livres/', views.detail_library_livres, name='detail_library_livres'),
    path('livres/<int:livre_id>/emprunter', views.emprunter_livre, name='emprunter_livre'),
    path('livres/<int:livre_id>/rendre', views.rendre_livre, name='rendre_livre'),
]
