from rest_framework import serializers
from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=30
    )
    birth_date = serializers.DateField(
        required=True,
    )
    nickname = serializers.CharField(max_length=30, required=False, allow_blank=True)
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=30
    )
    email = serializers.EmailField(required=False)
    income = serializers.IntegerField(required=False)

    def get_cleaned_data(self):
        cleaned_data = {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'name': self.validated_data.get('name', ''),
            'email': self.validated_data.get('email', ''),
            'birth_date': self.validated_data.get('birth_date', ''),
            'profile_img': self.validated_data.get('profile_img', ''),
            'income': self.validated_data.get('income', ''),
        }
        return cleaned_data
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = UserModel
        fields = (
            'pk', 'username', 'email', 'first_name', 'last_name',
            'nickname', 'birth_date', 'profile_img', 'name', 'income',
        )
        read_only_fields = ('email', 'birth_date', )