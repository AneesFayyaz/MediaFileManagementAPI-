from django.urls import path
from .views import Mediafileuploadview, loginview, logoutview, registerview
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

urlpatterns = [
    path('upload/', Mediafileuploadview.as_view(), name="mediafile-upload"),
    path('upload/<int:pk>/', Mediafileuploadview.as_view(), name='mediafile_operations'),
    path('login/', loginview.as_view(), name='login'),
    path('logout/', logoutview.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token'),  # Added parentheses here
    path('token/refresh', TokenRefreshView.as_view(), name='tokenrefresh'),  # Added parentheses here
    path('register/', registerview.as_view(), name='register')
]