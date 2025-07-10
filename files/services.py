from .models import AudioFile
from datetime import datetime, timedelta
from django.utils import timezone
from azure.storage.blob import BlobServiceClient, ContentSettings, generate_blob_sas, BlobSasPermissions
import environ
import uuid
from mutagen import File
from users.services import UserQuotaService


env = environ.Env()


class AzureBlobService:
    def __init__(self):
        self.connection_string = env('AZURE_BLOB_CONNECTION_STRING')
        self.client = BlobServiceClient.from_connection_string(
            self.connection_string)
        self.container = self.client.get_container_client(
            env('AZURE_STORAGE_CONTAINER_NAME'))

    def upload(self, blob_name, file, content_type="application/octet-stream"):
        blob_client = self.container.get_blob_client(blob_name)
        blob_client.upload_blob(
            file,  content_settings=ContentSettings(content_type=content_type))
        return blob_client.url

    def delete(self, blob_name):
        self.container.delete_blob(blob_name)

    def generate_sas_url(self, blob_name, content_disposition=None, expiry_minutes=15):
        blob_client = self.container.get_blob_client(blob_name)

        # Create SAS token with content disposition
        sas_token = generate_blob_sas(
            account_name=env('AZURE_STORAGE_ACCOUNT_NAME'),
            container_name=env('AZURE_STORAGE_CONTAINER_NAME'),
            blob_name=blob_name,
            account_key=env('AZURE_STORAGE_KEY'),
            permission=BlobSasPermissions(read=True),
            expiry=timezone.now() + timedelta(minutes=expiry_minutes),
            content_disposition=content_disposition  # Add content disposition
        )

        # Construct the full URL with SAS token
        return f"{blob_client.url}?{sas_token}"


class AudioFileService:

    def __init__(self, user):
        self.azure_blob_service = AzureBlobService()
        self.user = user
        self.dir_root = "meetingscribe/"

    def upload_Audio_file(self, audio_file, user):
        if not audio_file:
            raise ValueError("No audio file provided")

        # check file extension
        if not audio_file.name:
            raise ValueError("Audio file name is required")
        if '.' not in audio_file.name:
            raise ValueError("Audio file name must have an extension")
        extension = audio_file.name.split('.')[-1].lower()
        if extension not in ['mp3', 'wav', 'ogg', 'flac', 'm4a']:
            raise ValueError("Unsupported audio file format")

        # chek file size is less than 50MB
        if audio_file.size > 50 * 1024 * 1024:  #
            raise ValueError("Audio file size exceeds 50MB limit")

        # check autio file duration is less than maximum allowed duration
        audio = File(audio_file)
        duraton_seconds = audio.info.length

        user_quota_service = UserQuotaService(user)
        user_quota = user_quota_service.get_quota()
        if duraton_seconds > (user_quota.max_minutes - user_quota.used_minutes) * 60:
            raise ValueError("Audio file duration exceeds user's limit")

        # Create a unique blob name
        unique_id = str(uuid.uuid4())
        blob_name = f"{self.dir_root}{unique_id}.{extension}"

        # Upload the file to Azure Blob Storage
        url = self.azure_blob_service.upload(blob_name, audio_file)
        if not url:
            raise ValueError(
                "Failed to upload audio file to Azure Blob Storage")

        # Save the file metadata to the database
        audio_file_record = AudioFile.objects.create(
            id=unique_id,
            name=audio_file.name,
            size=audio_file.size,
            extention=extension,
            durtion_seconds=duraton_seconds,
            user=user,
            uploaded_at=timezone.now()
        )

        # Update user's quota
        user_quota_service.update_quota(duraton_seconds / 60)
        return audio_file_record

    def get_audio_file_url(self, audioFile_id):
        try:
            audio_file = AudioFile.objects.get(
                id=audioFile_id, user=self.user)
            blob_name = f"{self.dir_root}{audio_file.id}.{audio_file.extention}"
            return self.azure_blob_service.generate_sas_url(blob_name)

        except AudioFile.DoesNotExist:
            raise ValueError("Audio File not found")

    def get_user_audio_files(self):
        audio_files = AudioFile.objects.filter(user=self.user)
        if not audio_files:
            raise ValueError("No audio files found for the user")

        return audio_files
