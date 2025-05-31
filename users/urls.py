from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from users.views import (
    UserRegisterView,
    UserLoginView,
    UserDetailView,
    UserUpdateView,
    UserLoyaltyCardView,
    UserPaymentHistoryView,
)

urlpatterns = [
    path('user/register/', csrf_exempt(UserRegisterView.as_view()), name='user-register'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),
    # path('user/logout/', UserLogoutView.as_view(), name='user-logout'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('user/data/', UserUpdateView.as_view(), name='user-update'),
    path('user/loyalty-card/', UserLoyaltyCardView.as_view(), name='user-loyalty-card'),
    path('user/payment-history/', UserPaymentHistoryView.as_view()),
]