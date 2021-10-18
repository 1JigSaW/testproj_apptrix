from django.contrib import admin
from django.urls import path, include
from meeting_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/create', views.RegisterView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]
