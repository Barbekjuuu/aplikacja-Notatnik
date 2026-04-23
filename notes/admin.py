from django.contrib import admin
#lekcja 22 - zadanie 8 - dodanie tagów do notatek
from .models import Note, Category, Tag

admin.site.register(Note)
admin.site.register(Category)
admin.site.register(Tag)

# # Rejestracja modeli w panelu admina
# admin.site.register(Note)
# admin.site.register(Category) 

# Register your models here.
