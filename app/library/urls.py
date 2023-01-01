from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_request,name="login"),
    path('signup/', views.signup,name="signup"),
    path('logout/', views.logout_request, name='logout'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('search/',views.search),
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

    path('livres/<int:livre_id>/nouveau-commentaire', views.new_message, name='new_message'),
    path('livres/<int:message_id>/edit-commentaire', views.edit_comment, name='edit_comment'),
    path('livres/<int:message_id>/delete-commentaire', views.delete_comment, name='delete_comment'),
    path('lectures/<int:groupe_id>/nouveau-commentaire', views.new_message_groupe, name='new_message_groupe'),

    path('lectures/', views.all_groupes, name='all_groupes'),
    path('lectures/<int:groupe_id>/', views.detail_groupe, name='detail_groupe'),
    path('lectures/new', views.new_groupe, name='new_groupe'),
    path('lectures/<int:groupe_id>/edit', views.edit_groupe, name='edit_groupe'),
    path('lectures/<int:groupe_id>/inscription', views.inscription_groupe, name='inscription_groupe'),
]
