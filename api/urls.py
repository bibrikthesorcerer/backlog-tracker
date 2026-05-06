from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api import views

app_name = "api"

urlpatterns = [
    path('media_items/', views.MediaItemsView.as_view(), name='media_items'),
    path('media_items/<int:id>/', views.SingleMediaItemView.as_view(), name='single_media_item'),
    path('media_items/<int:id>/start/', views.MediaItemLifecycleView.as_view(action="start"), name='start_media_item'),
    path('media_items/<int:id>/complete/', views.MediaItemLifecycleView.as_view(action="complete"), name='complete_media_item'),
    path('media_items/<int:id>/drop/', views.MediaItemLifecycleView.as_view(action="drop"), name='drop_media_item'),
    path('tags/', views.TagsView.as_view(), name='tags'),
    path('tags/<int:id>/', views.SingleTagView.as_view(), name='single_tag'),
    
    path('queue/', views.MediaItemQueueView.as_view(), name='queue'),
    
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name=f'{app_name}:schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name=f'{app_name}:schema'), name='redoc'),
]