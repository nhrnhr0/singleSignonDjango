from django.shortcuts import render
import json
from django.http import JsonResponse
import uuid
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
import requests
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
import base64
from urllib.parse import quote


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_screen(request):
    if request.method == 'POST':
        screen_id = request.data['screen_id']
        screen_name = request.data['screen_name']
        user = request.user
        org = user.organization
        
        # Check if the screen_id is already registered
        screen = User.objects.filter(username=f'screen_{screen_id}').first()
        if screen:
            return JsonResponse({'status': 'error','detail': f'Screen {screen_id} already registered'}, status=400)
        
        
        # Register the screen (create a user with viwer permission)
        username = f'screen_{screen_id}'
        password = str(uuid.uuid4())
        
        screen = User.objects.create_user(username=username, password=password)
        screen.organization = org
        screen.type = User.TYPE_SCREEN
        screen.name = screen_name
        screen.save()
        
        register_screen_at_standalog_server(screen_id,screen_name, org.backend_domain, request.META.get("HTTP_AUTHORIZATION"))
        
        print(f'Screen {screen_id} registered to {user.username}')
        
        # redirect_to
        redirect_to = org.frontend_domain + '/dashboard/screens/?id=' + screen_id + '&auth_token=' + encoded_auth_token(user)
        
        return JsonResponse({'status':'success', 'detail': f'Screen {screen_id} registered to {user.username}', 'redirect_to': redirect_to}, status=200)
    return render(request, 'register_screen.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def get_screen_access(request):
    # if screen.credential_sent is False: set the password to UUID and send the credentials to the screen
    # if screen.credential_sent is True: send error message
    # retrun error if credentials was not sent
    if request.method == 'POST':
        data = json.loads(request.body)
        screen_id = data.get('screen_id')
        screen = User.objects.filter(username=f'screen_{screen_id}').first()
        
        if not screen:
            return JsonResponse({'status': 'error','error_type': 'not_found','message': f'Screen {screen_id} not found'}, status=200)
        
        if screen.user_type != User.TYPE_SCREEN:
            return JsonResponse({'status': 'error', 'error_type': 'not_screen', 'message': f'User {screen_id} is not a screen'}, status=200)
        
        if screen.credential_sent:
            return JsonResponse({'status': 'error', 'error_type': 'credentials_sent', 'message': f'Credentials for screen {screen_id} already sent'}, status=200)
        
        screen.credential_sent = True
        new_pass = str(uuid.uuid4())
        screen.set_password(new_pass)
        screen.save()
        
        # need to create a 'redirect_to' with a url to the standalong server with the screen display
        # <screen.organization>/display/?id=<screen.uuid>&auth_token=<auth_token>
        # getting auth_token from api-token-auth
        
        redirect_to = screen.organization.frontend_domain + '/display?id=' + screen_id + '&auth_token=' + encoded_auth_token(screen)
        
        return JsonResponse({'status': 'success', 'message': f'Credentials sent to screen {screen_id}', 'redirect_to':redirect_to}, status=200)
    pass


def encoded_auth_token(screen):
    auth_token = Token.objects.get(user=screen).key
    auth_b64 = base64.b64encode(json.dumps({'auth_token': auth_token}).encode()).decode()
    auth_b64Safe = quote(auth_b64)
    return auth_b64Safe


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return JsonResponse({'username': user.username, 'backend_domain': user.organization.backend_domain,'frontend_domain':  user.organization.frontend_domain, 'type': user.user_type})
    pass


def register_screen_at_standalog_server(screen_id,screen_name, domain,auth):
    url = f'{domain}/api/register-screen/'
    data = {'screen_id': screen_id, 'screen_name': screen_name}
    # request.META.get("HTTP_AUTHORIZATION") = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2Mjc4MjY3LCJpYXQiOjE3MTYxOTE4NjcsImp0aSI6IjRkZWRkMWFkMDhiZDQ1NTE4MWY5ZDkwNWY5ODkyNTVhIiwidXNlcl9pZCI6Mn0.McICSwQLVtwufci7hUsM5oGCTWFBvc8pl0Cl8yBKNGc'
    headers = {'Authorization':auth}
    print(url)
    response = requests.post(url, data=data, headers=headers)
    
    resp = response.json()
    print(resp)
    return resp