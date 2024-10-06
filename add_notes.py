# add_notes.py

import os

import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.models import Note

# Get the user model
User = get_user_model()

# Replace with an existing user instance
user_instance = User.objects.get(email='goldendevuz@gmail.com')  # Use an existing username

# Path to media directory
media_root = os.path.join(os.path.dirname(__file__), 'media_files')

# Create Note instances
notes_data = [
    {
        "title": "Django Models Tutorial",
        "md_file": os.path.join(media_root, 'notes/md_files/django_models.md'),
        "text": "This note covers the basics of Django models, including fields, methods, and model inheritance.",
        "is_grammar_correct": True,
        "author": user_instance
    },
    {
        "title": "Learning Python",
        "text": "Python is a versatile programming language known for its simplicity and readability.",
        "is_grammar_correct": True,
        "thumbnail": os.path.join(media_root, 'notes/thumbnails/python_thumbnail.jpg'),
        # Updated to use a real image file
        "author": user_instance
    },
    {
        "title": "Web Development with Django",
        "html_file": os.path.join(media_root, 'notes/html_files/web_development.html'),
        "text": "An introduction to building web applications using Django.",
        "is_grammar_correct": False,
        "author": user_instance
    },
    {
        "title": "Quick Python Tips",
        "author": user_instance
    },
    {
        "title": "Advanced Django Techniques",
        "md_file": os.path.join(media_root, 'notes/md_files/django_models.md'),
        "text": "This note covers advanced features in Django, such as custom template tags and signals.",
        "is_grammar_correct": True,
        "html_file": os.path.join(media_root, 'notes/html_files/web_development.html'),
        "thumbnail": os.path.join(media_root, 'notes/thumbnails/django_thumbnail.jpg'),
        # Updated to use a real image file
        "author": user_instance
    }
]

# Add notes to the database
for note_data in notes_data:
    note = Note.objects.create(
        title=note_data['title'],
        text=note_data.get('text', ''),
        is_grammar_correct=note_data.get('is_grammar_correct', None),
        author=note_data['author']
    )

    # Adding files if they exist
    if 'md_file' in note_data and os.path.exists(note_data['md_file']):
        with open(note_data['md_file'], 'rb') as file:
            note.md_file.save(os.path.basename(note_data['md_file']), file)

    if 'html_file' in note_data and os.path.exists(note_data['html_file']):
        with open(note_data['html_file'], 'rb') as file:
            note.html_file.save(os.path.basename(note_data['html_file']), file)

    if 'thumbnail' in note_data and os.path.exists(note_data['thumbnail']):
        with open(note_data['thumbnail'], 'rb') as file:
            note.thumbnail.save(os.path.basename(note_data['thumbnail']), file)

print("Notes have been added successfully.")
