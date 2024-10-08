from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token  

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),  
    path('admin/', admin.site.urls),              
    path('api/', include('myapp.urls')),          
]
