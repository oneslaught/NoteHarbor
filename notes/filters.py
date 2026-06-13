from .models import Course, Tag

def filter_notes(notes, request):
    course_id = request.GET.get('course')
    tag_id = request.GET.get('tag')

    if course_id:
        notes = notes.filter(course_id=course_id)
    if tag_id:
        notes = notes.filter(tags__id=tag_id)

    return notes

def get_filter_context(notes_queryset):
    course_ids = notes_queryset.values_list('course_id', flat=True).distinct()
    tag_ids = notes_queryset.values_list('tags__id', flat=True).distinct()

    courses = Course.objects.filter(id__in=course_ids)
    tags = Tag.objects.filter(id__in=tag_ids)

    return courses, tags