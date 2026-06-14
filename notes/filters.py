from click import option

from .models import Course, Tag

def filter_notes(notes, request):
    course_id = request.GET.get('course')
    tag_id = request.GET.get('tag')
    search = request.GET.get('search')
    note_type = request.GET.get('type')

    if course_id:
        notes = notes.filter(course_id=course_id)
    if tag_id:
        notes = notes.filter(tags__id=tag_id)
    if search:
        notes = notes.filter(title__icontains=search)
    if note_type == 'notes':
        notes = notes.filter(original_note__isnull=True)
    elif note_type == 'forks':
        notes = notes.filter(original_note__isnull=False)

    return notes

def get_filter_context(notes_queryset):
    course_ids = notes_queryset.values_list('course_id', flat=True).distinct()
    tag_ids = notes_queryset.values_list('tags__id', flat=True).distinct()

    courses = Course.objects.filter(id__in=course_ids)
    tags = Tag.objects.filter(id__in=tag_ids)

    return courses, tags

import json

def get_tags_json(tags):
    return json.dumps([{'id': t.id, 'name': t.name} for t in tags])

def get_selected_tags_json(request, tags):
    tag_ids = request.GET.getlist('tag')
    selected = [{'id': t.id, 'name': t.name} for t in tags if str(t.id) in tag_ids]
    return json.dumps(selected)

def sort_notes(notes, request):
    sort = request.GET.get('sort', 'newest')
    if sort == 'oldest':
        notes = notes.order_by('created_at')
    elif sort == 'most_forked':
        from django.db.models import Count
        notes = notes.annotate(forks_count=Count('forks')).order_by('-forks_count')
    elif sort == 'highest_rated':
        from django.db.models import Avg
        notes = notes.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')
    elif sort == 'lowest_rated':
        from django.db.models import Avg
        notes = notes.annotate(avg_rating=Avg('ratings__score')).order_by('avg_rating')
    else:
        notes = notes.order_by('-created_at')
    return notes