from rest_framework import serializers

from core.models import BaseBoard


class BaseBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseBoard
        fields = "__all__"
