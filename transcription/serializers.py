from rest_framework.serializers import ModelSerializer
from .models import Transcription
from users.serializers import UserSerializer


class TranscriptionSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Transcription
        fields = ('id', 'text', 'audio_file', 'user', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
