# encoding: utf-8

from rest_framework import serializers
from api.models import UserRequestHistory
from django.contrib.auth.models import User



class UserRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequestHistory
        exclude = ['id', 'user']

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    username = serializers.CharField(max_length=64)
    password = serializers.CharField()
    email = serializers.EmailField()
    is_admin = serializers.BooleanField(default=False)

    def save(self):
        if self.validated_data['is_admin'] == True:
            user = User.objects.create_superuser(self.validated_data['username'], self.validated_data['email'], self.validated_data['password'])
        else:
            user = User.objects.create_user(self.validated_data['username'], self.validated_data['email'], self.validated_data['password'])

        user.save()

        return user