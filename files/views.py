from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .services import FileService
from .serializers import AudioFileSerializer


class AudioFileViewSet(ViewSet):

    def create(self, request):
        """
        Upload an audio file.
        POST /audio-files/
        """
        try:
            audio_file = request.FILES.get('audio_file')
            if not audio_file:
                return Response(
                    {"error": "No audio file provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = request.user
            file_service = FileService(user)
            audio_file_record = file_service.upload_audio_file(audio_file)
            serializer = AudioFileSerializer(audio_file_record)

            return Response({
                "message": "Audio file uploaded successfully",
                "data": serializer.data,

            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """
        Get an audio file URL by ID.
        GET /audio-files/{id}/
        """
        try:
            user = request.user
            file_service = FileService(user)
            audio_file_url = file_service.get_audio_file_url(pk)

            return Response({
                "audio_file_url": audio_file_url
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

    def list(self, request):
        """
        List all audio files for the authenticated user.
        GET /audio-files/
        """
        try:
            user = request.user
            file_service = FileService(user)
            audio_files = file_service.get_user_audio_files()
            serializer = AudioFileSerializer(audio_files, many=True)

            return Response({
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
