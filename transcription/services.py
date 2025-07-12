from .models import Transcription
from files.services import AudioFileService
import requests
import tempfile
from django.conf import settings
import environ
from openai import AzureOpenAI

env = environ.Env()


class TranscriptionService:
    def __init__(self, user):
        self.audio_file_service = AudioFileService(user)
        self.user = user

    def get_transcription(self, audio_file_id):
        audio_file = self.audio_file_service.get_audio_file_by_id(
            audio_file_id)
        try:
            # Check if transcription already exists
            transcription = Transcription.objects.get(audio_file=audio_file)
        except Transcription.DoesNotExist:
            return None
        return transcription

    def create_transcription(self, audio_file_id):
        audio_file = self.audio_file_service.get_audio_file_by_id(
            audio_file_id)

        # Get SAS URL of the audio file from Azure Blob Storage
        audio_file_url = self.audio_file_service.get_audio_file_url(
            audio_file_id)

        # Download audio file
        temp_file = self.download_audio_file(
            audio_file_url=audio_file_url,
            extension=f".{audio_file.extension}"
        )

        try:
            # Get transcription text
            transcription_text = self.transcribe_audio(temp_file)
            # Create Transcription record
            transcription = Transcription.objects.create(
                audio_file=audio_file,
                text=transcription_text,
                user=self.user
            )
        finally:
            # Always clean up the temp file
            temp_file.close()
            import os
            os.unlink(temp_file.name)

        return transcription_text

    def download_audio_file(self, audio_file_url, extension=".mp3"):
        print(f"Downloading audio file from: {audio_file_url}")
        response = requests.get(audio_file_url, stream=True)
        response.raise_for_status()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
        temp_file.write(response.content)
        temp_file.flush()
        temp_file.seek(0)
        return temp_file

    def transcribe_audio(self, temp_file):
        """
        Transcribe audio file with Whisper via OpenAIService.
        """
        openai_service = OpenAIService(self.user)
        transcription_text = openai_service.create_transcription(
            temp_file.name)

        return transcription_text


class OpenAIService:
    def __init__(self, user):
        self.user = user
        print(
            env('OPENAI_API_BASE'), env('OPENAI_API_KEY')

        )
        self.client = AzureOpenAI(
            azure_endpoint=env('OPENAI_API_BASE'),
            api_key=env('OPENAI_API_KEY'),
            api_version="2024-06-01"
        )

    def create_transcription(self, audio_file_path):
        with open(audio_file_path, "rb") as audio:
            response = self.client.audio.transcriptions.create(
                model="whisper",
                file=audio
            )
        return response.text
