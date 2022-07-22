# encoding: utf-8

from rest_framework import serializers

from api.models import UserRequestHistory


class UserRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequestHistory
        exclude = ['id', 'user']
        extra_kwargs = {'date': {'write_only':True}}

