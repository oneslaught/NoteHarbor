from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('notes/<int:pk>/', views.note_detail_view, name='note_detail'),
    path('notes/<int:pk>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('notes/<int:pk>/fork/', views.fork_note_view, name='fork_note'),
    path('my-forks/', views.my_forks_view, name='my_forks'),
    path('notes/<int:pk>/delete/', views.delete_note_view, name='delete_note'),
]