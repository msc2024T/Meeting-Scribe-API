from rest_framework import serializers
from .models import Summary, actionItem, KeyPoint


class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = actionItem
        fields = ['id', 'description', 'assigned_to', 'due_date', 'status']


class KeyPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyPoint
        fields = ['id', 'content']


class SummaryResultSerializer(serializers.ModelSerializer):
    action_items = ActionItemSerializer(many=True, read_only=True)
    key_points = KeyPointSerializer(many=True, read_only=True)

    class Meta:
        model = Summary
        fields = ['id', 'subject', 'action_items', 'key_points', 'created_at']


# Alternative: If you're passing the data as a dictionary (not model instances)
class SummaryResultDictSerializer(serializers.Serializer):
    subject = serializers.CharField()
    action_items = ActionItemSerializer(many=True)
    key_points = KeyPointSerializer(many=True)
