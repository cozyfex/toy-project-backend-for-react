import hmac
import json
import subprocess
from hashlib import sha256
from ipaddress import ip_address, ip_network

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError, JsonResponse
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


# Webhook of GitHub
@require_POST
@csrf_exempt
def webhook(request):
    # Verify if request came from GitHub
    forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
    client_ip_address = ip_address(
        forwarded_for.split(',')[0].strip() if forwarded_for else request.META.get('REMOTE_ADDR')
    )
    whitelist = requests.get('https://api.github.com/meta').json()['hooks']

    valid_access = False
    for valid_ip in whitelist:
        if client_ip_address in ip_network(valid_ip):
            valid_access = True
            break
    if valid_access is not True:
        return HttpResponseForbidden('Permission denied.')

    # Verify the request signature
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE_256')
    if header_signature is None:
        return HttpResponseForbidden('Permission denied.')

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha256':
        return HttpResponseServerError('Operation not supported.', status=501)

    secret = settings.GITHUB_WEBHOOK_KEY.encode('utf-8')
    digest = hmac.new(key=secret, msg=request.body, digestmod=sha256)
    calculated_signature = digest.hexdigest()

    if not hmac.compare_digest(header_signature, 'sha256=' + calculated_signature):
        return HttpResponseForbidden('Permission denied.')

    # If request reached this point we are in a good shape
    # Process the GitHub events
    event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

    if event == 'ping':
        return HttpResponse('pong')
    elif event == 'push':
        # Deploy some code for example
        subprocess.Popen(['git', 'pull', 'origin', 'main'], cwd=settings.BASE_DIR)
        subprocess.Popen(['.venv/bin/pip', 'install', '-r', 'requirements.pip'], cwd=settings.BASE_DIR)
        return HttpResponse('success')

    # In case we receive an event that's not ping or push
    return HttpResponse(status=204)


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
