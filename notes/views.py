from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import Note
from .forms import NoteForm   # utworzymy ten formularz w następnym kroku
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger#zadanie 10 - importujemy narzędzia do paginacji

def home(request):
    """Strona powitalna"""
    return render(request, 'home.html')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def note_list(request):
    """Lista notatek z paginacją - maksymalnie 3 notatki na stronę"""
    
    all_notes = Note.objects.all().order_by('-created_at')
    
    # Tworzymy paginator: 3 notatki na stronę
    paginator = Paginator(all_notes, 3)
    
    # Pobieramy numer strony z adresu URL (np. ?page=2)
    page_number = request.GET.get('page')
    
    try:
        notes = paginator.page(page_number)
    except PageNotAnInteger:
        notes = paginator.page(1)           # jeśli ktoś wpisze nie liczbę → pokaż stronę 1
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)  # jeśli strona za duża → pokaż ostatnią
    
    return render(request, 'notes/list.html', {'notes': notes})

def note_create(request):
    """Tworzenie nowej notatki"""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)      # przygotuj obiekt, ale nie zapisuj jeszcze
            
            # Jeśli użytkownik jest zalogowany, przypisz autora
            if request.user.is_authenticated:
                note.author = request.user
            # Jeśli nie jest zalogowany, pole author zostanie puste (null)
            
            note.save()                         # zapisz notatkę
            return redirect('note_list')
    else:
        form = NoteForm()
    
    return render(request, 'notes/create.html', {'form': form})

    # ====================== AUTENTYKACJA ======================

def register_view(request):
    """Rejestracja nowego użytkownika"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)           # automatycznie logujemy użytkownika po rejestracji
            return redirect('note_list')
    else:
        form = UserCreationForm()
    
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

# =========================================================
def note_delete(request, pk):
    """Kasowanie notatki"""
    note = get_object_or_404(Note, pk=pk)   # znajdź notatkę po id lub pokaż 404
    
    if request.method == 'POST':
        note.delete()                       # usuń notatkę z bazy
        return redirect('note_list')
    
    return render(request, 'notes/delete.html', {'note': note})


def note_edit(request, pk):
    """Edycja istniejącej notatki"""
    note = get_object_or_404(Note, pk=pk)   # pobierz notatkę po id

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)   # wypełnij formularz danymi z notatki
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)                 # wypełnij formularz danymi z istniejącej notatki

    return render(request, 'notes/create.html', {'form': form, 'note': note})

def note_detail(request, pk):
    """Szczegóły pojedynczej notatki - widok szczegółów"""
    note = get_object_or_404(Note, pk=pk)   # pobiera notatkę po id lub pokazuje 404 jeśli nie istnieje
    
    context = {
        'note': note,
    }
    
    return render(request, 'notes/detail.html', context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

