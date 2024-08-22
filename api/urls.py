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
    
    path('plots/', views.CreateOrUpdatePlotView.as_view(), name='create-or-update-plot'),
    path('plots-list/', views.LatestPlotView.as_view(), name='plot-by-section'),
    
    path('kalag-list/', views.AllKalagListsAPIView.as_view(), name='kalag-list'),
    path('masterlist-create/', views.MasterListCreateView.as_view(), name='masterlist-create'),
    path('masterlist/', views.MasterListView.as_view(), name='masterlist-list'),
    path('masterlist/<int:pk>/delete/', views.MasterListDeleteAPIView.as_view(), name='masterlist-delete'),
]