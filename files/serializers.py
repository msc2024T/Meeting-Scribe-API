from rest_framework import serializers
from .models import AudioFile
from users.serializers import UserSerializer


class AudioFileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AudioFile
        fields = ('id', 'name', 'size', 'extention',
                  'durtion_seconds', 'user', 'uploaded_at')
        read_only_fields = ('id', 'user', 'uploaded_at')
