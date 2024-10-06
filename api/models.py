from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Note(TimeStampedModel):
    title = models.CharField(max_length=200, unique=True, verbose_name='Note Title')
    md_file = models.FileField(upload_to='notes/md_files/', null=True, blank=True, verbose_name='Markdown File')
    text = models.TextField(max_length=4000, null=True, blank=True, verbose_name='Text Content')
    is_grammar_correct = models.BooleanField(null=True, blank=True, verbose_name='Grammar Correct')
    html_file = models.FileField(upload_to='notes/html_files/', null=True, blank=True, verbose_name='HTML File')
    thumbnail = models.ImageField(upload_to='notes/thumbnails/', null=True, blank=True, verbose_name='Thumbnail')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes', verbose_name='Author')

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __str__(self):
        return f"{self.title} by {self.author}"
