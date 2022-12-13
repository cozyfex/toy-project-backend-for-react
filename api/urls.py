from django.urls import path, include
from rest_framework import routers

from api import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'base-board', views.BaseBoardSet, basename='base-board')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dump', views.dump_board, name='dump'),
    path('webhook', views.webhook, name='webhook')
]
