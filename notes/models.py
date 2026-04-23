from django.db import models
from django.contrib.auth.models import User

#lekcja 22 - zadanie 1 - dodanie kategorii do notatek
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nazwa kategorii")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

#lekcja 22 - zadanie 8 - dodanie tagów do notatek

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nazwa tagu")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tagi"

class Note(models.Model):
    """Model notatki"""
    
    title = models.CharField(max_length=200, verbose_name="Tytuł notatki")
    content = models.TextField(verbose_name="Treść notatki")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data ostatniej edycji")
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Autor",
        null=True,
        blank=True
    )

        #lekcja 22 - zadanie 1 - dodanie kategorii do notatek

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kategoria"
    )

#lekcja 22 - zadanie 8 - dodanie tagów do notatek

    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        verbose_name="Tagi"
    )
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Notatka"
        verbose_name_plural = "Notatki"
        ordering = ['-created_at']

