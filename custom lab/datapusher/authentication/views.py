from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status

from account.models import Account
from .models import LoginUser
from rest_framework.response import Response
import datetime
import jwt
import json
from django.conf import settings
import logging
logger = logging.getLogger(__name__)
import bcrypt
from cryptography.fernet import Fernet
def encrypt_token_data(data):
    cipher_suite = Fernet(settings.TOKEN_SECRET_KEY)
    encoded_data = json.dumps(data).encode()
    encrypted_data = cipher_suite.encrypt(encoded_data)
    return encrypted_data.decode()

class AccoutnLoginView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def post(self,request):
        try:
            data = request.data
            user_name = data.get('Username')
            password = data.get('Password')

            user = LoginUser.objects.get(Username= user_name)
           

            if not user:
                return Response({ 'status' : 'fail','message' : 'Username does exist'},status= status.HTTP_400_BAD_REQUEST)
            
            if not bcrypt.checkpw(bytes(password, 'utf-8'), bytes(user.Password, 'utf-8')):
                return Response({'status': 'fail', 'message': 'Invalid username/password'},status=status.HTTP_400_BAD_REQUEST)

            token_data = {}
            account_id = Account.objects.get(login_user = user)
           
            if user.is_admin:
                token_data['is_admin'] = True
            token_data['account_id'] = account_id.account_id
            token_data['user_id'] = user.id 
            current_date = datetime.datetime.now()
            exp_time = current_date + datetime.timedelta(minutes= 1440 )
            encrypted_data = encrypt_token_data(token_data)
            token = jwt.encode({'data': encrypted_data,'exp' : exp_time},algorithm='RS256')
            response_data = {'token' : token}
            if user.is_admin:
                response_data['is_admin'] = True
                
            return Response({'status': 'success','message' : 'Login Successfull',"data":response_data})
            
        except Exception as e:
            logger.exception("Exception{}".format(e.args)) 
            return Response({'status': 'failed','message': 'something went wrong, Please try again'},status= status.HTTP_400_BAD_REQUEST)
