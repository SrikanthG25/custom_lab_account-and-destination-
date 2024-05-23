from django.db import models

class LoginUser(models.Model):
    Username = models.CharField(max_length=32)
    Password = models.CharField(max_length=230)
    is_admin = models.BooleanField(default=False)
    created_by = models.CharField(max_length=32,null=True,blank=True)
    created_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=32,null=True,blank=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "loginuser"