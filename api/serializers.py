from rest_framework import serializers

from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    created_date = serializers.ReadOnlyField()
    completed_date = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created_date', 'completed_date', 'important']


class TodoCompleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['title', 'memo', 'created_date', 'completed_date', 'important']
