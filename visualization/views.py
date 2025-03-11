"""
Views for the visualization frontend.

This module contains views for the visualization frontend that displays
charts and interactive elements for the demographic data.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import json
from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic
from django.db.models import Count
from django.urls import reverse
from django.core.management import call_command
import os
import tempfile


@require_http_methods(["GET"])
def dashboard(request):
    """
    View for the demographics dashboard.

    This view renders the dashboard template with the following context:
    - api_endpoint: URL for the API
    - years: List of available years
    - age_groups: List of available age groups
    - sexes: List of available sexes
    - hdi_categories: List of available HDI categories
    """
    # Get unique values for filters
    years = list(
        DemographicStatistic.objects.values_list("year", flat=True)
        .distinct()
        .order_by("year")
    )
    age_groups = list(
        DemographicStatistic.objects.values_list("age_group", flat=True)
        .distinct()
        .order_by("age_group")
    )
    sexes = list(
        DemographicStatistic.objects.values_list("sex", flat=True)
        .distinct()
        .order_by("sex")
    )
    hdi_categories = list(
        DemographicStatistic.objects.values_list("hd_index", flat=True)
        .distinct()
        .order_by("hd_index")
    )

    # API endpoint for the dashboard to use
    api_endpoint = "/api/demographics/"

    # Get counts for summary stats
    total_records = DemographicStatistic.objects.count()

    context = {
        "api_endpoint": api_endpoint,
        "years": json.dumps(years),
        "age_groups": json.dumps(age_groups),
        "sexes": json.dumps(sexes),
        "hdi_categories": json.dumps(hdi_categories),
        "total_records": total_records,
    }

    return render(request, "visualization/dashboard.html", context)


@require_http_methods(["POST"])
def import_file(request):
    """Handle importing data from an uploaded file."""
    if "file" not in request.FILES:
        messages.error(request, "No file provided.")
        return redirect("dashboard")

    uploaded_file = request.FILES["file"]

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        temp_file_path = temp_file.name

    try:
        # Call the management command
        call_command("import_demographics", file=temp_file_path)
        messages.success(
            request, f"Successfully imported data from file: {uploaded_file.name}"
        )
    except Exception as e:
        messages.error(request, f"Failed to import data: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

    return redirect("dashboard")


@require_http_methods(["POST"])
def import_url(request):
    """Handle importing data from a URL."""
    url = request.POST.get("url")
    if not url:
        messages.error(request, "No URL provided.")
        return redirect("dashboard")

    try:
        # Call the management command
        call_command("import_demographics", url=url)
        messages.success(request, f"Successfully imported data from URL: {url}")
    except Exception as e:
        messages.error(request, f"Failed to import data: {str(e)}")

    return redirect("dashboard")


@require_http_methods(["POST"])
def clean_database(request):
    """Handle cleaning the database."""
    try:
        # Delete all demographic statistics
        count = DemographicStatistic.objects.count()
        DemographicStatistic.objects.all().delete()
        messages.success(
            request, f"Successfully cleaned the database. Removed {count} records."
        )
    except Exception as e:
        messages.error(request, f"Failed to clean the database: {str(e)}")

    return redirect("dashboard")
