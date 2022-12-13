from django.shortcuts import render
from faker import Faker
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers import BaseBoardSerializer
from core.models import BaseBoard


# Create your views here.
class BaseBoardSet(viewsets.ModelViewSet):
    serializer_class = BaseBoardSerializer
    pagination_class = PageNumberPagination

    queryset = BaseBoard.objects.all().order_by('-id')


def dump_board():
    fake = Faker(['ko_KR'])

    for _ in range(123):
        board = BaseBoard()
        board.name = fake.name()
        board.content = fake.sentence()
        board.save()

    return ''
