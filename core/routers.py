from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='posts')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'user', UserViewset, basename='user')
router.register(r'chat', MessageViewSet, basename='chat')

urlpatterns = router.urls
