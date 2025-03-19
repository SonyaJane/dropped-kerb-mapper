from . import views # import the views file 
from django.urls import path

urlpatterns = [
    path('reports', views.ReportList.as_view(), name='reports-list'),
]