from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from api import views
from project import hooks

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'base-board', views.BaseBoardSet, basename='base-board')
router.register(r'user', views.UserSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'jwt-login', obtain_jwt_token),
    path(r'jwt-refresh', refresh_jwt_token),
    path(r'jwt-verify', verify_jwt_token),
    path(r'login', views.post_login, name='login'),
    path(r'dump', views.dump_board, name='dump'),
    path(r'webhook', hooks.webhook, name='webhook')
]
