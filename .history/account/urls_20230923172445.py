from django.urls import path, include
from .views import (
    RegisterView,
    ActivationView,
    LogoutView,
    # LosePasswordView,
    # LosePasswordCompleteView,
    ChangePasswordView,
    ForgotPasswordView,
    ForgotPasswordCompleteView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:email>/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('change_password/', ChangePasswordView.as_view()),
    path('lose_password/', ForgotPasswordView.as_view()),
    path('lose_confirm/', ForgotPasswordCompleteView.as_view(), name='forgot'),
    # path('lose_password/', LosePasswordView.as_view()),
    # path('lose_password_confirm/<str:email>/<str:activation_code>/', LosePasswordCompleteView.as_view()),
]

Для создания системы подписок в Django, которая включает в себя три приложения (аккаунты, лайки/рейтинги и видео), вам следует следовать структуре проекта, которая позволит вам интегрировать функциональность подписок во все необходимые места. Вот как вы можете это сделать:

Создайте модель подписок: Определите модель подписок, которая будет связывать пользователей из приложения аккаунтов и пользователей, на которых они подписываются. Эта модель может быть размещена в одном из ваших приложений, например, в приложении аккаунтов:
python
Copy code
# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')

    class Meta:
        unique_together = ('subscriber', 'target_user')
Создайте сериализатор для модели подписок: Определите сериализатор для модели подписок в том же приложении аккаунтов:
python
Copy code
# accounts/serializers.py
from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
Определите представления для подписок: Создайте представления для создания, обновления и удаления подписок. Представления также могут быть размещены в приложении аккаунтов:
python
Copy code
# accounts/views.py
from rest_framework import generics, permissions
from .models import Subscription
from .serializers import SubscriptionSerializer

class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(subscriber=self.request.user)
Настройте URL-пути: Определите URL-пути для представлений подписок в приложении аккаунтов:
python
Copy code
# accounts/urls.py
from django.urls import path
from .views import SubscriptionCreateView

urlpatterns = [
    path('subscribe/', SubscriptionCreateView.as_view(), name='subscription-create'),
    # Другие URL-пути для управления подписками, например, отмена подписки.
]