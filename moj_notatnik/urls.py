from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes.urls')),   # wszystkie ścieżki z aplikacji notes
    path('accounts/', include('allauth.urls')),   # ← lekcja 22 - zadanie 10 - dodajemy: ścieżki do logowania/rejestracji z allauth
]