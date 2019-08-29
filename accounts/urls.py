from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.update_profile, name="profile"),
]

app_name = 'accounts'
