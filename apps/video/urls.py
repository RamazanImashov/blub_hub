from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicsView, VideoView


router = DefaultRouter()
router.register('topics', TopicsView)
router.register('videos', VideoView)


urlpatterns = [
    path('', include(router.urls)), 
]
