from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create a single default router
router = DefaultRouter()

# Register the viewSets with the router
router.register(r'users', UserViewSet)
router.register(r'sessions', SessionViewSet, basename='sessions')
router.register(r'files', GeeksModelViewSet)

# Define the urlpatterns using the router's and views URLs 
urlpatterns = [
    path('', include(router.urls)),
    path('user-sessions/<str:username>', GetUserSessions.as_view()),
    path('archived-sessions/', ArchivedSessions.as_view()),
    path('all-sessions/', AllSessions.as_view()),
    path('save-session-messages/', SaveSessionMessage.as_view()),
    path('create-session/', CreateSession.as_view()),
    path('update-session/<int:pk>', UpdateSession.as_view()),
    # JWT API URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]