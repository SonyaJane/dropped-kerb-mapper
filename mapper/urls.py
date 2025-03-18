from . import views # import the views file 
from django.urls import path

urlpatterns = [
    path('', views.ReportList.as_view(), name='home'), # URL pattern for the home page
]