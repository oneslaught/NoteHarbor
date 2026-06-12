from django.shortcuts import render, get_object_or_404
from .models import Note

# Create your views here.

def home_view(request):
    notes = Note.objects.all().order_by('-created_at')[:6]
    return render(request, 'notes/home.html', {'notes': notes})

def note_detail_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})