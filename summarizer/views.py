from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from summarizer.services import SummarizerService
from .serializers import SummaryResultDictSerializer


class SummarizerView(APIView):
    """
    View for summarizing audio files.
    """

    def post(self, request, audio_id):
        """
        Summarize the audio file with the given ID.
        POST /summarizer/summarize/{audio_id}/
        """
        try:
            summarizer_service = SummarizerService(request.user)
            summary = summarizer_service.summarize_all(audio_id)
            serializer = SummaryResultDictSerializer(summary)

            return Response({
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, audio_id):
        """
        Retrieve the summary for the audio file with the given ID.
        GET /summarizer/summarize/{audio_id}/
        """
        try:
            summarizer_service = SummarizerService(request.user)
            summary = summarizer_service.get_summary(audio_id)
            if not summary:
                return Response(
                    {"error": "Summary not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = SummaryResultDictSerializer(summary)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
