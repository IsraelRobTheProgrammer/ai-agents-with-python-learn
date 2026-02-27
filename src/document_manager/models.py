from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


# Create your models here.
class Document(models.Model):
    title = models.CharField(default="Title")
    content = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    active_at = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.active and self.active_at:
            self.active_at = timezone.now()
        else:
            self.active_at = None

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"<Document: {self.title}>"
