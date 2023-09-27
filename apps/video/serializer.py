from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Topics, Video
from apps.review.serializers import CommentSerializer
from django.db.models import Avg
# from apps.video.serializer import *

class TopicsSerializer(ModelSerializer):
    class Meta:
        model = Topics
        fields = '__all__'


class VideoListSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_preview', 'title', 'slug']


class VideoDetailSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.email')

    class Meta:
        model = Video
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        video = Video.objects.create(user=user,  **validated_data)
        return video

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.all().count()
        rep['dislikes'] = instance.dislikes.all().count()
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return rep





