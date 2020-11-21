import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Question(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question = models.CharField(_("question"), max_length=150)
    is_general = models.BooleanField(_("is_general"))
    categories = models.CharField(_("categories"), max_length=100)
    point = models.PositiveIntegerField(_("point"), null=True)
    icon_url = models.URLField(_("icon_url"), null=True)
    duration = models.PositiveIntegerField(_("duration"), null=True)
    date_created = models.DateField(_("date_created"), auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

class Choices(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice = models.CharField(_("choice"), max_length=70)
    is_correct_choice = models.BooleanField(_("is_correct_choice"))
    is_icon_url = models.URLField(_("is_icon_url"), null=True)






