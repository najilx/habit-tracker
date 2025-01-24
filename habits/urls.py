from django.urls import path
from . import views
from .views import LeaderboardView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('add/', views.add_habit, name='add_habit'),
    path('progress/<int:habit_id>/', views.mark_progress, name='mark_progress'),
    path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('edit/<int:habit_id>/', views.edit_habit, name='edit_habit'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]