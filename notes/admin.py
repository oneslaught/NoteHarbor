from django.contrib import admin
from .models import Course, Tag, Note, SavedNote, Rating

# Register your models here.

admin.site.register(Course)
admin.site.register(Tag)
admin.site.register(Note)
admin.site.register(SavedNote)
admin.site.register(Rating)