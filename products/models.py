from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

from products.validators import validate_file_size


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    inventory = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey("Collection", on_delete=models.PROTECT)
    promotions = models.ManyToManyField("Promotion", blank=True)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["unit_price"]),
            models.Index(fields=["inventory"]),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="products/images", validators=[validate_file_size]
    )

    def save(self, *args, **kwargs):
        image = Image.open(self.image)

        output_io = BytesIO()
        image.save(output_io, format=image.format, quality=75)

        file = InMemoryUploadedFile(
            output_io,
            None,
            self.image.name,
            "image/jpeg",
            output_io.getbuffer().nbytes,
            None,
        )
        self.image.save(self.image.name, file, save=False)

        super().save(*args, **kwargs)


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
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MinValueValidator(10)]
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["rating"]), models.Index(fields=["created_at"])]

    def __str__(self) -> str:
        return f"Review by {self.author}"
