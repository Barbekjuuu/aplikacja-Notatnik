from django.urls import path
from . import views
from django.contrib.auth import views as auth_views #zadanie 8 - lekcja 24 - importujemy widoki logowania i wylogowania z django-allauth

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.note_list, name='note_list'),
    path('notes/new/', views.note_create, name='note_create'),
    #zakomentowane na potrzeby lekcji 22 - zadanie 10 - ponieważ będziemy korzystać z widoków rejestracji/logowania z allauth
    # path('register/', views.register_view, name='register'), #dodajemy url dla rejestracji
    # path('login/', views.login_view, name='login'),#dodajemy url dla logowania
    # path('logout/', views.logout_view, name='logout'),          #dodajemy url dla wylogowania
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    # zadanie 2 - dodanie widoku do filtrowania notatek po kategorii - lekcja 22
    path('category/<int:category_id>/', views.notes_by_category, name='notes_by_category'),
    # zadanie 3 - dodanie widoku profilu użytkownika - lekcja 24
    path('profile/', views.profile, name='profile'),
    path('register/', views.register_view, name='register'), #lekcja 24 - zadanie 6 - dodajemy url dla rejestracji
    path('login/', views.login_view, name='login'),#lekcja 24 - zadanie 6 - dodajemy url dla logowania
    path('logout/', views.logout_view, name='logout'),          #lekcja 24 - zadanie 6 - dodajemy url dla wylogowania
    # ====================== LEKCJA 24 - ZADANIE 8 ======================
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='notes/password_change_form.html'
         ), 
         name='password_change'),
    
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='notes/password_change_done.html'
         ), 
         name='password_change_done'),

    # ====================== LEKCJA 24 - ZADANIE 10 ======================
    path('users/', views.user_list, name='user_list'),
]