from django.urls import path
from . import views

app_name = 'api_user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='api_login'),
    path('manage/', views.ManagerUserView.as_view(), name='manage'),
]
