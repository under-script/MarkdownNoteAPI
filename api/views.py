
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.files.base import ContentFile
import markdown
from .models import Note
from .serializers import NoteSerializer, GrammarCheckSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return NoteSerializer
        return None

    def perform_create(self, serializer):
        # Add author field during creation
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Add author field during update
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], url_path='check-grammar')
    def check_grammar(self, request):
        note = self.get_object()
        serializer = GrammarCheckSerializer(data={'text': note.text})

        if serializer.is_valid():
            result = serializer.check_grammar()
            return Response(result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='render-md-to-html')
    def render_md_to_html(self, request):
        note = self.get_object()

        try:
            if note.md_file:
                md_content = note.md_file.read().decode('utf-8')
            elif note.text:
                md_content = note.text
            else:
                return Response({"error": "No content available for conversion."}, status=status.HTTP_400_BAD_REQUEST)

            html_content = markdown.markdown(md_content)
            html_file = ContentFile(html_content, name=f"{note.title}.html")
            note.html_file.save(f"{note.title}.html", html_file)
            note.save()

            return Response({"success": "Markdown has been rendered to HTML and saved."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)