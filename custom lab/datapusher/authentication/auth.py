from django.contrib.auth.models import AnonymousUser
from authentication.models import LoginUser
import logging
from rest_framework  import exceptions
from cryptography.fernet import Fernet
from django.conf import settings
from rest_framework.authentication import BaseAuthentication,get_authorization_header
from rest_framework.permissions import BasePermission
import jwt
import json

logger = logging.getLogger(__name__)


def decrypt_token(data):
    cipher_suite = Fernet(settings.TOKEN_SECRET_KEY)
    decrypted_data = cipher_suite.decrypt(data.encode())
    return decrypted_data.decode()

class JWTAuthentication(BaseAuthentication):
    
    model = None
    def get_model(self):
        
        return LoginUser
    
    def authenticate(self, request):
        
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg ="Invalid token header.No credentials provided"
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) > 2:
            msg = "Invalid token header"
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == 'null':
                msg = "Null token not allowed"
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = "Invalid token header.Token header should be valid"
            raise exceptions.AuthenticationFailed(msg)
        
        user, token, identifier = self.authenticate_credentials(token)
        if identifier:
            request.account_id = identifier.get("account_id")
            request.is_admin = identifier.get("is_admin")
            request.user_id = identifier.get("user_id")
        else:
            return None
        return(user,token)

    def authenticate_credentials(self,token):
        model = self.get_model()
        try:
            payload = jwt.decode(token,algorithms=['RS256'])
            
            payload_data = payload.get('data')
            
            if not payload:
                logger.info('Token has no data')
                raise exceptions.AuthenticationFailed('Invalid Token')
            
            token_data = json.loads(decrypt_token(payload_data))
            user_id = token_data.get('user_id')
           
            user = model.objects.get(id=user_id)
            
            if token_data.get('account_id'):
                user_id = token_data.get("account_id")
            if token_data.get('is_admin'):
                is_admin = token_data.get("is_admin")
            if token_data.get(user_id):
                user_id = token_data.get("user_id")
                return (user,token,{"account_id":user_id,"is_admin" : is_admin,"user_id" : user_id})
            return (None,None,None)
        
        except LoginUser.DoesNotExist as le:
            logger.exception('Exception {}',format(le.args))
            raise exceptions.AuthenticationFailed("You are not authorized to perform this operation")
        
        except jwt.ExpiredSignatureError as je:
            logger.exception('Exception {}',format(je.args))
            raise exceptions.AuthenticationFailed("Token is expired")

        except jwt.DecodeError or jwt.InvalidTokenError as de:
            logger.exception("JWT Error")
            raise exceptions.AuthenticationFailed("Invalid Token")

    def authenticate_header(self, request):
        return 'Token'
class ISAuthenticated(BasePermission):
     def has_permission(self, request, view):
         if request.user:
             if not isinstance(request.user,AnonymousUser):
                 return True
         return False

