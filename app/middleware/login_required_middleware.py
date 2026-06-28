from django.shortcuts import redirect, HttpResponseRedirect
# from django.urls import reverse
# from django.conf import settings
# import re
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.exempt_urls = [
#             reverse('login'),  # Exempt login page
#             reverse('token_obtain_pair'),  # JWT login endpoint
#             reverse('token_refresh'),      # JWT refresh endpoint
#         ]

#     def __call__(self, request):
#         # Allow access to static and media files
#         if request.path.startswith(settings.STATIC_URL) or request.path.startswith(settings.MEDIA_URL):
#             return self.get_response(request)
#         auth = JWTAuthentication()
#         try:
#             user_auth_tuple = auth.authenticate(request)
#             if user_auth_tuple:
#                 request.user, _ = user_auth_tuple
#         except AuthenticationFailed:
#             return JsonResponse({'detail': 'Invalid or expired token'}, status=401)

#         # Redirect to login if no valid JWT or user not authenticated
#         if not request.user or not request.user.is_authenticated:
#             return JsonResponse({'detail': 'Authentication required'}, status=401)

#         return self.get_response(request)


# from django.shortcuts import render ,redirect

from app.helper import user_validation

def auth_middleware(get_response):
    def middleware(request):
        return_url = request.META['PATH_INFO']
        if not request.session.get('customer'):
            return redirect(f'/login?return_url={return_url}')
        response = get_response(request)
        return response
    return middleware

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('login'),
            reverse('token_obtain_pair'),
            reverse('token_refresh'),
        ]

    def __call__(self, request):
        if request.path in self.exempt_urls:
            return self.get_response(request)

        # Allow access to static/media files
        if request.path.startswith(settings.STATIC_URL) or request.path.startswith(settings.MEDIA_URL):
            return self.get_response(request)

        access_token = request.COOKIES.get("access")  # or from Authorization header, or session
        result = user_validation(access_token)

        if result.get("message") != "User present":
            # Redirect to login if this is a browser or API request handler
            if request.path.startswith("/api/"):
                return JsonResponse({'detail': result['message']}, status=401)
            else:
                return HttpResponseRedirect(reverse('login'))

        # Set the user object manually to request
        request.user = result["user_obj"]
        return self.get_response(request)