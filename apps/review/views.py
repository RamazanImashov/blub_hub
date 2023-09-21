from .models import Like, Dislike, Comment, Rating
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from .perimissions import IsAuthor
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ('update', 'partial_update', 'destroy'):
            permissions = [IsAuthor]
        else:
            permissions = [AllowAny]
        return [permissions() for permissions in permissions]


class CommentView(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RatingView(PermissionMixin, ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


# <<<<<<< HEAD
# class WatchLaterListView(ListAPIView):
#     serializer_class = WatchLaterListSerializer
#     permission_classes = (IsAuthenticated,)
# =======
# class WatchLaterView(ModelViewSet):
#     serializer_class = WatchLaterListSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         return self.request.user.watch_later.all()
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return WatchLaterListSerializer
#         return WatchLaterDitailSerializer

class WatchLaterViewSet(ModelViewSet):
    queryset = WatchLater.objects.all()
    serializer_class = WatchLaterSerializer


    def get_queryset(self):
        return self.request.user.watch_later.all()

# <<<<<<< HEAD
#
# class WatchLaterDeleteView(DestroyAPIView):
#     lookup_url_kwarg = 'pk'
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         return self.request.user.watch_later.all()
# =======
# >>>>>>> 582fcad (h1)
