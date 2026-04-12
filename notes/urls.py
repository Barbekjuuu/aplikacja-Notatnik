from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.note_list, name='note_list'),
    path('notes/new/', views.note_create, name='note_create'),
    path('register/', views.register_view, name='register'), #dodajemy url dla rejestracji
    path('login/', views.login_view, name='login'),#dodajemy url dla logowania
    path('logout/', views.logout_view, name='logout'),          #dodajemy url dla wylogowania
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
]