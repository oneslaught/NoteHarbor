from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name
    
class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')
    original_note = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='forks'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class SavedNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_notes')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'note')

    def __str__(self):
        return f'{self.user.username} → {self.note.title}'
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('user', 'note')

    def __str__(self):
        return f'{self.user.username} → {self.note.title}: {self.score}'