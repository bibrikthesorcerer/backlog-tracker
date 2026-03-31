from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api import views

app_name = "api"

urlpatterns = [
    path('media_items/', views.MediaItemsView.as_view()),
    path('media_items/<int:id>/', views.SingleMediaItemView.as_view()),
    path('tags/', views.TagsView.as_view()),
    path('tags/<int:id>/', views.SingleTagView.as_view()),
    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name=f'{app_name}:schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name=f'{app_name}:schema'), name='redoc'),
]