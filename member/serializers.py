from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
    
class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'nickname', 'university']

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=100)
    university = serializers.CharField(max_length=50)
    
    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'university': self.validated_data.get('university', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.username = self.cleaned_data.get('username')
        user.nickname = self.cleaned_data.get('nickname')
        user.university = self.cleaned_data.get('university')
        user.save()
        adapter.save_user(request, user, self)
        return user
    
    
class LoginRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True, max_length=20)
    password = serializers.CharField(required=True, write_only=True, max_length=50)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'nickname', 'university']