from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Note, SavedNote
from .filters import filter_notes, get_filter_context

# Create your views here.

def home_view(request):
    notes = Note.objects.all().order_by('-created_at')
    courses, tags = get_filter_context(notes)
    notes = filter_notes(notes, request)
    return render(request, 'notes/home.html', {
        'notes': notes,
        'courses': courses,
        'tags': tags,
        'current_course': request.GET.get('course'),
        'current_tag': request.GET.get('tag'),
    })


def note_detail_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedNote.objects.filter(user=request.user, note=note).exists()
    return render(request, 'notes/note_detail.html', {'note': note, 'is_saved': is_saved})


@login_required
def toggle_favorite_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    saved = SavedNote.objects.filter(user=request.user, note=note)
    if saved.exists():
        saved.delete()
    else:
        SavedNote.objects.create(user=request.user, note=note)
    return redirect('note_detail', pk=pk)


@login_required
def favorites_view(request):
    all_saved = SavedNote.objects.filter(user=request.user)
    total_notes = all_saved.count()

    notes = Note.objects.filter(saved_by__user=request.user).order_by('-saved_by__saved_at')
    courses, tags = get_filter_context(notes)
    total_courses = courses.count()
    notes = filter_notes(notes, request)

    return render(request, 'notes/favorites.html', {
        'notes': notes,
        'courses': courses,
        'tags': tags,
        'total_notes': total_notes,
        'total_courses': total_courses,
        'current_course': request.GET.get('course'),
        'current_tag': request.GET.get('tag'),
    })