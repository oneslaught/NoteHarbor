from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Note, SavedNote
from .filters import filter_notes, get_filter_context


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
    can_fork = False
    if request.user.is_authenticated:
        is_saved = SavedNote.objects.filter(user=request.user, note=note).exists()
        root_note = note.original_note if note.is_fork else note
        can_fork = (
            root_note.author != request.user and
            not Note.objects.filter(author=request.user, original_note=root_note).exists()
        )
    return render(request, 'notes/note_detail.html', {
        'note': note,
        'is_saved': is_saved,
        'can_fork': can_fork,
    })


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


@login_required
def fork_note_view(request, pk):
    original_note = get_object_or_404(Note, pk=pk)
    if original_note.author == request.user:
        return redirect('note_detail', pk=pk)
    root_note = original_note.original_note if original_note.is_fork else original_note
    already_forked = Note.objects.filter(
        author=request.user,
        original_note=root_note
    ).exists()
    if already_forked:
        return redirect('note_detail', pk=pk)
    forked_note = Note.objects.create(
        author=request.user,
        course=root_note.course,
        original_note=root_note,
        title=f'{root_note.title} (fork by {request.user.username})',
        content=root_note.content,
    )
    forked_note.tags.set(root_note.tags.all())
    return redirect('note_detail', pk=forked_note.pk)

@login_required
def my_forks_view(request):
    notes = Note.objects.filter(author=request.user, original_note__isnull=False).order_by('-created_at')
    courses, tags = get_filter_context(notes)
    notes_filtered = filter_notes(notes, request)
    return render(request, 'notes/my_forks.html', {
        'notes': notes_filtered,
        'courses': courses,
        'tags': tags,
        'current_course': request.GET.get('course'),
        'current_tag': request.GET.get('tag'),
    })


@login_required
def delete_note_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.user != note.author and not request.user.profile.is_admin:
        return redirect('note_detail', pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('home')
    return render(request, 'notes/delete_note.html', {'note': note})