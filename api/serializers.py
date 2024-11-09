from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Kalag, Plot, MasterList, Memories, ImagesMemories, VideosMemories

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class KalagSerializer(serializers.ModelSerializer):
    qr = serializers.CharField(allow_blank=True, required=False)  # Allow qr to be blank and not required

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
            'relative_relation',
            'qr'  # qr should not be required
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
    kalag = serializers.PrimaryKeyRelatedField(queryset=Kalag.objects.all())  # Use ID instead of nested data

    class Meta:
        model = Memories
        fields = [
            'id',
            'kalag',
            'speech',
            'profile_pic',
        ]
class ImagesMemoriesSerializer(serializers.ModelSerializer):
    kalag = serializers.PrimaryKeyRelatedField(queryset=Kalag.objects.all())  # Accept kalag ID

    class Meta:
        model = ImagesMemories
        fields = ['id', 'kalag', 'background_image']

class VideosMemoriesSerializer(serializers.ModelSerializer):
    kalag = KalagSerializer()  # Use KalagSerializer for the kalag field

    class Meta:
        model = VideosMemories
        fields = ['id', 'kalag', 'video']