import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from faker import Faker
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers import BaseBoardSerializer, UserSerializer
from core.models import BaseBoard


# Create your views here.
class BaseBoardSet(viewsets.ModelViewSet):
    serializer_class = BaseBoardSerializer
    pagination_class = PageNumberPagination

    queryset = BaseBoard.objects.all().order_by('-id')


class UserSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    queryset = User.objects.all().order_by('-id')


@require_POST
@csrf_exempt
def post_login(request):
    unicode = request.body.decode('utf-8')
    data = json.loads(unicode)
    username = data['username']
    password = data['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        login_result = {
            "result": True,
            "data": {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.get_full_name(),
            }
        }

        return JsonResponse(login_result)
    else:
        return JsonResponse({'result': False, 'user': None})


# Add dump data
def dump_board():
    fake = Faker(['ko_KR'])

    for _ in range(123):
        board = BaseBoard()
        board.name = fake.name()
        board.title = fake.sentence()
        board.content = fake.sentence()
        board.save()

    return HttpResponse('done')
