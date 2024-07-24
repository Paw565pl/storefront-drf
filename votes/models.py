from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Vote(models.Model):
    DISLIKE = -1
    LIKE = 1

    VOTES = ((DISLIKE, "Dislike"), (LIKE, "Like"))

    value = models.SmallIntegerField(verbose_name="Like/Dislike", choices=VOTES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "content_type", "object_id"],
                name="one_vote_per_user",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} {self.get_value_display()} {self.content_type.model} {self.object_id}"
