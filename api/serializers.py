from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Kalag, Plot

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class KalagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kalag
        fields = ['id', 'cemetery_section', 'name', 'date_born', 'date_died', 'address']


class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = ['id', 'cemetery_section', 'name', 'number']