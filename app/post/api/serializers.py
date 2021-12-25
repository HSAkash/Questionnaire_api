from user import models as user_models
from post import models as post_models
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'image')
        read_only_fields = ('id', 'username', 'email', 'image')


class AnswerSerializer(serializers.ModelSerializer):
    """Answer Serializer"""
    athor = serializers.SerializerMethodField(read_only=True)
    question_id = serializers.PrimaryKeyRelatedField(
        source='question', read_only=True)

    class Meta:
        model = post_models.Answer
        fields = ('id', 'description', 'question_id', 'athor', )
        read_only_fields = ('id', )

    def get_athor(self, obj):
        user = obj.user
        serializer = UserSerializer(user)
        return serializer.data


class QuestionSerializer(serializers.ModelSerializer):
    """Question  serializer"""
    athor = serializers.SerializerMethodField(read_only=True)
    total_answer = serializers.SerializerMethodField()

    class Meta:
        model = post_models.Question
        fields = ('id', 'title', 'description',
                  'created_at', 'total_answer',
                  'published_date', 'athor',
                  )
        read_only_fields = ('id', 'total_answer',
                            'published_date', 'total_answer',)

    def get_athor(self, obj):
        user = obj.user
        serializer = UserSerializer(user)
        return serializer.data

    def get_total_answer(self, obj):
        """Get total answer"""
        return post_models.Answer.objects.filter(question=obj).count()
