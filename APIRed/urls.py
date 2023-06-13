
from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.static import serve
from django.conf import settings
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_viewset/', include('core.routers')),
    path('posts/', include('core.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='login'),
]


urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
    ]