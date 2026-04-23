import random
from django.core.management.base import BaseCommand
from faker import Faker
from notes.models import Note   # ← dostosowane do Twojej aplikacji

class Command(BaseCommand):
    help = 'Wypełnia bazę danymi testowymi (notatki)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Rozpoczynam seedowanie bazy...')

        fake = Faker('pl_PL')

        # Tworzymy 30 przykładowych notatek
        for _ in range(30):
            Note.objects.create(
                title=fake.sentence(nb_words=5),
                content=' '.join(fake.paragraphs(nb=3)),
                # Jeśli masz pole author lub user – odkomentuj i dopasuj:
                # author=random.choice(User.objects.all()),
            )

        self.stdout.write(self.style.SUCCESS('✓ Utworzono 30 notatek'))
        self.stdout.write(self.style.SUCCESS('🎉 Seedowanie zakończone pomyślnie!'))