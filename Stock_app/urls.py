from django.urls import path
from . import views

urlpatterns = [
    path('abc/', views.abc, name="abc"),
    path('register/', views.registerapi.as_view(), name='register'),
    path('login/', views.loginapi.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('calculate_investment/', views.calculate_investment, name='calculate_investment'),
    path('hubs/', views.HubListCreateAPIView.as_view(), name='hub-list-create'),
    path('hubs/<int:pk>/', views.HubRetrieveUpdateDestroyAPIView.as_view(), name='hub-detail'),
    path('machines/', views.MachineListCreateAPIView.as_view(), name='machine-list-create'),
    path('machines/<int:pk>/', views.MachineRetrieveUpdateDestroyAPIView.as_view(), name='machine-detail'),
    path('machineview/<int:hub_id>/', views.machineview, name='machineview'),
    path('technicians/', views.listalltechnicians, name='techniciannames'),
]
