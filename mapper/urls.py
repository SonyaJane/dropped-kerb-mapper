from . import views # import the views file 
from django.urls import path
from .views import ReportEditView

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    # path('create-report/', views.create_report, name='create-report'),
    path('map/', views.map_reports, name='map-reports'),
    path('reports', views.ReportList.as_view(), name='reports-list'),
    path('reports/<int:pk>/', views.report_detail, name='report-detail'),
    path('reports/<int:pk>/edit/', ReportEditView.as_view(), name='edit-report'),
    path('os_tiles/<int:z>/<int:x>/<int:y>/', views.get_os_map_tiles, name='tile-proxy'),
    path('google_satellite_tiles/<int:z>/<int:x>/<int:y>/', views.get_google_satellite_tiles, name='google-satellite-tiles'),
]