from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User



User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают!")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)