# Generated by Django 5.0.7 on 2024-07-24 16:37

import django.core.validators
import django.db.models.deletion
import django_extensions.db.fields
import file_validator.models
import imagekit.models.fields
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Promotion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "discount",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="discount (in %)",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ["title"],
                "indexes": [
                    models.Index(fields=["title"], name="products_co_title_dd4507_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        max_length=255,
                        populate_from="title",
                        unique=True,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "unit_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0"))
                        ],
                    ),
                ),
                ("inventory", models.IntegerField(default=0)),
                (
                    "last_update",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="products.collection",
                    ),
                ),
                (
                    "promotions",
                    models.ManyToManyField(blank=True, to="products.promotion"),
                ),
            ],
            options={
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    imagekit.models.fields.ProcessedImageField(
                        upload_to="products/images",
                        validators=[
                            file_validator.models.FileSizeValidator(
                                max_upload_file_size=5242880
                            )
                        ],
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ]
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        validators=[
                            django.core.validators.MinLengthValidator(10),
                            django.core.validators.MaxLengthValidator(1000),
                        ]
                    ),
                ),
                (
                    "created_at",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["title"], name="products_pr_title_7d8124_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["slug"], name="products_pr_slug_3edc0c_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["unit_price"], name="products_pr_unit_pr_4a871b_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="review",
            index=models.Index(fields=["rating"], name="products_re_rating_7ca3f6_idx"),
        ),
        migrations.AddIndex(
            model_name="review",
            index=models.Index(
                fields=["created_at"], name="products_re_created_7e194a_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                fields=("product", "author"), name="one_review_for_product_per_user"
            ),
        ),
    ]
