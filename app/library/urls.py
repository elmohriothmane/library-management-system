from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_request,name="login"),
    path('signup/', views.signup,name="signup"),
    path('logout/', views.logout_request, name='logout'),

    path('libraries/', views.all_libraries, name='all_libraries'),
    path('libraries/<int:library_id>/', views.detail_library, name='detail_library'),
    path('libraries/<int:library_id>/livres/', views.detail_library_livres, name='detail_library_livres'),

    path('livres/<int:livre_id>/', views.detail_livre, name='detail_livre'),
    path('livres/<int:livre_id>/emprunter', views.emprunter_livre, name='emprunter_livre'),
    path('livres/<int:livre_id>/rendre', views.rendre_livre, name='rendre_livre'),
    path('library/<int:library_id>/livres/new', views.new_livre, name='new_livre'),
    path('livres/<int:livre_id>/edit', views.edit_livre, name='edit_livre'),
    path('livres/<int:livre_id>/delete', views.delete_livre, name='delete_livre'),

    path('emprunts/', views.all_emprunts, name='all_emprunts'),
    path('profile/<str:username>', views.profile, name='profile'),
]
