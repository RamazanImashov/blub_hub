from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicsView, VideoView, WatchLaterViewSet


router = DefaultRouter()
router.register('topics', TopicsView)
router.register('videos', VideoView)


urlpatterns = [
    path('', include(router.urls)),
    path('watch_later/', WatchLaterViewSet.as_view(), name='list')
]
