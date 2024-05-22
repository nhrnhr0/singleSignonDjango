from django.shortcuts import render
import json
from django.http import JsonResponse
import uuid
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
import requests

from django.shortcuts import redirect


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
            return JsonResponse({'detail': f'Screen {screen_id} already registered'}, status=400)
        
        
        # Register the screen (create a user with viwer permission)
        username = f'screen_{screen_id}'
        password = str(uuid.uuid4())
        
        screen = User.objects.create_user(username=username, password=password)
        screen.organization = org
        screen.type = User.TYPE_SCREEN
        screen.name = screen_name
        screen.save()
        
        register_screen_at_standalog_server(screen_id,screen_name, org.domain, request.META.get("HTTP_AUTHORIZATION"))
        
        print(f'Screen {screen_id} registered to {user.username}')
        return JsonResponse({'detail': f'Screen {screen_id} registered to {user.username}'})
    return render(request, 'register_screen.html')

@api_view(['POST'])
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
        
        return JsonResponse({'status': 'success', 'message': f'Credentials sent to screen {screen_id}', 'password': new_pass, 'username': screen.username}, status=200)
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_standalog_server_url(request):
    domain = request.user.organization.domain
    return JsonResponse({'url': domain})
    pass



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return JsonResponse({'username': user.username, 'domain': user.organization.domain, 'type': user.user_type})
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