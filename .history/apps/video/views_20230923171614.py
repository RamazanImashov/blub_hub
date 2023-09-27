from rest_framework import viewsets, generics
from .models import Video, Topics
from rest_framework.response import Response

from .serializer import VideoDetailSerializer, VideoListSerializer, TopicsSerializer
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import logging
from rest_framework.decorators import action
from .permissions import IsAdminPermission, IsAuthorPermission
from apps.review.serializers import *

logger = logging.getLogger(__name__)


class PermissionMixin:
    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy', 'create'):
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class TopicsView(PermissionMixin, viewsets.ModelViewSet):
    queryset = Topics.objects.all()
    serializer_class = TopicsSerializer


class VideoView(PermissionMixin, viewsets.ModelViewSet):
    queryset = Video.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    logger.warning('Предупреждение')
    filterset_fields = ['topics', 'title']
    search_fields = ['title']


    @method_decorator(cache_page(60*10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60*10))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return VideoListSerializer
        return VideoDetailSerializer

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def rating(self, request, pk=None):
        video = self.get_object()
        user = request.user
        serializer = RatingActionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(video=video, author=user)
            message = 'rating'
            return Response(message, status=200)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        video = self.get_object()
        user = request.user
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                like = Like.objects.get(video=video, author=user)
                like.delete()
                message = 'Unlike'
            except Like.DoesNotExist:
                Like.objects.create(video=video, author=user)
                message = 'Like'
            return Response(message, status=200)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        video = self.get_object()
        user = request.user
        serializer = DisLikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                dislike = Dislike.objects.get(video=video, author=user)
                dislike.delete()
                message = 'UnDislike'
            except Dislike.DoesNotExist:
                Dislike.objects.create(video=video, author=user)
                message = 'DisLike'
            return Response(message, status=200)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def watch_later(self, request, pk=None):
        video = self.get_object()
        user = request.user
        serializer = WatchLaterActionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                watchlater = WatchLater.objects.get(video=video, author=user)
                watchlater.delete()
                message = 'UnWatchLater'
            except WatchLater.DoesNotExist:
                WatchLater.objects.create(video=video, author=user)
                message = 'WatchLater'
            return Response(message, status=200)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        video = self.get_object()
        user = request.user
        serializer = CommentActionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(video=video, author=user)
            message = request.data
            return Response(message, status=200)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
from rest_framework import generics, permissions
from .models import Video, Subscription
from .serializer import VideoSerizlizer, SubscriptionSerializer

class VideoList(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class SubscribedVideosList(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Получите видео от пользователей, на которых подписан текущий пользователь
        subscribed_users = user.subscriptions.all().values_list('target_user', flat=True)
        return Video.objects.filter(uploaded_by__in=subscribed_users)
