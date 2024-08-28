from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Kalag, Plot, MasterList, Memories

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class KalagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kalag
        fields = [
            'id', 
            'cemetery_section', 
            'name', 
            'date_born', 
            'date_died', 
            'address',
            'grave_number',
            'relative_name', 
            'relative_number', 
            'relative_address', 
            'relative_relation'
        ]



class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = ['id', 'cemetery_section', 'name', 'number']
        

        
class MasterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterList
        fields = ['kalag', 'grave_level', 'amount', 'year', 'status']  # Exclude 'date_registered' if it's auto-generated

    def validate(self, data):
        # Add custom validation if necessary
        if 'kalag' not in data:
            raise serializers.ValidationError({"kalag": "This field is required."})
        return data
    
    
class MasterListViewSerializer(serializers.ModelSerializer):
    kalag = KalagSerializer()
    class Meta:
        model = MasterList
        fields = ['id', 'kalag', 'grave_level', 'amount', 'year', 'date_registered', 'status']
        
        
class MemoriesSerializer(serializers.ModelSerializer):
    kalag = KalagSerializer()  # Use KalagSerializer for the kalag field

    class Meta:
        model = Memories
        fields = [
            'id',
            'kalag',
            'speech',
            'background_image',
            'profile_pic',
            'qr',
            'video'
        ]