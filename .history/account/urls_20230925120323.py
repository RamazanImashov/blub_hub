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
    SubscriptionCreateView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
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
    path('subscribe/', SubscriptionCreateView.as_view(), name='subscription-create'),
    # path('lose_password/', LosePasswordView.as_view()),
    # path('lose_password_confirm/<str:email>/<str:activation_code>/', LosePasswordCompleteView.as_view()),
]


