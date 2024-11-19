from rest_framework import generics, permissions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import ImagesMemoriesSerializer, UserSerializer, KalagSerializer, PlotSerializer, MasterListSerializer, MasterListViewSerializer, MemoriesSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Kalag, Plot, MasterList, Memories, ImagesMemories
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
import qrcode
from io import BytesIO
import base64
from django.http import HttpResponse
from django.core.files.base import ContentFile
from rest_framework.exceptions import NotFound
import logging
from rest_framework.parsers import MultiPartParser, FormParser
logger = logging.getLogger(__name__)

class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]  # Optionally, add permissions
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
    permission_classes = [AllowAny]  # Optionally, add permissions
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
    permission_classes = [AllowAny]  # Optionally, add permissions
    queryset = Kalag.objects.all()
    serializer_class = KalagSerializer
    
    
class MasterListCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Optionally, add permissions
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
    permission_classes = [AllowAny]  # Optionally, add permissions
    queryset = MasterList.objects.all()
    serializer_class = MasterListViewSerializer
    
class MasterListDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [AllowAny]  # Optionally, add permissions
    queryset = MasterList.objects.all()
    serializer_class = MasterListViewSerializer

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MasterList.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
class KalagUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]  # Optionally, add permissions
    queryset = Kalag.objects.all()
    serializer_class = KalagSerializer
    lookup_field = 'id'
    
class KalagDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]  # Optionally, add permissions
    queryset = Kalag.objects.all()
    serializer_class = KalagSerializer
    lookup_field = 'id'  # Use 'id' as the lookup field
    
class CreateMemoriesView(APIView):
    permission_classes = [AllowAny]  # Optionally, add permissions
    def post(self, request, kalag_id):
        # Get the Kalag object using the kalag_id from the URL
        kalag = get_object_or_404(Kalag, id=kalag_id)
        
        # Combine kalag with the incoming data
        data = request.data.copy()
        data['kalag'] = kalag.id
        
        # Serialize the data
        serializer = MemoriesSerializer(data=data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the serializer, which creates a Memories instance
            serializer.save()
            # Return a successful response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return a response with errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    
    
    
    
    
class UpdateKalagQR(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        try:
            kalag = Kalag.objects.get(pk=pk)
        except Kalag.DoesNotExist:
            return Response({"error": "Kalag not found."}, status=status.HTTP_404_NOT_FOUND)

        # Generate QR code with Kalag data, including the id
        kalag_data = {
            'id': kalag.id,  # Add the id to the QR data
            'cemetery_section': kalag.cemetery_section,
            'name': kalag.name,
            'date_born': kalag.date_born,
            'date_died': kalag.date_died,
            'address': kalag.address,
            'grave_number': kalag.grave_number,
            'relative_name': kalag.relative_name,
            'relative_number': kalag.relative_number,
            'relative_address': kalag.relative_address,
            'relative_relation': kalag.relative_relation,
        }

        # Format kalag data into a string for QR code
        kalag_info = '\n'.join(f"{key}: {value}" for key, value in kalag_data.items())
        qr_image = qrcode.make(kalag_info)

        # Save QR code to BytesIO
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)

        # Save QR code to the model
        qr_filename = f'kalag_{pk}.png'
        kalag.qr.save(qr_filename, ContentFile(buffer.read()), save=True)

        # Encode QR code to base64 for API response
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Serialize the Kalag instance and add QR code to the response
        serializer = KalagSerializer(kalag)
        response_data = serializer.data
        response_data['qr'] = qr_code_base64  # Add base64 QR code to response
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    
    
    
    
class ScannedKalagQrView(APIView):
    """
    API View to fetch Kalag details using kalagId (parameter).
    """
    permission_classes = [AllowAny]
    
    def get(self, request, kalagId, *args, **kwargs):
        try:
            # Retrieve Kalag object by ID
            kalag = Kalag.objects.get(id=kalagId)
        except Kalag.DoesNotExist:
            # If Kalag not found, return a 404 error response
            return Response({"error": "Kalag not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize Kalag data
        serializer = KalagSerializer(kalag)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    

class AddUpdateMemoriesAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]  # Optionally, add permissions
    serializer_class = MemoriesSerializer

    def post(self, request, id):
        print("Received request data:", request.data)  # Print all request data
        print("Received request files:", request.FILES)  # Print all request files

        try:
            kalag_instance = Kalag.objects.get(id=id)
            print(f"Kalag instance found: {kalag_instance}")
        except Kalag.DoesNotExist:
            print(f"Kalag with id {id} not found.")
            raise NotFound(f"Kalag with id {id} not found.")

        # Check if a Memories instance for the given Kalag already exists
        memories_instance, created = Memories.objects.get_or_create(kalag=kalag_instance)
        print("Memories instance:", "Created new" if created else "Existing", memories_instance)

        # Serialize the data
        serializer = self.get_serializer(memories_instance, data=request.data, partial=True)

        # Validate the serializer before accessing validated_data
        if serializer.is_valid():
            print("Serializer data is valid.")

            # Check if a new profile_pic is provided
            if not request.FILES.get("profile_pic"):
                # If no new profile_pic is provided, keep the existing one
                serializer.validated_data['profile_pic'] = memories_instance.profile_pic

            # Save the memory
            serializer.save(kalag=kalag_instance)  # Explicitly set the kalag relation
            message = "Memory created" if created else "Memory updated"
            print("Memory saved successfully:", serializer.data)
            return Response({
                "message": message,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            print("Validation errors:", serializer.errors)  # Print validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class KalagMemoriesListAPIView(generics.ListAPIView):
    serializer_class = MemoriesSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        kalag_id = self.kwargs['id']
        
        # Check if Kalag with given ID exists
        try:
            kalag_instance = Kalag.objects.get(id=kalag_id)
            print(f"Kalag instance found: {kalag_instance}")
        except Kalag.DoesNotExist:
            print(f"Kalag with id {kalag_id} not found.")
            raise NotFound(f"Kalag with id {kalag_id} not found.")
        
        # Return Memories associated with the Kalag instance
        return Memories.objects.filter(kalag=kalag_instance)
    
    
    
    
class UploadBackgroundImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, kalagId, *args, **kwargs):
        try:
            kalag_instance = Kalag.objects.get(id=kalagId)
        except Kalag.DoesNotExist:
            return Response({"detail": "Kalag not found."}, status=status.HTTP_404_NOT_FOUND)

        # Add the kalag instance to the request data before serialization
        request.data['kalag'] = kalag_instance.id
        
        # Now use the serializer to validate and save
        serializer = ImagesMemoriesSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class KalagImagesListAPIView(APIView):
    permission_classes = [AllowAny]  # Optionally, add permissions
    def get(self, request, kalagId, *args, **kwargs):
        # Filter ImagesMemories entries by kalag_id
        images = ImagesMemories.objects.filter(kalag_id=kalagId)
        
        if not images.exists():
            return Response(
                {"detail": "No images found for this Kalag entry."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ImagesMemoriesSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteImagesMemoriesAPIView(APIView):
    permission_classes = [AllowAny]  # Optionally, add permissions

    def delete(self, request, *args, **kwargs):
        image_memory_id = kwargs.get('id')
        
        try:
            image_memory = ImagesMemories.objects.get(id=image_memory_id)
            image_memory.delete()
            return Response({"message": "Image memory deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ImagesMemories.DoesNotExist:
            return Response({"error": "Image memory not found."}, status=status.HTTP_404_NOT_FOUND)
        
class ListOfKalagView(generics.ListAPIView):
    queryset = Kalag.objects.all()
    serializer_class = KalagSerializer
    permission_classes = [AllowAny]  # Public access