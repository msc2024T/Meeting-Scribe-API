import environ
from openai import AzureOpenAI
from transcription.services import TranscriptionService
import json
from django.utils import timezone
from .models import Summary, actionItem, KeyPoint

# Initialize environment variables
env = environ.Env()


class SummarizerService:

    def __init__(self, user):
        self.client = AzureOpenAI(
            azure_endpoint=env('OPENAI_API_BASE'),
            api_key=env('OPENAI_API_KEY'),
            api_version="2024-12-01-preview"
        )
        self.user = user

    def get_subject(self, text):
        instruction = (
            "You are a helpful assistant. "
            "Read the following meeting transcript and return ONLY a short subject line summarizing the meeting."
        )
        return self._call_gpt(instruction, text)

    def extract_action_items(self, text):
        instruction = (
            "You are a helpful assistant. "
            "Extract all action items from this meeting transcript. "
            "Return JSON array with fields: description, assigned_to, due_date"
        )
        format_example = '''
[
{
    "description": "Description of the action item.",
    "assigned_to": "Person assigned",
    "due_date": "Due date (if available)."
    
}
]
'''
        return self._call_gpt(instruction + "\nFormat:\n" + format_example, text)

    def extract_key_points(self, text):
        instruction = (
            "You are a helpful assistant. "
            "Extract the key points from this meeting transcript. "
            "Return JSON array with each item having a 'content' field."
        )
        format_example = '''
[
{
    "content": "Key point text here."
}
]
'''
        return self._call_gpt(instruction + "\nFormat:\n" + format_example, text)

    def _call_gpt(self, system_message, text):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text}
            ],
            max_tokens=1024,
            temperature=0.3,
            top_p=1.0
        )
        return response.choices[0].message.content

    def summarize_all(self, audio_id):

        transcription_service = TranscriptionService(self.user)
        transcription = transcription_service.get_transcription(
            audio_file_id=audio_id)
        if not transcription:
            raise ValueError(
                "Transcription not found for the given audio file ")
        text = transcription.text

        instruction = (
            "You are a helpful assistant. "
            "Read the following meeting transcript and return a JSON object with three fields: "
            "'subject' (a short subject line), "
            "'action_items' (a list of action items), "
            "and 'key_points' (a list of key points).\n\n"
            "Return ONLY valid JSON in this format:"
        )
        format_example = '''
                {
                "subject": "Short subject line.",
                "action_items": [
                    {
                    "description": "Description of the action item.",
                    "assigned_to": "Person assigned.",
                    "due_date": "Due date if available.",
                    "status": "pending"
                    }
                ],
                "key_points": [
                    {
                    "content": "Key point text here."
                    }
                ]
                }
                '''
        data = json.loads(self._call_gpt(
            instruction + "\nFormat:\n" + format_example, text))
        result = self.save_summary(transcription, data)

        return result

    def save_summary(self, transcription, summary_data):

        summary = Summary.objects.create(
            transcription=transcription,
            subject=summary_data.get('subject', ''),
            created_at=timezone.now()
        )
        action_items = []

        for item in summary_data.get('action_items', []):
            actionItem.objects.create(
                summary=summary,
                description=item.get('description', ''),
                assigned_to=item.get('assigned_to', ''),
                due_date=item.get('due_date'),
                status=item.get('status', 'pending')
            )
            action_items.append(item)

        key_points = []

        for point in summary_data.get('key_points', []):
            KeyPoint.objects.create(
                summary=summary,
                content=point.get('content', '')
            )

            key_points.append(point)

        result = dict(
            subject=summary.subject,
            action_items=action_items,
            key_points=key_points
        )

        return result

    def get_summary(self, audio_id):
        try:
            transcription_service = TranscriptionService(self.user)
            transcription = transcription_service.get_transcription(
                audio_file_id=audio_id)
            if not transcription:
                return None

            summary = Summary.objects.get(transcription=transcription)
            action_items = summary.action_items.all()
            key_points = summary.key_points.all()
            result = dict(
                subject=summary.subject,
                action_items=[item for item in action_items],
                key_points=[point for point in key_points]
            )
            return result
        except Summary.DoesNotExist:
            return None
