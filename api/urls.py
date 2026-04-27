from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api import views

app_name = "api"

urlpatterns = [
    path('media_items/', views.MediaItemsView.as_view(), name='media_items'),
    path('media_items/<int:id>/', views.SingleMediaItemView.as_view(), name='single_media_item'),
    path('tags/', views.TagsView.as_view(), name='tags'),
    path('tags/<int:id>/', views.SingleTagView.as_view(), name='single_tag'),
    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name=f'{app_name}:schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name=f'{app_name}:schema'), name='redoc'),
]