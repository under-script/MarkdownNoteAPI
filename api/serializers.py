from rest_framework import serializers

from api.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['id', 'author']

class GrammarCheckSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=4000)

    def validate_text(self, value):
        # Optionally add custom validation for text if needed
        if not value.strip():
            raise serializers.ValidationError("Text content cannot be empty.")
        return value

    def check_grammar(self):
        import language_tool_python

        # Get the validated text data
        text = self.validated_data.get('text')

        # Initialize the grammar checker tool
        tool = language_tool_python.LanguageTool('en-US')

        # Check for grammatical errors
        matches = tool.check(text)

        # Construct response with grammar issues
        errors = []
        for match in matches:
            errors.append({
                'issue': match.ruleId,
                'message': match.message,
                'suggestions': match.replacements,
                'context': match.context
            })

        return {'text': text, 'errors': errors}