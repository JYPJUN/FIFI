from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=30, null=True, blank=True, unique=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    profile_img = models.ImageField(upload_to='profile_image/', default='profile_image/basic.png')
    birth_date = models.DateField(blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_email, user_field, user_username
        data = form.cleaned_data
        username = data.get("username")
        nickname = data.get("nickname")
        name = data.get("name")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        profile_img = data.get("profile_img")
        birth_date = data.get('birth_date')
        income = data.get("income")
        
        user_email(user, email)
        user_username(user, username)
        
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if name:
            user_field(user, "name", name)
        if income:
            user_field(user, "income", income)
        if profile_img:
            user.profile_img = profile_img
        if birth_date:
            user.birth_date = birth_date
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user