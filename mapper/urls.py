from django.urls import path
from . import views # import the views file 
from .views import MapReportsView

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('contact/', views.contact, name='contact'),
    path('instructions/', views.instructions, name='instructions'),
    path('map/', MapReportsView.as_view(), name='map-reports'),
    path('reports/', views.ReportList.as_view(), name='reports-list'),
    path('reports/<int:pk>/', views.report_detail, name='report-detail'),
    path('reports/<int:pk>/edit/', views.edit_report, name='edit-report'),
    path('reports/<int:pk>/delete/', views.delete_report, name='delete-report'),
    path('os_tiles/<int:z>/<int:x>/<int:y>/', views.get_os_map_tiles, name='tile-proxy'),
    path('google_satellite_tiles/<int:z>/<int:x>/<int:y>/', views.get_google_satellite_tiles, name='google-satellite-tiles'),
    path('reports/<int:pk>/update-location/', views.update_report_location, name='update-report-location'),
    path('email-confirmation-success/', views.email_confirmation_success, name='email-confirmation-success'),
]