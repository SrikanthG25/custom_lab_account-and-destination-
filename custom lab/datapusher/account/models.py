import uuid
from django.db import models

HTTP_METHOD_CHOICES = [('GET', 'GET'),('POST', 'POST'),('PUT', 'PUT'),('DELETE', 'DELETE'),]

class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    account_name = models.CharField(max_length=125)
    app_secret_token = models.CharField(max_length=125, editable=False)
    website = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "account_data"
    def __str__(self):
        return self.account_name

class Destination( models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(max_length=20, choices=HTTP_METHOD_CHOICES)
    headers = models.JSONField()

    class Meta:
        db_table = "destination_data"
    