from django.shortcuts import render
from .models import Note

# Create your views here.

def home_view(request):
    notes = Note.objects.all().order_by('-created_at')[:6]
    return render(request, 'notes/home.html', {'notes': notes})