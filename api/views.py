from rest_framework import generics, permissions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserSerializer, KalagSerializer, PlotSerializer, MasterListSerializer, MasterListViewSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Kalag, Plot, MasterList
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    


class KalagCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = KalagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class KalagListView(generics.ListAPIView):
    queryset = Kalag.objects.all()
    serializer_class = KalagSerializer
    filter_backends = [SearchFilter]
    search_fields = ['cemetery_section']
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        cemetery_section = self.request.query_params.get('cemetery_section')
        if cemetery_section:
            queryset = queryset.filter(cemetery_section=cemetery_section)
        return queryset
    
class KalagDeleteView(generics.DestroyAPIView):
    queryset = Kalag.objects.all()
    serializer_class = KalagSerializer
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        # Retrieve the Kalag object by ID
        try:
            kalag = self.get_object()
            kalag.delete()
            return Response({"message": "Kalag record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Kalag.DoesNotExist:
            return Response({"error": "Kalag record not found."}, status=status.HTTP_404_NOT_FOUND)


class CreateOrUpdatePlotView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        cemetery_section = request.data.get('cemetery_section')
        name = request.data.get('name')
        number = request.data.get('number')

        if not cemetery_section or not name or number is None:
            return Response({'error': 'cemetery_section, name, and number are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_plot = Plot.objects.filter(cemetery_section=cemetery_section, name=name).first()

        if existing_plot:
            existing_plot.number = number
            existing_plot.save()
            serializer = PlotSerializer(existing_plot)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = PlotSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LatestPlotView(generics.ListAPIView):
    serializer_class = PlotSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        cemetery_section = self.request.query_params.get('cemetery_section', None)
        if cemetery_section:
            # Adjust the ordering based on your needs (e.g., latest date or other field)
            queryset = Plot.objects.filter(cemetery_section=cemetery_section).order_by('-id')[:1]
        else:
            queryset = Plot.objects.none()
        return queryset
    

class AllKalagListsAPIView(generics.ListAPIView):
    queryset = Kalag.objects.all()
    serializer_class = KalagSerializer
    
    
class MasterListCreateView(generics.CreateAPIView):
    queryset = MasterList.objects.all()
    serializer_class = MasterListSerializer  
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        print("Request data:", self.request.data)  # Print the request data
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        kalag_id = self.request.data.get('kalag')
        if MasterList.objects.filter(kalag_id=kalag_id).exists():
            raise ValidationError("A MasterList entry for this Deceased Person already exists; duplication is not allowed.")
        
        # Save the serializer if everything is correct
        serializer.save()

    def post(self, request, *args, **kwargs):
        kalag_id = request.data.get('kalag')
        if MasterList.objects.filter(kalag_id=kalag_id).exists():
            return Response(
                {"error": "A MasterList entry for this Deceased Person already exists; duplication is not allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().post(request, *args, **kwargs)
class MasterListView(generics.ListAPIView):
    queryset = MasterList.objects.all()
    serializer_class = MasterListViewSerializer
    
class MasterListDeleteAPIView(generics.DestroyAPIView):
    queryset = MasterList.objects.all()
    serializer_class = MasterListViewSerializer

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MasterList.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)