# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import get_user_model
# import json
import requests , json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import redirect, render
from employee_job_tracking.models import CustomUser as User
GOOGLE_CLIENT_ID = "281758721391-qrnm7k6pb2s9r2meqltuvq1rj4eelc83.apps.googleusercontent.com"


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    token = request.data.get('token')
    print(token)
    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Step 1: Verify token with Google
    try:
        google_response = requests.get(
            f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'
        )
    except requests.RequestException:
        return Response({'error': 'Failed to contact Google'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    if google_response.status_code != 200:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    payload = google_response.json()
    if payload.get('aud') != GOOGLE_CLIENT_ID:
        return Response({'error': 'Invalid client ID'}, status=status.HTTP_400_BAD_REQUEST)

    # Step 2: Extract user info
    email = payload.get('email')
    name = payload.get('name')
    picture = payload.get('picture')

    if not email:
        return Response({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Step 3: Get or create user
    user, created = User.objects.get_or_create(
        email=email,
        full_name = name, 
        auth_provider ="google"
    )

    # Step 4: Generate your own token here (e.g., JWT or DRF token)
    return Response({
        'message': 'Login successful',
        'user': {
            'email': user.email,
            'name': user.full_name,
            'picture': picture,
        },
        'token': 'your_generated_token_here'  # Replace with real token logic
    }, status=status.HTTP_200_OK)




def google_login_new(request):
    # if request.method == 'POST':
    #     token = request.POST['idtoken']
    #     try:
    #         # Verify the ID token and get the user's Google account info
    #         info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
    #         print(info)
    #         # Use the info to authenticate the user in Django
    #         # You can store the user's information in the session or in your database
    #         # Redirect to the homepage or the next URL
    #         return redirect('/')
    #     except ValueError:
    #         # Invalid token
    #         pass
    context ={
            'GOOGLE_CLIENT_ID':GOOGLE_CLIENT_ID,
        }
    return render(request, 'login-1.html', context)
