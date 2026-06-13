from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('notes/<int:pk>/', views.note_detail_view, name='note_detail'),
    path('notes/<int:pk>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('favorites/', views.favorites_view, name='favorites'),
]