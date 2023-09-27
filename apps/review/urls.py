from django.urls import path, include
from .views import CommentView,  WatchLaterViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('comments', CommentView)
# router.register('ratings', RatingView)
router.register('watch_later', WatchLaterViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('watch_laters/', WatchLaterView.as_view(), name='list'),
]