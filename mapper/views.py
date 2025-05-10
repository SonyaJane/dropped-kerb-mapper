"""
Views for the Dropped Kerb Mapper application.

This module defines all HTTP endpoints and view logic for:
  • home: Public landing page.
  • MapReportsView: Interactive map-based report creation and listing (HTMX-enabled).
  • update_report_location: AJAX endpoint to move a report marker.
  • edit_report: Display and process the report editing form.
  • delete_report: Delete a user's report with permission checks.
  • ReportList: Tabular listing of reports via django-tables2.
  • report_detail: Detail page (and HTMX/JSON partial) for a single report.
  • get_os_map_tiles: Proxy view to fetch OS raster map tiles.
  • get_google_satellite_tiles: Proxy view to fetch Google satellite tiles with session management.
  • CustomConfirmEmailView: Auto-confirm email and log the user in.
  • email_confirmation_success: Static page after email confirmation.
  • instructions: Static usage instructions page.
  • contact: Render and process the contact-us form.

Each view either returns an HttpResponse (rendered template, JSON, or image bytes) 
or redirects as appropriate, and enforces authentication/permissions where required.
"""
import os
import json
import requests

from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django_tables2 import SingleTableView, RequestConfig
from allauth.account.views import ConfirmEmailView
from .forms import ReportForm, ContactForm
from .models import Report
from .tables import ReportTable
from .utils import serialise_report, get_google_session_token

# HOME PAGE
def home(request):
    """
    Render and return the application home page.

    Provides the landing page for Dropped Kerb Mapper, offering
    introductory content and navigation to login, signup, and map
    reporting features.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered 'mapper/home.html' template.
    """
    return render(request, 'mapper/home.html')


# MAP REPORTS PAGE
class MapReportsView(LoginRequiredMixin, View):
    """
    Handles the interactive map-reports page:

    GET:
      - Instantiates an empty ReportForm
      - Fetches existing reports: all for superusers, or only the
        current user's reports
      - Serialises reports into JSON-safe dictionaries
      - Renders 'mapper/map_reports.html' passing:
          • form: ReportForm instance
          • reports: list of serialised report dicts
          • is_map_reports: True (to customise form cancel link)

    POST:
      - Binds ReportForm to request.POST and request.FILES with user context
      - On valid form:
          • Creates a new Report (assigns request.user, saves)
          • Adds a SUCCESS message to the messages framework
          • Renders the HTMX partial 'mapper/partials/success.html'
            with context {'report': serialised_report}
      - On invalid form:
          • Adds an ERROR message
    """
    def get(self, request):
        """
        Handle GET requests for the interactive map-reports page.

        - Instantiates an empty ReportForm for new report submissions.
        - Retrieves existing reports: all reports for superusers, or only the
          current user's reports otherwise.
        - Serialises each report into a JSON-safe dictionary.
        - Renders 'mapper/map_reports.html' with context:
            • form: ReportForm instance
            • reports: list of serialised report dicts
            • is_map_reports: True (to adjust the cancel link behavior).

        Args:
            request (HttpRequest): The incoming HTTP GET request.

        Returns:
            HttpResponse: The rendered map reports page.
        """
        form = ReportForm()
        # Only show this user's reports (unless they're superuser)
        if request.user.is_superuser:
            reports = Report.objects.all()
        else:
            reports = Report.objects.filter(user=request.user)
        data = [serialise_report(report) for report in reports]
        return render(request, 'mapper/map_reports.html',
                        {'form': form,
                        'reports': data,
                        # Indicate to the ReportForm that it is on the map_reports page
                        'is_map_reports': True})

    def post(self, request):
        """
        Handle POST requests to create a new dropped-kerb report via the map interface.

        - Binds ReportForm to request.POST, request.FILES, and the current user.
        - If the form is valid:
            • Creates and saves a new Report linked to request.user.
            • Adds a SUCCESS message to the messages framework.
            • Returns the HTMX partial 'mapper/partials/success.html'
              with context {'report': serialise_report(report)}.
        - If the form is invalid:
            • Adds an ERROR message.

        Args:
            request (HttpRequest): The incoming HTTP POST request from the map page.

        Returns:
            HttpResponse: Rendered success partial.
        """
        form = ReportForm(data=request.POST, files=request.FILES, user=request.user)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.add_message(request, messages.SUCCESS, 'Report created successfully!')
            return render(request,
                        'mapper/partials/success.html',
                        {'report': serialise_report(report)})
        messages.add_message(request,
                             messages.ERROR,
                             'Error creating report. Please try again later.')
        return HttpResponse(status=204)

