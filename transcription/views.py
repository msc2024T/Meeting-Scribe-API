from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import TranscriptionService


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
