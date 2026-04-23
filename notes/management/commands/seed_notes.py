import random
from django.core.management.base import BaseCommand
from faker import Faker
from notes.models import Note, Category, Tag          # ← DODANO: Tag
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seeduje bazę danymi testowymi (kategorie + 100 notatek + tagi)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Czyszczenie bazy...')
        
        # a. Usuń wszystkie notatki i kategorie
        Note.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()                     # ← DODANO (Zadanie 9)
        
        self.stdout.write(self.style.SUCCESS('✓ Baza wyczyszczona'))

        fake = Faker('pl_PL')

        # b. Stwórz predefiniowane kategorie
        category_names = [
            "Praca", "Osobiste", "Pomysły", "Zakupy", 
            "Podróże", "Zdrowie", "Finanse", "Inne"
        ]
        
        categories = []
        for name in category_names:
            cat = Category.objects.create(name=name)
            categories.append(cat)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Utworzono {len(categories)} kategorii'))

        # ====================== lekcja 22 - zadanie 9 - POCZĄTEK ROZBUDOWY ======================
        # c. Stwórz tagi (nowość w Zadaniu 9)
        tag_names = [
            "ważne", "pilne", "pomysł", "do zrobienia", "spotkanie",
            "finanse", "zdrowie", "praca", "osobiste", "inspiracja"
        ]
        tags = []
        for name in tag_names:
            tag = Tag.objects.create(name=name)
            tags.append(tag)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Utworzono {len(tags)} tagów'))
        # ====================== lekcja 22 - zadanie 9 - KONIEC ROZBUDOWY ======================

        # d. Stwórz 100 losowych notatek
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING('Brak użytkowników!'))
            return

        for i in range(100):
            note = Note.objects.create(
                title=fake.sentence(nb_words=6),
                content=' '.join(fake.paragraphs(nb=3)),
                author=random.choice(users),
                category=random.choice(categories)
            )
            
            # ====================== lekcja 22 - zadanie 9 - POCZĄTEK ROZBUDOWY ======================
            # Losowo przypisz od 1 do 5 tagów do każdej notatki
            random_tags = random.sample(tags, random.randint(1, 5))
            note.tags.set(random_tags)
            # ====================== lekcja 22 - zadanie 9 - KONIEC ROZBUDOWY ======================
        
        self.stdout.write(self.style.SUCCESS('✓ Utworzono 100 notatek z tagami'))
        self.stdout.write(self.style.SUCCESS('🎉 Seedowanie zakończone!'))