@require_POST
@login_required
def update_report_location(request, pk):
    """
    Update an existing report's latitude and longitude when the user drags 
    the map marker to another location.

    Only accepts POST requests from authenticated users.
    Superusers may update any report; regular users may only update their own.

    Parses 'latitude' and 'longitude' from request.POST:
      - Returns HttpResponseBadRequest if values are missing or invalid.
      - Updates the Report instance, triggering reverse geocoding and spatial lookups on save().
      - Adds a SUCCESS message and returns the HTMX partial 'mapper/partials/success.html'
        with context {'report': serialise_report(report)}.

    Args:
        request (HttpRequest): The incoming POST request containing 'latitude' and 'longitude'.
        pk (int): Primary key of the Report to update.

    Returns:
        HttpResponse: Rendered success partial on successful update.
        HttpResponseBadRequest: If required parameters are missing or invalid.
    """
    # Get the report with primary key pk
    # superuser can update any report, others can only update their own
    if request.user.is_superuser:
        report = get_object_or_404(Report, pk=pk)
    else:
        report = get_object_or_404(Report, pk=pk, user=request.user)
    try:
        lat = float(request.POST['latitude'])
        lon = float(request.POST['longitude'])
    except (KeyError, json.JSONDecodeError): # Handle missing or invalid data
        return HttpResponseBadRequest()

    # Get the report object and update its location
    report.latitude = lat
    report.longitude = lon
    report.save() # handles updating the place_name, county and local authority
    # get the updated report object
    report.refresh_from_db()
    # Create success message
    messages.add_message(request, messages.SUCCESS, 'Location updated successfully!')
    # render a small partial that HTMX will swap
    return render(request,
                  'mapper/partials/success.html',
                  {'report': serialise_report(report)})

def edit_report(request, pk):
    """
    Display and process the form for editing an existing report.

    GET:
      - Retrieves the Report by primary key.
      - Instantiates a ReportForm pre-populated with the report instance.
      - Renders 'mapper/edit_report.html' with context {'form': form, 'report': report}.

    POST:
      - Binds ReportForm to request.POST, request.FILES, and the existing report.
      - If valid and the user has permission (owner or superuser):
          • Saves the updated report.
          • Adds a SUCCESS message.
          • Redirects to the report-detail page.
      - Otherwise:
          • Adds an ERROR message.
          • Falls through to re-render the edit form with errors.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): Primary key of the Report to edit.

    Returns:
        HttpResponse or HttpResponseRedirect: Renders the edit form template on GET
        or invalid POST; redirects to detail page on successful POST.
    """
    # Allow superuser to grab any report; others only their own
    report = get_object_or_404(Report, pk=pk)

    # For when the form is submitted:
    if request.method == "POST":
        # Bind the form to the POST data and files
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid() and (report.user == request.user or request.user.is_superuser):
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Report updated successfully!')
            return HttpResponseRedirect(reverse('report-detail', args=[pk]))
        messages.add_message(request, messages.ERROR, 'Error updating report.')
    else: # GET request
        # Create a new form instance with the existing report data
        # Prepopulate the form with the existing report data
        form = ReportForm(instance=report)
    return render(request, 'mapper/edit_report.html', {'form': form, 'report': report})  


def delete_report(request, pk):
    """
    Delete a dropped-kerb report.

    - Retrieves the Report by primary key (returns 404 if not found).
    - If the requesting user is the report owner or a superuser:
        • Deletes the report.
        • Adds a SUCCESS message.
        • Redirects to the reports list page.
    - If the user is not the owner or a superuser:
        • Adds an ERROR message indicating lack of permission.
        • Redirects to the reports list page.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): Primary key of the Report to delete.

    Returns:
        HttpResponseRedirect: Redirect to 'reports-list' after deletion or
                              permission denial.
    """
    # Get the report object based on the primary key (pk) from the URL
    queryset = Report.objects.all()
    report = get_object_or_404(queryset, pk=pk)
    if report.user == request.user or request.user.is_superuser:
        report.delete()
        messages.add_message(request, messages.SUCCESS, 'Report deleted successfully!')
    messages.add_message(request,
                         messages.ERROR,
                         'You do not have permission to delete this report.')
    return HttpResponseRedirect(reverse('reports-list'))


