from django.urls import path, include
from rest_framework import routers
from github_webhooks import urls as github_webhooks_urls

from api import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'base-board', views.BaseBoardSet, basename='base-board')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dump', views.dump_board, name='dump'),
    path('webhooks/github/receive/', include(github_webhooks_urls)),
]
