from .models import Transcription
from files.services import AudioFileService
import azure.cognitiveservices.speech as speechsdk
import requests
import ffmpeg
import os
import time
import tempfile
from django.conf import settings


class TranscriptionService:
    def __init__(self, user):
        self.audio_file_service = AudioFileService(user)
        self.user = user

    def get_transcription(self, audio_file_id):
        audio_file = self.audio_file_service.get_audio_file_by_id(
            audio_file_id)
        transcription = Transcription.objects.get(audio_file=audio_file)
        return transcription

    def create_transcription(self, audio_file_id):
        audio_file = self.audio_file_service.get_audio_file_by_id(
            audio_file_id)

        # Download the audio file from Azure Blob Storage
        audio_file_url = self.audio_file_service.get_audio_file_url(
            audio_file_id)

        # Use temporary files with proper cleanup
        temp_mp3_path = None
        temp_wav_path = None

        try:
            # Download audio file
            temp_mp3_path = self.download_audio_file(audio_file_url)

            # Convert to WAV for compatibility
            temp_wav_path = self.convert_to_wav(temp_mp3_path)

            # Transcribe using Azure Speech SDK
            transcription = self.transcribe_audio(temp_wav_path, audio_file)

            return transcription

        finally:
            # Clean up temporary files
            if temp_mp3_path and os.path.exists(temp_mp3_path):
                os.remove(temp_mp3_path)
                print(f"Cleaned up temporary MP3: {temp_mp3_path}")
            if temp_wav_path and os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
                print(f"Cleaned up temporary WAV: {temp_wav_path}")

    def download_audio_file(self, audio_file_url):
        """Download audio file from Azure Blob Storage URL"""
        try:
            print(f"Downloading audio file from: {audio_file_url}")

            response = requests.get(audio_file_url, stream=True)
            response.raise_for_status()

            # Create temporary file for MP3
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        temp_file.write(chunk)

                temp_file_path = temp_file.name
                print(f"Audio file downloaded to: {temp_file_path}")
                print(
                    f"Downloaded file size: {os.path.getsize(temp_file_path)} bytes")
                return temp_file_path

        except requests.exceptions.RequestException as e:
            print(f"Error downloading audio file: {str(e)}")
            raise ValueError(f"Failed to download audio file: {str(e)}")
        except Exception as e:
            print(f"Unexpected error downloading audio file: {str(e)}")
            raise ValueError(f"Failed to download audio file: {str(e)}")

    def convert_to_wav(self, input_path):
        """Convert audio file to WAV format using ffmpeg"""
        try:
            print("Converting to WAV...")

            # Create temporary file for WAV output
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                output_path = temp_file.name

            # Use ffmpeg-python to convert
            (
                ffmpeg.input(input_path)
                .output(output_path, format="wav", acodec="pcm_s16le", ar=16000)
                .overwrite_output()
                .run(quiet=True)
            )

            print(f"Conversion completed. WAV file: {output_path}")
            print(f"WAV file size: {os.path.getsize(output_path)} bytes")
            return output_path

        except ffmpeg.Error as e:
            print(f"FFmpeg error: {e}")
            raise ValueError(f"Failed to convert audio file: {e}")
        except Exception as e:
            print(f"Unexpected error during conversion: {str(e)}")
            raise ValueError(f"Failed to convert audio file: {str(e)}")

    def transcribe_audio(self, wav_file_path, audio_file):
        """Transcribe audio using Azure Speech SDK"""
        try:
            print("Initializing Speech SDK...")

            # Use Django settings for environment variables
            speech_config = speechsdk.SpeechConfig(
                subscription=settings.SPEECH_KEY, region=settings.SERVICE_REGION
            )

            # Configure for better recognition
            speech_config.speech_recognition_language = "en-US"

            audio_input = speechsdk.AudioConfig(filename=wav_file_path)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config, audio_config=audio_input
            )

            print("Starting transcription...")

            # Use continuous recognition for longer audio files
            done = False
            transcript_segments = []

            def recognized_handler(evt):
                if evt.result.text:
                    print(f"Recognized: {evt.result.text}")
                    transcript_segments.append(evt.result.text)

            def stop_handler(evt):
                nonlocal done
                print("Transcription session stopped.")
                done = True

            def canceled_handler(evt):
                nonlocal done
                print(f"Transcription canceled: {evt.reason}")
                if evt.reason == speechsdk.CancellationReason.Error:
                    print(f"Error details: {evt.error_details}")
                done = True

            speech_recognizer.recognized.connect(recognized_handler)
            speech_recognizer.session_stopped.connect(stop_handler)
            speech_recognizer.canceled.connect(canceled_handler)

            speech_recognizer.start_continuous_recognition()

            # Wait for completion (with timeout)
            timeout = 300  # 5 minutes timeout
            elapsed = 0
            while not done and elapsed < timeout:
                time.sleep(1)
                elapsed += 1

            speech_recognizer.stop_continuous_recognition()

            # Combine all transcript segments
            full_transcript = " ".join(transcript_segments).strip()
            print(f"Full transcript: {full_transcript}")

            if full_transcript:
                transcription = Transcription.objects.create(
                    audio_file=audio_file,
                    text=full_transcript,
                    user=self.user,
                )
                return transcription
            else:
                raise ValueError("Transcription failed: No text recognized.")

        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            raise ValueError(f"Transcription failed: {str(e)}")
