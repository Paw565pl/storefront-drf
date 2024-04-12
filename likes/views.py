from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.exceptions import Conflict
from likes.models import LikeDislike
from likes.serializers import LikeDislikeSerializer


# Create your views here.
class LikeDislikeView(RetrieveUpdateDestroyAPIView):
    content_object_queryset: QuerySet | None = None
    integrity_error_message: str | None = None

    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        if self.content_object_queryset is None:
            raise AttributeError("content_object_queryset must be set")
        return super().dispatch(request, *args, **kwargs)

    def get_content_object_id(self, *args, **kwargs):
        content_object_id = self.kwargs.get("pk")

        if content_object_id is None:
            raise AttributeError("you must include the object pk in the url path")

        return content_object_id

    def get_object(self, *args, **kwargs):
        content_object_id = self.get_content_object_id()
        content_type = ContentType.objects.get_for_model(
            self.content_object_queryset.model
        )

        return get_object_or_404(
            self.get_queryset(),
            object_id=content_object_id,
            content_type=content_type,
            user=self.request.user,
        )

    def post(self, request, *args, **kwargs):
        content_object_id = self.get_content_object_id()
        content_object = get_object_or_404(
            self.content_object_queryset, pk=content_object_id
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.get_queryset().create(
                **serializer.validated_data,
                user=request.user,
                content_object=content_object,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            raise Conflict(
                self.integrity_error_message
                or "You have already liked or disliked this resource."
            )
