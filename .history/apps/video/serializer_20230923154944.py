from rest_framework.serializers import ModelSerializer
from .models import Topics, Video

from apps.review.serializers import CommentSerializer
from django.db.models import Avg
from apps.video.serializers import 

class TopicsSerializer(ModelSerializer):
    class Meta:
        model = Topics
        fields = '__all__'


class VideoListSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_preview', 'title']


class VideoDetailSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        rep['likes'] = instance.likes.all().count()
        rep['dislikes'] = instance.dislikes.all().count()
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return rep

