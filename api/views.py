import hmac
from hashlib import sha256
from ipaddress import ip_address, ip_network

import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
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


# Webhook of GitHub
# @require_POST
@csrf_exempt
def webhook(request):
    # Verify if request came from GitHub
    forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
    # client_ip_address = ip_address(
    #     forwarded_for.split(',')[0].strip() if forwarded_for else request.META.get('REMOTE_ADDR')
    # )
    # client_ip_address = ip_address('185.199.108.3')
    # whitelist = requests.get('https://api.github.com/meta').json()['hooks']
    #
    # valid_access = False
    # for valid_ip in whitelist:
    #     if client_ip_address in ip_network(valid_ip):
    #         valid_access = True
    #         break
    # if valid_access is not True:
    #     return HttpResponseForbidden('Permission denied.')

    # Verify the request signature
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE-256')
    header_signature = 'sha256=37591682021f0f59d63dc632764cb049728277709566703ebf22ce67af7e1875'
    if header_signature is None:
        return HttpResponseForbidden('Permission denied.')

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha256':
        return HttpResponseServerError('Operation not supported.', status=501)

    signature_bytes = bytes(settings.GITHUB_WEBHOOK_KEY, 'utf-8')
    digest = hmac.new(key=signature_bytes, msg=request.body, digestmod=sha256)
    calculated_signature = digest.hexdigest()

    if calculated_signature != signature:
        return HttpResponseForbidden('Permission denied.')

    # If request reached this point we are in a good shape
    # Process the GitHub events
    event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

    if event == 'ping':
        return HttpResponse('pong')
    elif event == 'push':
        # Deploy some code for example
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
