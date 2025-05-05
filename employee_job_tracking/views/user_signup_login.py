from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from employee_job_tracking.models import CustomUser as User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password

class UserSignupLoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        full_name = request.data.get('full_name')
        role = request.data.get('role') 
        if not all ([email, password , full_name, role]):
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        encoded_password = make_password(password)
        User.objects.create(email=email, password=encoded_password , full_name=full_name, role=role)
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not all([email, password]):
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_obj = User.objects.filter(email=email).first()
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if check_password(password, user_obj.password):
                refresh = RefreshToken()
                refresh.payload['user_email'] = user_obj.email
                refresh.payload['user_id'] = user_obj.id 
                User.objects.filter(phone_number = email).update(token = [{"accessToken": f"{refresh.access_token}" , "refreshToken":f"{refresh}"}])
                return Response({"message":"user auth success",'access': str(refresh.access_token), 'refresh': str(refresh) , "status":"200"}, status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
