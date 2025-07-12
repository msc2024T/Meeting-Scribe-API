from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import TranscriptionService
from .serializers import TranscriptionSerializer


class TranscriptionView(APIView):

    def post(self, request, audio_file_id):
        """
        Create a transcription for an audio file.
        POST /transcriptions/
        """
        try:

            user = request.user
            transcription_service = TranscriptionService(user)
            transcription = transcription_service.create_transcription(
                audio_file_id)

            return Response({
                "message": "Transcription created successfully",
                "data": transcription,
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, audio_file_id):
        """
        Retrieve a transcription for an audio file.
        GET /transcriptions/{audio_file_id}/
        """
        try:
            user = request.user
            transcription_service = TranscriptionService(user)
            transcription = transcription_service.get_transcription(
                audio_file_id)
            if not transcription:
                return Response(
                    {"data": "Transcription not found"},
                    status=status.HTTP_200_OK
                )
            serializer = TranscriptionSerializer(transcription)

            return Response({
                "data": serializer.data,
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
