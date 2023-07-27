# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include the URLs from the 'users' app
    path('api/', include('users.urls')),
]
