from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from .models import Like, Comment, Rating, Dislike, WatchLater
# from apps.video.serializer import VideoListSerializer


class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment


class CommentActionSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    video = ReadOnlyField()

    class Meta:
        model = Comment
        fields = '__all__'

    def validate_product(self, video):
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(video=video, author=user):
            raise ValidationError(
                "You can't be rating"
            )
        return video


class RatingSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def validate_rating(self, rating):
        if rating in range(1, 6):
            return rating
        raise ValidationError(
            'rating not be more 5'
        )

    def validate_video(self, video):
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(video=video, author=user):
            raise ValidationError(
                "You can't be rating"
            )
        return video

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)


class RatingActionSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    video = ReadOnlyField()

    class Meta:
        model = Rating
        fields = '__all__'

    def validate_rating(self, rating):
        if rating in range(1, 6):
            return rating
        raise ValidationError(
            'rating not be more 5'
        )

    def validate_product(self, video):
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(video=video, author=user):
            raise ValidationError(
                "You can't be rating"
            )
        return video


class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    video = ReadOnlyField()

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)


class DisLikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    video = ReadOnlyField()

    class Meta:
        model = Dislike
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)



class WatchLaterActionSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    video = ReadOnlyField()

    class Meta:
        model = WatchLater
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)


# <<<<<<< HEAD
# class WatchLaterListSerializer(ModelSerializer):
#     video = VideoListSerializer()
#
#     class Meta:
#         model = WatchLater
#         fields = ['video']
#
#
# class WatchLaterCreateSerializer(ModelSerializer):
#     author = ReadOnlyField(source='author.email')
#
#     class Meta:
#         model = WatchLater
#         fields = '__all__'
#
#
# =======
# class WatchLaterListSerializer(ModelSerializer):
#     author = ReadOnlyField(source='author.email')
#
#     class Meta:
#         model = WatchLater
#         fields = 'video'
#
#
# class WatchLaterDitailSerializer(ModelSerializer):
#     author = ReadOnlyField(source='author.email')
#
#     class Meta:
#         model = WatchLater
#         fields = ['video', 'author']


class WatchLaterSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    class Meta:
        model = WatchLater
        fields = ['author', 'video']

from rest_framework import generics, permissions
from .models import Video, Subscription
from .serializers import VideoSerializer, SubscriptionSerializer

class VideoList(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

# class SubscribedVideosList(generics.ListAPIView):
#     serializer_class = VideoSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         # Получите видео от пользователей, на которых подписан текущий пользователь
#         subscribed_users = user.subscriptions.all().values_list('target_user', flat=True)
#         return Video.objects.filter(uploaded_by__in=subscribed_users)
