from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from .forms import ReportForm
from .models import Report
import os
import json
import requests
import time

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


def map_reports(request):
    if request.method =="POST":
        report_form = ReportForm(data=request.POST, files=request.FILES)
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.user = request.user
            report.save()
            messages.add_message(request, messages.SUCCESS, 'Report created successfully!')
            # return redirect('map-reports')  # Redirect to the reports list page
        if not report_form.is_valid():
            print("Report form errors:", report_form.errors)
    report_form = ReportForm()
        
    # Get all reports for the map view    
    reports = Report.objects.all()
    reports_data = [
        {
            'id': report.id,
            'latitude': report.latitude,
            'longitude': report.longitude,
            'place_name': report.place_name,
            'county': report.county.county if report.county else None,
            'classification': report.classification,
            'reasons': report.get_reasons_display(),
            'comments': report.comments,
            'photoUrl': report.photo.url if report.photo else None,
        }
        for report in reports
    ]
    return render(request, 'mapper/map_reports.html', {'form': report_form, 'reports': reports_data, 'is_map_reports': True})


def edit_report(request, pk):
    """
    Edit an existing report
    """
    # Get the report object based on the primary key (pk) from the URL
    queryset = Report.objects.all()
    report = get_object_or_404(queryset, pk=pk)
    
    # For when the form is submitted:
    if request.method == "POST":
        print("POST data:", request.POST)
        # Bind the form to the POST data and files
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid() and report.user == request.user:
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Report updated successfully!')
            return HttpResponseRedirect(reverse('report-detail', args=[pk]))
        else:
            messages.add_message(request, messages.ERROR, 'Error updating report.')
    else:
        # Prepopulate the form with the existing report data
        form = ReportForm(instance=report)
    return render(request, 'mapper/edit_report.html', {'form': form, 'report': report})    


def delete_report(request, pk):
    """
    Edit an existing report
    """
    # Get the report object based on the primary key (pk) from the URL
    queryset = Report.objects.all()
    report = get_object_or_404(queryset, pk=pk)
    if report.user == request.user:
        report.delete()
        messages.add_message(request, messages.SUCCESS, 'Report deleted successfully!')
        return HttpResponseRedirect(reverse('reports-list'))
    else:
        messages.add_message(request, messages.ERROR, 'You do not have permission to delete this report.')
    

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
    
    
@csrf_protect
def update_report_location(request, pk):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            # Validate the data
            if latitude is None or longitude is None:
                return JsonResponse({'success': False, 
                                     'error': 'Invalid data'}, 
                                    status=400)

            # Get the report object and update its location
            report = get_object_or_404(Report, pk=pk)
            report.latitude = latitude
            report.longitude = longitude
            report.save()
            
            # get the new place_name and county
            updated_place_name = report.place_name
            print(f"Updated place name: {updated_place_name}")
            updated_county = report.county.county if report.county else None
            print(f"Updated county: {updated_county}")
            
            return JsonResponse({'success': True, 
                                 'message': 'Location updated successfully!',
                                 'place_name': updated_place_name,
                                 'county': updated_county})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)