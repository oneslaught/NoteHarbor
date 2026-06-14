from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('notes/<int:pk>/', views.note_detail_view, name='note_detail'),
    path('explore/', views.explore_view, name='explore'),
    path('notes/<int:pk>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('notes/<int:pk>/fork/', views.fork_note_view, name='fork_note'),
    path('my-forks/', views.my_forks_view, name='my_forks'),
    path('my-notes/', views.my_notes_view, name='my_notes'),
    path('notes/create/', views.create_note_view, name='create_note'),
    path('notes/<int:pk>/edit/', views.edit_note_view, name='edit_note'),
    path('notes/<int:pk>/rate/', views.rate_note_view, name='rate_note'),
    path('notes/<int:pk>/delete/', views.delete_note_view, name='delete_note'),
]