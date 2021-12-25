"""rest freamwork import"""
from . import api_permissions
from . import serializers
from post import models as post_models
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import (
    viewsets,
    permissions,
    filters,
    status,
    pagination,
)
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404


class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = post_models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          api_permissions.UpdateOwnStatus,)
    pagination_class = pagination.PageNumberPagination

    def perform_create(self, serializer):
        temp_path = self.request.get_full_path().split('/')
        serializer.save(user=self.request.user,
                        question=post_models.Question.objects.get(id=temp_path[3]))

    def get_queryset(self, pk=None, **kwargs):
        if not pk:
            temp_path = self.request.get_full_path().split('/')
            # return self.queryset.filter(question__id__in=temp_path[3])
            return self.queryset.filter(question=post_models.Question.objects.get(id=temp_path[3]))
        return self.queryset


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = post_models.Question.objects.filter(
        published_date__isnull=False)
    serializer_class = serializers.QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          api_permissions.UpdateOwnStatus,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    pagination_class = pagination.PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DarfViewSet(viewsets.ModelViewSet):
    """
    Draf Question publish or edit.
    """
    queryset = post_models.Question.objects.filter(published_date__isnull=True)
    serializer_class = serializers.QuestionSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        api_permissions.UpdateOwnStatus,
    )
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self, **kwargs):
        return self.queryset.filter(user=self.request.user)


@api_view(('GET',))
@permission_classes([permissions.IsAuthenticated, ])
def pulished(request, pk):
    """
    publish question
    """
    question = get_object_or_404(post_models.Question, id=pk)
    if request.user == question.user:
        question.publish()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
