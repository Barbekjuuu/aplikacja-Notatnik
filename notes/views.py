from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q # do wyszukiwania notatek po tytule i treści - lekcja 22 - zadanie 6
#zadanie 5 - lekcja 24 - dodajemy dekorator login_required do widoku profilu, aby był dostępny tylko dla zalogowanych użytkowników
from django.contrib.auth.decorators import login_required # lekcja 24 - zadanie 3 - strona profilu dostępna tylko dla zalogowanych użytkowników
from .models import Note
from .forms import NoteForm
from .forms import CustomUserCreationForm # lekcja 24 - zadanie 6 - własny formularz rejestracji z dodatkowym polem email
#zadanie 10 - lekcja 24 - tylko dla pracowników - dekorator staff_member_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

# ====================== STRONA GŁÓWNA ======================
# Pokazuje 5 najnowszych notatek - lekcja 22 -zadanie 3
@login_required #lekcja 24 - zadanie 5 - strona główna dostępna tylko dla zalogowanych użytkowników
def home(request):
    """Strona główna - pokazuje 5 najnowszych notatek"""
    
    latest_notes = Note.objects.all().order_by('-created_at')[:5]
    
    return render(request, 'home.html', {'latest_notes': latest_notes})


# ====================== LISTA NOTATEK (Lekcja 22 - zadanie 6) ======================

def note_list(request):
    """Lista notatek z wyszukiwarką i paginacją"""
    
    query = request.GET.get('q', '')   # pobieramy frazę z paska adresu (?q=coś)
    
    all_notes = Note.objects.all().order_by('-created_at')
    
    if query:
        all_notes = all_notes.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    # Paginacja
    paginator = Paginator(all_notes, 6)
    page_number = request.GET.get('page')
    
    try:
        notes = paginator.page(page_number)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)
    
    return render(request, 'notes/list.html', {
        'notes': notes,
        'query': query   # przekazujemy wyszukiwaną frazę do szablonu
    })

# # ====================== LISTA NOTATEK Z PAGINACJĄ (Lekcja 20 + 22) ======================

# def note_list(request):
#     """Lista notatek z paginacją - maksymalnie 3 notatki na stronę"""
    
#     all_notes = Note.objects.all().order_by('-created_at')
    
#     # Tworzymy paginator: 3 notatki na stronę
#     paginator = Paginator(all_notes, 3)
    
#     # Pobieramy numer strony z adresu URL (np. ?page=2)
#     page_number = request.GET.get('page')
    
#     try:
#         notes = paginator.page(page_number)
#     except PageNotAnInteger:
#         notes = paginator.page(1)           # jeśli ktoś wpisze nie liczbę → pokaż stronę 1
#     except EmptyPage:
#         notes = paginator.page(paginator.num_pages)  # jeśli strona za duża → pokaż ostatnią stronę
    
#     return render(request, 'notes/list.html', {'notes': notes})


# ====================== TWORZENIE I EDYCJA NOTATEK ======================

def note_create(request):
    """Tworzenie nowej notatki"""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            if request.user.is_authenticated:
                note.author = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    
    return render(request, 'notes/create.html', {'form': form})


def note_edit(request, pk):
    """Edycja istniejącej notatki"""
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/create.html', {'form': form, 'note': note})


# ====================== SZCZEGÓŁY I USUWANIE ======================

def note_detail(request, pk):
    """Szczegóły pojedynczej notatki"""
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/detail.html', {'note': note})


def note_delete(request, pk):
    """Kasowanie notatki"""
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    
    return render(request, 'notes/delete.html', {'note': note})


# ====================== AUTENTYKACJA (Lekcja 20) ======================

def register_view(request):
    """Rejestracja nowego użytkownika"""
    if request.method == 'POST':
        # form = UserCreationForm(request.POST) # lekcja 24 - zadanie 6 - zamieniamy domyślny formularz rejestracji na własny, który zawiera dodatkowe pole email
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # lekcja 24 - zadanie 9 - automatyczne logowanie po rejestracji
            return redirect('note_list')
    else:
        # form = UserCreationForm()# lekcja 24 - zadanie 6 - zamieniamy domyślny formularz rejestracji na własny, który zawiera dodatkowe pole email
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Logowanie użytkownika"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('note_list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Wylogowanie użytkownika"""
    logout(request)
    return redirect('home')


# ====================== ZADANIE 2 - LEKCJA 22 ======================
# Widok: notatki z danej kategorii

def notes_by_category(request, category_id):
    """Wyświetla wszystkie notatki należące do wybranej kategorii"""
    notes = Note.objects.filter(category_id=category_id).order_by('-created_at')
    return render(request, 'notes/notes_by_category.html', {'notes': notes})
# ====================== ZADANIE 3 - LEKCJA 24 ======================
@login_required
def profile(request):
    """Strona profilu użytkownika"""
    return render(request, 'notes/profile.html')

    # ====================== LEKCJA 24 - ZADANIE 10 ======================
@staff_member_required
def user_list(request):
    """Lista wszystkich użytkowników (tylko dla staff)"""
    users = User.objects.all().order_by('username')
    return render(request, 'notes/user_list.html', {'users': users})