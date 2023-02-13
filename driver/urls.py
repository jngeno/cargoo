from django.urls import path, include
from .views import Dashboard, ServiceDetails

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('services/<int:pk>/', ServiceDetails.as_view(), name='service-details'),
    

]