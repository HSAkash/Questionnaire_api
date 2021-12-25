from django.db import models
from django.db import models
from django.utils import timezone
from django.conf import settings


class Question(models.Model):
    """Post model for Asking question"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questionuser')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Answer(models.Model):
    """Answer model for answering question"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='answeruser')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answerpost')
    description = models.TextField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    def accept(self):
        self.is_accepted = True
        self.save()
