from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import BaseBoard, Naming


class BaseBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseBoard
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class NamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Naming
        fields = '__all__'
