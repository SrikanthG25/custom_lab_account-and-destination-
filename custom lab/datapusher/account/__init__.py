from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account, Destination
import logging

logger = logging.getLogger(__name__)

class AccountAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get("email")
            account_id = data.get("account_id")
            account_name = data.get("account_name")
            app_secret_token = data.get("app_secret_token")
            website = data.get("website")

            if not email or not account_name or not app_secret_token:
                return Response({"status": 400, "message": "Email, account name, and app secret token are required"}, status=status.HTTP_400_BAD_REQUEST)
            
            existing_account = Account.objects.filter(app_secret_token=app_secret_token).exists()
            if existing_account:
                return Response({"status": 409, "message": "Account with this app secret token already exists"}, status=status.HTTP_409_CONFLICT)
            
            Account.objects.create(email=email, account_id=account_id, account_name=account_name, app_secret_token=app_secret_token, website=website)
            return Response({'status': 'success','message':'Successfully Added'} , status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong Please try again'} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, account_id):
        try:
            account = Account.objects.get(account_id=account_id)
            account_data = {
                "id": account.id,
                "email": account.email,
                "account_id": account.account_id,
                "account_name": account.account_name,
                "app_secret_token": account.app_secret_token,
                "website": account.website
            }
            return Response({"status": 200, "message": "Account successful data view",'data' : account_data}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"status": 404, "message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            data = request.data
            app_secret_token = request.headers.get('CL-XTOKEN')
            
            if not app_secret_token:
                return Response({"status": 401, "message": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            
            account = Account.objects.get(app_secret_token=app_secret_token)
            
            if not account:
                return Response({"status": 404, "message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
            
            account.account_name = data.get("account_name", account.account_name)
            account.email = data.get("email", account.email)
            account.website = data.get("website", account.website)
            
            account.save()
            return Response({'status': 'success','message':'Account updated successfully!'} , status=status.HTTP_200_OK)
            
        except Account.DoesNotExist:
            return Response({"status": 404, "message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DestinationAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            account_id = data.get("account_id")
            account = Account.objects.get(account_id=account_id)
            url = data.get("url")
            http_method = data.get("http_method")
            headers = data.get("headers")
            destination = Destination.objects.create(account=account, url=url, http_method=http_method, headers=headers)
            return Response({'status': 'success','message':'Successfully Added'} , status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"status": 404, "message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong Please try again'} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, destination_id):
        try:
            destination = Destination.objects.get(id=destination_id)
            destination_data = {
                "id": destination.id,
                "account_id": destination.account_id,
                "url": destination.url,
                "http_method": destination.http_method,
                "headers": destination.headers
            }
            return Response({"status": 200, "message": "Destination successful data view",'data' : destination_data}, status=status.HTTP_200_OK)
        except Destination.DoesNotExist:
            return Response({"status": 404, "message": "Destination not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, destination_id):
        try:
            destination = Destination.objects.get(id=destination_id)
            data = request.data
            destination.url = data.get("url", destination.url)
            destination.http_method = data.get("http_method", destination.http_method)
            destination.headers = data.get("headers", destination.headers)
            destination.save()
            return Response({'status': 'success','message':'Destination updated successfully!'} , status=status.HTTP_200_OK)
        except Destination.DoesNotExist:
            return Response({"status": 404, "message": "Destination not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, destination_id):
        try:
            Destination.objects.filter(id=destination_id).delete()
            return Response({'status': 'success','message':'Destination deleted successfully!'} , status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
