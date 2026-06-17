from multiprocessing import context

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .filters import filter_notes, get_filter_context, get_selected_tags_json, get_tags_json, sort_notes
from .forms import NoteForm
from .models import Note, SavedNote, Rating


def home_view(request):
    context = {}
    if request.user.is_authenticated:
        context['saved_count'] = SavedNote.objects.filter(user=request.user).count()
        context['forks_count'] = Note.objects.filter(author=request.user, original_note__isnull=False).count()
        context['notes_count'] = Note.objects.filter(author=request.user, original_note__isnull=True).count()
        context['recent_saved'] = Note.objects.filter(saved_by__user=request.user).order_by('-saved_by__saved_at')[:3]
        context['recent_notes'] = Note.objects.filter(author=request.user, original_note__isnull=True).order_by('-created_at')[:6]
    return render(request, 'notes/home.html', context)

def note_detail_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    is_saved = False
    can_fork = False
    user_rating = 0
    if request.user.is_authenticated:
        is_saved = SavedNote.objects.filter(user=request.user, note=note).exists()
        root_note = note.original_note if note.is_fork else note
        can_fork = (
            root_note.author != request.user and
            not Note.objects.filter(author=request.user, original_note=root_note).exists()
        )
        rating = Rating.objects.filter(user=request.user, note=note).first()
        user_rating = rating.score if rating else 0
    return render(request, 'notes/note_detail.html', {
        'note': note,
        'is_saved': is_saved,
        'can_fork': can_fork,
        'user_rating': user_rating,
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
    notes = Note.objects.filter(saved_by__user=request.user)
    courses, tags = get_filter_context(notes)
    total_courses = courses.count()
    notes = filter_notes(notes, request)
    notes = sort_notes(notes, request)
    return render(request, 'notes/favorites.html', {
        'notes': notes,
        'courses': courses,
        'tags': tags,
        'tags_json': get_tags_json(tags),
        'selected_tags_json': get_selected_tags_json(request, tags),
        'total_notes': total_notes,
        'total_courses': total_courses,
        'current_course': request.GET.get('course'),
        'current_tag': request.GET.get('tag'),
        'current_sort': request.GET.get('sort', 'newest'),
        'show_forks_sort': True,
        'search_context': 'favorites',
    })
    
def explore_view(request):
    notes = Note.objects.all()
    courses, tags = get_filter_context(notes)
    notes = filter_notes(notes, request)
    notes = sort_notes(notes, request)
    return render(request, 'notes/explore.html', {
        'notes': notes,
        'courses': courses,
        'tags': tags,
        'tags_json': get_tags_json(tags),
        'selected_tags_json': get_selected_tags_json(request, tags),
        'current_course': request.GET.get('course'),
        'current_tag': request.GET.get('tag'),
        'current_sort': request.GET.get('sort', 'newest'),
        'show_forks_sort': True,
        'search_context': 'all',
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
    notes = Note.objects.filter(author=request.user, original_note__isnull=False)
    courses, tags = get_filter_context(notes)
    notes_filtered = filter_notes(notes, request)
    notes_filtered = sort_notes(notes_filtered, request)
    return render(request, 'notes/my_forks.html', {
        'notes': notes_filtered,
        'courses': courses,
        'tags': tags,
        'tags_json': get_tags_json(tags),
        'selected_tags_json': get_selected_tags_json(request, tags),
        'current_course': request.GET.get('course'),
        'current_tag': request.GET.get('tag'),
        'current_sort': request.GET.get('sort', 'newest'),
        'show_forks_sort': False,
        'search_context': 'my_forks',
    })
    
@login_required
def my_notes_view(request):
    notes = Note.objects.filter(author=request.user, original_note__isnull=True)
    courses, tags = get_filter_context(notes)
    notes_filtered = filter_notes(notes, request)
    notes_filtered = sort_notes(notes_filtered, request)
    return render(request, 'notes/my_notes.html', {
        'notes': notes_filtered,
        'courses': courses,
        'tags': tags,
        'tags_json': get_tags_json(tags),
        'selected_tags_json': get_selected_tags_json(request, tags),
        'current_course': request.GET.get('course'),
        'current_tag': request.GET.get('tag'),
        'current_sort': request.GET.get('sort', 'newest'),
        'show_forks_sort': True,
        'search_context': 'my_notes',
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

@login_required
def create_note_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                from .models import Tag
                tag_names = [t.strip().lower() for t in tags_input.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    note.tags.add(tag)
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm()
    return render(request, 'notes/create_note.html', {'form': form})

@login_required
def edit_note_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.user != note.author and not request.user.profile.is_admin:
        return redirect('note_detail', pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            tags_input = form.cleaned_data.get('tags_input', '')
            note.tags.clear()
            if tags_input:
                from .models import Tag
                tag_names = [t.strip().lower() for t in tags_input.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    note.tags.add(tag)
            return redirect('note_detail', pk=note.pk)
    else:
        existing_tags = ', '.join(note.tags.values_list('name', flat=True))
        form = NoteForm(instance=note, initial={'tags_input': existing_tags})
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})

@login_required
def rate_note_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        score = request.POST.get('score')
        if score and score.isdigit() and 1 <= int(score) <= 5:
            from .models import Rating
            Rating.objects.update_or_create(
                user=request.user,
                note=note,
                defaults={'score': int(score)}
            )
    return redirect('note_detail', pk=pk)

def search_notes_view(request):
    query = request.GET.get('q', '')
    context = request.GET.get('context', 'all')
    if context == 'favorites' and request.user.is_authenticated:
        notes = Note.objects.filter(saved_by__user=request.user)
    elif context == 'my_notes' and request.user.is_authenticated:
        notes = Note.objects.filter(author=request.user, original_note__isnull=True)
    elif context == 'my_forks' and request.user.is_authenticated:
        notes = Note.objects.filter(author=request.user, original_note__isnull=False)
    else:
        notes = Note.objects.all()
    if query:
        notes = notes.filter(title__icontains=query)
    notes = notes[:10]
    results = [
        {
            'id': note.pk,
            'title': note.title,
            'author': note.author.username,
            'course': note.course.name,
            'course_id': note.course.id,
            'average_rating': note.average_rating(),
            'fork_count': note.fork_count,
            'is_fork': note.is_fork,
        }
        for note in notes
    ]
    return JsonResponse({'results': results})