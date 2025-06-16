from django.urls import path
from .views import (
    RegisterUserView, UserListView, UserDetailUpdateView, 
    api_root, logout_view, login_view, register_view, dashboard_view, update_user
)
from user_api import views

urlpatterns = [
    path('', api_root),  # API root
    path('api/register/', RegisterUserView.as_view(), name='api-register'),  # ✅ ADD THIS
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailUpdateView.as_view(), name='user-detail'),
    path('login/', login_view, name='login'),  # Frontend
    path('signup/', register_view, name='signup'),  # Frontend signup
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('delete-user/<int:pk>/', views.delete_user, name='delete-user'),
    path('update-user/<int:pk>/', views.update_user, name='update-user'),
]
