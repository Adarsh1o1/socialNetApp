from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', Search, basename='user')
router.register(r'friend-requests', FriendRequests, basename='friend_request')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', Signup.as_view() ),
    path('login/', Login.as_view() ),
]