# LIST OF REPORTS
class ReportList(LoginRequiredMixin, SingleTableView):
    """
    Display a table of dropped-kerb reports for the current user.

    Authentication required:
      - Superusers see all reports.
      - Regular users see only their own.

    Renders the reports in a paginated django-tables2 table
    using 'mapper/reports.html' as the template. The table
    columns are dynamically excluded based on the user's role:
      • Superusers exclude: user_report_number, latitude, longitude, local_authority
      • Regular users exclude: id, user, latitude, longitude, local_authority, created_at
    """
    login_url = 'account_login' # where to redirect if not logged in
    redirect_field_name = 'next'
    model = Report
    template_name = "mapper/reports.html"

    def get_queryset(self):
        """
        Retrieve the list of Report objects for display in the table.

        - Superusers receive all reports.
        - Regular users receive only their own reports.

        Returns:
            QuerySet[Report]: The filtered set of reports based on the current user's permissions.
        """
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        return qs

    def get_table(self, **kwargs):
        """
        Construct and configure the ReportTable for the list view.

        - Retrieves the filtered QuerySet via get_queryset().
        - Excludes certain columns based on the current user's role:
            • Superusers: user_report_number, latitude, longitude, local_authority
            • Regular users: id, user, latitude, longitude, local_authority, created_at
        - Applies django-tables2 RequestConfig for pagination and sorting.

        Args:
            **kwargs: Additional keyword arguments (unused).

        Returns:
            ReportTable: The configured table instance for rendering.
        """
        qs = self.get_queryset()
        # Dynamically exclude columns based on the current user
        if self.request.user.is_superuser:
            table = ReportTable(qs,
                                exclude=('user_report_number','latitude',
                                         'longitude','local_authority'))
        else:
            table = ReportTable(qs, 
                                exclude=('id', 'user','latitude','longitude',
                                         'local_authority','created_at'))
        RequestConfig(self.request).configure(table)
        return table


# REPORT DETAILS
@login_required
def report_detail(request, pk):
    """
    Display detailed information for a single dropped-kerb report.

    - Retrieves the Report by primary key (404 if not found).
    - If `place_name` is missing, attempts reverse geocoding and saves it.
    - For HTMX or AJAX requests, returns JsonResponse with serialised report data.
    - For standard requests, renders 'mapper/report_detail.html' with the report context.

    Args:
        request (HttpRequest): The incoming HTTP request.
        pk (int): Primary key of the Report to display.

    Returns:
        JsonResponse: Serialised report for HTMX/AJAX calls.
        HttpResponse: Rendered detail page for regular requests.
    """
    queryset = Report.objects.all()
    report = get_object_or_404(queryset, pk=pk)

    # check if the place_name is empty and reverse geocode if necessary
    if not report.place_name:
        success = report.reverse_geocode(report.latitude, report.longitude)
        if success:
            report.save(update_fields=['place_name'])

    # Check if the request is an AJAX or HTMX request
    if request.headers.get('HX-Request') \
        or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(serialise_report(report))

    # Render the report detail page for non-AJAX requests
    return render(request, "mapper/report_detail.html", {"report": report})


def get_os_map_tiles(request, z, x, y):
    """
    Proxy view to fetch Ordnance Survey raster map tiles.

    - Caps `z` (zoom level) at a configured maximum (20).
    - Builds the OS Maps API URL using `z`, `x`, `y` and the
      `OS_MAPS_API_KEY` environment variable.
    - Performs an HTTP GET to retrieve the PNG tile.
    - On success (HTTP 200), returns the tile bytes as an `image/png` response.
    - On failure, returns a 404 response with caching headers
      (`Cache-Control: public, max-age=3600`).

    Args:
        request (HttpRequest): The incoming HTTP request.
        z (int): Zoom level of the requested tile.
        x (int): X coordinate of the requested tile.
        y (int): Y coordinate of the requested tile.

    Returns:
        HttpResponse: The PNG tile on success, or a 404 response on error.
    """
    # Limit the maximum zoom level to 20
    max_zoom = 20
    if z > max_zoom:
        z = min(z, max_zoom)

    api_key = os.environ.get("OS_MAPS_API_KEY")

    # Construct the Ordnance Survey tile URL
    tile_url = f"https://api.os.uk/maps/raster/v1/zxy/Light_3857/{z}/{x}/{y}.png?key={api_key}"

    # Make a GET request to fetch the tile image
    response = requests.get(tile_url)

    if response.status_code == 200:
        # Return the image content with appropriate content-type
        return HttpResponse(response.content, content_type="image/png")

    # Return a 404 response with caching headers
    return HttpResponse(
        status=404,
        headers={
            "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
        }
    )

