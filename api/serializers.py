from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cemetery, Kalag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class CemeterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cemetery
        fields = ['id', 'section', 'location', 'slots']

class KalagSerializer(serializers.ModelSerializer):
    cemetery_section = CemeterySerializer()
    user = UserSerializer()

    class Meta:
        model = Kalag
        fields = ['id', 'cemetery_section', 'name', 'date_born', 'date_died', 'address', 'user']
