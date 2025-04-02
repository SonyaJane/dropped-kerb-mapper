from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from .forms import ReportForm
from .models import Report
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
import os
import requests
from django.http import HttpResponse, Http404
import time
import json
from django.core.cache import cache


def home(request):
    """
    Render the home page
    """
    return render(request, 'mapper/home.html')
 
 
class ReportList(generic.ListView):
   template_name = "mapper/reports.html"
   paginate_by = 24
   
   def get_queryset(self):
        """
        Return reports created by the logged-in user.
        If the user is a superuser, return all reports.
        """
        if self.request.user.is_superuser:
            # Superuser sees all reports
            return Report.objects.all()
        else:
            # Regular users see only their own reports
            return Report.objects.filter(user=self.request.user)
   
   
def report_detail(request, pk):
   """
   Retrieves a single report from the database and displays it on the page.
   """
   queryset = Report.objects.all()
   report = get_object_or_404(queryset, pk=pk)
   return render(request, "mapper/report_detail.html", {"report": report})


def create_report(request):
    if request.method == 'POST':
        report_form = ReportForm(request.POST, request.FILES)
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, 'Report created successfully!')
            return redirect('reports-list')  # Redirect to the reports list page
    else:
        form = ReportForm()
    return render(request, 'mapper/create_report.html', {'form': form})


class ReportEditView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'mapper/edit_report.html'

    def get_success_url(self):
        # Redirect to the report detail page after editing
        return reverse_lazy('report-detail', kwargs={'pk': self.object.pk})
    
    
def map_reports(request):
    """
    Create a map with all dropped kerb reports.
    """
    reports = Report.objects.all()  # Fetch all reports
    reports_data = [
        {
            'id': report.id,
            'latitude': report.latitude,
            'longitude': report.longitude,
            'classification': report.classification,
            'reasons': report.get_reasons_display(),
            'comments': report.comments,
        }
        for report in reports
    ]
    return render(request, 'mapper/map_reports.html', {'reports': reports_data})


def get_os_map_tiles(request, z, x, y):
    """
    Proxy view to fetch map tiles securely using the API key.
    """
    # Limit the maximum zoom level to 20
    MAX_ZOOM = 20
    if z > MAX_ZOOM:
        z = min(z, MAX_ZOOM)
    
    api_key = os.environ.get("OS_MAPS_API_KEY")

    # Construct the Ordnance Survey tile URL
    tile_url = f"https://api.os.uk/maps/raster/v1/zxy/Light_3857/{z}/{x}/{y}.png?key={api_key}"
    
    # Make a GET request to fetch the tile image
    response = requests.get(tile_url)
    
    
    if response.status_code == 200:
        # Return the image content with appropriate content-type
        return HttpResponse(response.content, content_type="image/png")
    else:
        # Return a 404 response with caching headers
        return HttpResponse(
            status=404,
            headers={
                "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
            }
        )


def get_google_session_token():
    # Try to retrieve the token data from the cache
    token_data = cache.get('google_tile_session_token')
    if token_data:
        return token_data.get('session')
    
    # If no token is cached, request a new one
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    # Set up the createSession endpoint URL
    create_session_url = f"https://tile.googleapis.com/v1/createSession?key={api_key}"
    
    # Define the required payload
    payload = {
        "mapType": "satellite",
        "language": "en-GB",
        "region": "UK"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    # Request the session token
    response = requests.post(create_session_url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        session_token = data.get("session")
        expiry = data.get("expiry")
        # Calculate the remaining time until expiry (expiry is seconds since the epoch)
        now = int(time.time())
        remaining = int(expiry) - now if expiry and int(expiry) > now else 14 * 24 * 3600
        # Cache the full token data (you might want to cache the expiry as well)
        cache.set('google_tile_session_token', data, timeout=remaining)
        return session_token
    else:
        raise Exception("Failed to obtain session token: " + response.text)



def get_google_satellite_tiles(request, z, x, y):
    """
    Proxy view to fetch Google Satellite map tiles.
    """
    # Check if the session token is cached, if not, create a new one
    try:
        session_token = get_google_session_token()
    except Exception as e:
        raise Http404("Could not obtain session token: " + str(e))
    
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    # Construct the Google Maps tile URL
    tile_url = f"https://tile.googleapis.com/v1/2dtiles/{z}/{x}/{y}?session={session_token}&key={api_key}"
    
    # Make a GET request to fetch the tile image
    response = requests.get(tile_url)
    
    if response.status_code == 200:
        # Return the image content with appropriate content-type
        return HttpResponse(response.content, content_type="image/png")
    elif response.status_code == 404: # Tile not found at requested zoom level
        # Return a 404 response with caching headers
        return HttpResponse(
            status=404,
            headers={
                "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
            }
        )
    else:
        raise Http404("Tile not found.")