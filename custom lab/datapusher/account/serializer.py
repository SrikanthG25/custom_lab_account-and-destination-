from rest_framework import serializers
from django.db import models
from .models import *

class AccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={'required': 'Please provide your email.'})
    account_id = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    account_name = serializers.CharField(required=True, max_length=125, error_messages={'required': 'Please provide your account name.'})
    app_secret_token = serializers.CharField(max_length=125, read_only=True)
    website = serializers.URLField(required=False, allow_null=True)
