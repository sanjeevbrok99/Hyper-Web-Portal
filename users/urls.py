# users/urls.py
from django.urls import path
from .views import   UserListCreateView, UserRetrieveByEmailView, UserRetrieveUpdateDestroyView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('users/by-email/', UserRetrieveByEmailView.as_view(), name='user-retrieve-by-email'),

 
]
