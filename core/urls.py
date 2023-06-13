from .views import * 
from django.urls import path, include

urlpatterns = [

    path('postlist/', PostList.as_view(), name='postlist'),
    path('postdetail/', PostDetail.as_view(), name='postdetail'),
    path('profiledetail/', ProfileDetail.as_view(), name='profiledetail'),

]