def get_google_satellite_tiles(request, z, x, y):
    """
    Proxy view to fetch Google Maps satellite tiles with session management.

    - Retrieves or creates a Google Maps session token via get_google_session_token().
    - Constructs the tile URL using `z`, `x`, `y`, the session token, and `GOOGLE_MAPS_API_KEY`.
    - Sends an HTTP GET to the Google Maps 2D tiles endpoint.
    - On HTTP 200, returns the tile bytes with content-type `image/png`.
    - On HTTP 404, returns a 404 response with caching headers
      (`Cache-Control: public, max-age=3600`).
    - On other error statuses or token failures, raises Http404.

    Args:
        request (HttpRequest): The incoming HTTP request.
        z (int): Zoom level of the requested tile.
        x (int): X coordinate of the requested tile.
        y (int): Y coordinate of the requested tile.

    Returns:
        HttpResponse: The satellite tile image (`image/png`) on success.
        HttpResponse: A 404 response with caching headers if the tile is not found.

    Raises:
        Http404: If the session token cannot be obtained or other non-404 errors occur.
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
    if response.status_code == 404: # Tile not found at requested zoom level
        # Return a 404 response with caching headers
        return HttpResponse(
            status=404,
            headers={
                "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
            }
        )
    else:
        raise Http404("Tile not found.")

# EMAIL CONFIRMATION FOR SIGNUP VIEW
class CustomConfirmEmailView(ConfirmEmailView):
    """
    Automatically confirm a user's email address and log them in.

    Overrides the default allauth ConfirmEmailView to:
      1. Retrieve and confirm the EmailConfirmation object.
      2. Authenticate and log the user in with Django's ModelBackend.
      3. Redirect the user to the 'email-confirmation-success' page.

    This streamlines the signup flow by skipping the manual confirmation step
    and immediately granting access upon visiting the confirmation link.
    """
    def get(self, *args, **kwargs):
        # Automatically confirm the email
        confirmation = self.get_object()
        confirmation.confirm(self.request)

        # Log the user in
        user = confirmation.email_address.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)

        # Redirect to a success page or login the user
        return redirect('email-confirmation-success')


def email_confirmation_success(request):
    """
    Render the email confirmation success page.

    This view is shown after a user has clicked their email confirmation link
    and been automatically logged in via CustomConfirmEmailView.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered 'mapper/email_confirmation_success.html' template.
    """
    return render(request, 'mapper/email_confirmation_success.html')


# INSTRUCTIONS PAGE
def instructions(request):
    """
    Render the instructions page.

    Displays usage instructions and guidance for the Dropped Kerb Mapper application.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered 'mapper/instructions.html' template.
    """
    return render(request, 'mapper/instructions.html')


# CONTACT PAGE
def contact(request):
    """
    Render and process the contact-us form.

    GET:
    - Instantiates ContactForm (pre-fills and locks user fields if authenticated).
    - Renders 'mapper/contact.html' with an empty form and message_sent=False.

    POST:
    - Binds ContactForm to request.POST and current user.
    - If valid:
        • Sends an email to the site admin with the visitor's message.
        • Sends a confirmation email back to the visitor.
        • Adds a success message and sets message_sent=True.
    - If invalid:
        • Falls through to re-render the form with validation errors.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered 'mapper/contact.html' template with:
            - form: ContactForm instance
            - message_sent: bool indicating if the message was successfully sent
    """
    message_sent = False
    if request.method == 'POST':
        form = ContactForm(request.POST,
                           user=request.user if request.user.is_authenticated else None)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send the message to Mobility Mapper admin
            send_mail(
                subject=f"Contact Form Submission from {first_name} {last_name}",
                message=f"Message from {first_name} {last_name} ({email}):\n\n{message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
            )

            # Send a confirmation email to the user
            confirmation_message = (
                f"Hi {first_name} {last_name},\n\n"
                "Thank you for your message, we will get back to you as soon as possible.\n\n"
                "Here is a copy of your message:\n"
                f"{message}\n\n"
                "Kind regards,\n"
                "Mobility Mapper"
            )

            send_mail(
                subject="Thank you for contacting Mobility Mapper",
                message=confirmation_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )

             # Display a success message
            messages.success(request, 'Message submitted successfully!')
            message_sent = True
    else:
        form = ContactForm(user=request.user if request.user.is_authenticated else None)

    return render(request, 'mapper/contact.html', {'form': form, 'message_sent': message_sent})
