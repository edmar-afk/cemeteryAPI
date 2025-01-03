from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    path('user/', views.UserDetailView.as_view(), name='user_detail'),
    
    
    path('kalags/create/', views.KalagCreateView.as_view(), name='kalag-create'),
    path('kalag/', views.KalagListView.as_view(), name='kalag-list'),
    path('kalag/<int:pk>/delete/', views.KalagDeleteView.as_view(), name='kalag-delete'),
    path('kalag/<int:id>/update/', views.KalagUpdateAPIView.as_view(), name='kalag-update'),
    path('kalags/<int:id>/', views.KalagDetailAPIView.as_view(), name='kalag-detail'),
    path('kalags/', views.ListOfKalagView.as_view(), name='list-of-kalags'),
    
    path('plots/', views.CreateOrUpdatePlotView.as_view(), name='create-or-update-plot'),
    path('plots-list/', views.LatestPlotView.as_view(), name='plot-by-section'),
    
    path('kalag-list/', views.AllKalagListsAPIView.as_view(), name='kalag-list'),
    path('masterlist-create/', views.MasterListCreateView.as_view(), name='masterlist-create'),
    path('masterlist/', views.MasterListView.as_view(), name='masterlist-list'),
    path('masterlist/<int:pk>/delete/', views.MasterListDeleteAPIView.as_view(), name='masterlist-delete'),
    
    path('memories/create/<int:kalag_id>/', views.CreateMemoriesView.as_view(), name='create-memories'),
    
    path('kalag/<int:pk>/update-qr/', views.UpdateKalagQR.as_view(), name='update_kalag_qr'),
    
    path('scanned-kalag/<int:kalagId>/', views.ScannedKalagQrView.as_view(), name='scanned-kalag-detail'),
    
    path('kalags/<int:id>/memories/', views.AddUpdateMemoriesAPIView.as_view(), name='add_update_memories'),
    path('kalags/<int:id>/memories-list/', views.KalagMemoriesListAPIView.as_view(), name='kalag-memories-list'),
    
    path('upload-background-image/<int:kalagId>/', views.UploadBackgroundImageView.as_view(), name='upload-background-image'),
    path('kalags/<int:kalagId>/images/', views.KalagImagesListAPIView.as_view(), name='kalag-images-list'),
    path('imagesmemories/<int:id>/delete/', views.DeleteImagesMemoriesAPIView.as_view(), name='delete-imagesmemories'),
]