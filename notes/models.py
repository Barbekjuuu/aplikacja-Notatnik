from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Notatka"
        verbose_name_plural = "Notatki"
        ordering = ['-created_at']