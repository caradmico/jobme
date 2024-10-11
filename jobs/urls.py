from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('fetch/', views.fetch_jobs, name='fetch_jobs'),  # Ensure this path exists
]
