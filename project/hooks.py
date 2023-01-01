import hmac
import subprocess
from hashlib import sha256

import requests
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseServerError, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ipaddress import ip_address, ip_network


# Webhook of GitHub
@require_POST
@csrf_exempt
def webhook(request):
    # Verify if request came from GitHub
    client_ip = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR')) \
        if request.META.get('HTTP_X_FORWARDED_FOR') \
        else u'{}'.format(request.META.get('REMOTE_ADDR'))
    client_ip_address = ip_address(client_ip)
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
