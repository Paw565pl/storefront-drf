from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response

from core.exceptions import Conflict
from likes.models import LikeDislike
from likes.serializers import LikeDislikeSerializer


# Create your views here.
class LikeDislikeViewSet(GenericAPIView):
    content_object_queryset: QuerySet | None = None
    integrity_error_message: str | None = None

    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer

    def dispatch(self, request, *args, **kwargs):
        if self.content_object_queryset is None:
            raise AttributeError("content_object_queryset must be set")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        object_id = self.kwargs["pk"]
        content_type = ContentType.objects.get_for_model(
            self.content_object_queryset.model
        )
        return get_object_or_404(
            self.get_queryset(),
            object_id=object_id,
            content_type=content_type,
            user=self.request.user,
        )

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        content_object = get_object_or_404(
            self.content_object_queryset, pk=kwargs["pk"]
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.get_queryset().create(
                **serializer.validated_data,
                user=request.user,
                content_object=content_object
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            raise Conflict(
                self.integrity_error_message
                or "You have already liked or disliked this resource."
            )

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        instance.vote = serializer.validated_data["vote"]
        instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
