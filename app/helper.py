import re , jwt , random , json
import requests
from employee_job_tracking.models import CustomUser as User
from .settings import SECRET_KEY
from datetime import datetime, timedelta , date
ACCESS_TOKEN_EXPIRY = timedelta(days=30) 



def user_validation(accessToken):
    '''
        here User validation by accesstoken
    '''
    if not accessToken:
        return {"message": "Invalid credential"}
    try:
        decoded_token = jwt.decode(accessToken, SECRET_KEY, algorithms=['HS256'])
        email = decoded_token.get("user_email")
        if not email:
            return {"message": "Token contained no recognizable user identification"}
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return {"message": "User does not exist"}
        return {"message": "User present", "user_obj": user}
    except jwt.ExpiredSignatureError:
        return {'message': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'}



def generate_access_token(user):
    """
    Generate a new access token
    """
    payload = {
        'user_email': user.email,
        'user_id':user.id,
        'exp': datetime.utcnow() + ACCESS_TOKEN_EXPIRY,  # Expiry time for access token
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')