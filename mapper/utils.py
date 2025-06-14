"""
Utilities for the mapper app
"""
import os
import requests
import time
from django.core.cache import cache


def serialise_report(report):
    """
    Convert a Report instance into a JSON-serialisable dict.

    Extracts key fields and related data for HTMX/JSON responses:
      - 'user': report.user.username or None
      - 'user_report_number': per-user sequence number
      - 'user_is_superuser': boolean flag
      - 'id': primary key
      - 'latitude', 'longitude', 'place_name'
      - 'county': name of the county if set, else None
      - 'condition': traffic-light code
      - 'reasons': human-readable reasons display
      - 'comments': free-text comments
      - 'photoUrl': URL to the uploaded image or None

    Args:
        report (Report): The Report model instance to serialize.

    Returns:
        dict: A mapping of report attributes suitable for JSON encoding.
    """
    # check if the place_name is empty and reverse geocode if necessary
    if not report.place_name:
        success = report.reverse_geocode(report.latitude, report.longitude)
        if success:
            report.save(update_fields=['place_name'])

    return {
        'user': report.user.username if report.user else None,
        'user_id': report.user.id if report.user else None,
        'user_report_number': report.user_report_number,
        'user_is_superuser': report.user.is_superuser if report.user
        else False,
        'id': report.id,
        'latitude': report.latitude,
        'longitude': report.longitude,
        'place_name': report.place_name,
        'county': report.county.county if report.county else None,
        'condition': report.condition,
        'reasons': report.get_reasons_display(),
        'comments': report.comments,
        'photoUrl': report.photo.url if report.photo else None,
        }


class SessionTokenError(Exception):
    """Raised when a Google Maps session token cannot be retrieved."""


def get_google_session_token():
    """
    Obtain and cache a Google Maps session token for satellite tile requests.

    - Checks the Django cache for an existing `google_tile_session_token`.
    - If found and not expired, returns the cached session token.
    - If missing or expired:
        1. Reads `GOOGLE_MAPS_API_KEY` from the environment.
        2. Calls the Google Maps `createSession` endpoint with payload:
           - mapType: "satellite"
           - language: "en-GB"
           - region: "UK"
        3. On HTTP 200, parses the JSON response for `session` and `expiry`.
        4. Calculates the remaining TTL and stores the full response in cache.
        5. Returns the new session token.
    - On non-200 responses, raises an Exception with the response text.

    Returns:
        str: A valid Google Maps session token.

    Raises:
        Exception: When the Google API call fails or returns a non-200 status.
    """
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
        "region": "UK",
        "layerTypes": "layerRoadmap",
        "overlay": "false"
    }
    headers = {
        "Content-Type": "application/json"
    }

    # Request the session token
    response = requests.post(create_session_url,
                             json=payload,
                             headers=headers,
                             timeout=30)
    if response.status_code == 200:
        data = response.json()
        session_token = data.get("session")
        expiry = data.get("expiry")
        # Calculate the remaining time until expiry (expiry is seconds since
        # the epoch)
        now = int(time.time())
        remaining = int(expiry) - now if expiry and int(expiry) > now else 14 * 24 * 3600
        # Cache the full token data (you might want to cache the expiry
        # as well)
        cache.set('google_tile_session_token', data, timeout=remaining)
        return session_token
    raise SessionTokenError(f"Failed to obtain session token: {response.text}")
