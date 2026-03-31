from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api import views

app_name = "api"

urlpatterns = [
    path('media_items/', views.MediaItemsView.as_view()),
    path('media_items/<int:id>/', views.SingleMediaItemView.as_view()),
]