from decimal import Decimal

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from django.db import models
from django_extensions.db import fields as extension_fields
from file_validator.models import FileSizeValidator
from imagekit.models import ProcessedImageField

from votes.models import Vote


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = extension_fields.AutoSlugField(
        max_length=255, unique=True, populate_from="title"
    )
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0))]
    )
    inventory = models.IntegerField(default=0)
    last_update = extension_fields.ModificationDateTimeField()
    collection = models.ForeignKey("Collection", on_delete=models.PROTECT)
    promotions = models.ManyToManyField("Promotion", blank=True)
    votes = GenericRelation(Vote)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["unit_price"]),
        ]

    def __str__(self) -> str:
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = ProcessedImageField(
        upload_to="products/images",
        format="webp",
        options={"quality": 75},
        validators=[FileSizeValidator(max_upload_file_size=5242880)],  # 5 MB
    )


class Collection(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return self.title


class Promotion(models.Model):
    name = models.CharField(max_length=255)
    discount = models.IntegerField(
        verbose_name="discount (in %)",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    content = models.TextField(
        validators=[MinLengthValidator(10), MaxLengthValidator(1000)]
    )
    created_at = extension_fields.CreationDateTimeField()
    votes = GenericRelation(Vote)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["rating"]), models.Index(fields=["created_at"])]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "author"], name="one_review_for_product_per_user"
            ),
        ]

    def __str__(self) -> str:
        return f"Review {self.id}"
