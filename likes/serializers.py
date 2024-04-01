from rest_framework import serializers

from likes.models import LikeDislike


class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ["vote"]
