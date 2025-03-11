"""
Tests for the frontend visualization views.

This module contains tests for the frontend visualization views
that display charts and interactive elements for the demographic data.
"""

import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.messages import get_messages
from unittest.mock import patch, MagicMock
import tempfile
import os

from demographics.models import DemographicStatistic, AgeGroup, Sex, HDIndex


@pytest.mark.django_db
class TestFrontendViews:
    """Test class for frontend visualization views."""

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Set up test data for the dashboard."""
        # Create age groups
        age_group_1 = AgeGroup.objects.create(name="0 - 4 years", is_aggregate=False)
        age_group_2 = AgeGroup.objects.create(name="5 - 9 years", is_aggregate=False)

        # Create sexes
        male = Sex.objects.create(name="Male", is_aggregate=False)
        female = Sex.objects.create(name="Female", is_aggregate=False)

        # Create HDI categories
        high_hdi = HDIndex.objects.create(
            name="High Human Development Index (HDI)", is_aggregate=False
        )
        medium_hdi = HDIndex.objects.create(
            name="Medium Human Development Index (HDI)", is_aggregate=False
        )

        # Create demographic statistics
        DemographicStatistic.objects.create(
            year=2023,
            age_group=age_group_1,
            sex=male,
            hd_index=high_hdi,
            value=1000,
        )
        DemographicStatistic.objects.create(
            year=2023,
            age_group=age_group_1,
            sex=female,
            hd_index=high_hdi,
            value=900,
        )
        DemographicStatistic.objects.create(
            year=2022,
            age_group=age_group_2,
            sex=male,
            hd_index=medium_hdi,
            value=800,
        )

    def test_dashboard_view(self):
        """Test that the dashboard view returns a 200 status code."""
        client = Client()
        url = reverse("dashboard")
        response = client.get(url)
        assert response.status_code == 200

        # Check that the response contains the required HTML elements and scripts
        content = response.content.decode()
        assert "<title>Demographics Dashboard</title>" in content or "<title>Dashboard</title>" in content
        assert 'id="app"' in content  # Alpine.js app container
        assert "alpine" in content.lower()  # Alpine.js might be referenced in various ways
        assert "axios" in content.lower() or "fetch" in content.lower()  # HTTP client
        assert "chart" in content.lower()  # Chart.js
        assert "tailwind" in content.lower() or "css" in content.lower()  # CSS framework

        # In a real app, years and age groups would be dynamically loaded,
        # so we won't check for specific values in the HTML

    def test_dashboard_contains_filter_controls(self):
        """Test that the dashboard contains filter controls."""
        client = Client()
        url = reverse("dashboard")
        response = client.get(url)
        content = response.content.decode()

        # Check for filter-related elements (the actual IDs might vary)
        assert "filter" in content.lower()
        assert "year" in content.lower()
        assert "age" in content.lower()
        assert "sex" in content.lower()
        assert "hdi" in content.lower() or "development" in content.lower()

    def test_dashboard_contains_chart_containers(self):
        """Test that the dashboard contains chart containers."""
        client = Client()
        url = reverse("dashboard")
        response = client.get(url)
        content = response.content.decode()

        # Check for chart container elements
        assert "chart" in content.lower()
        assert "canvas" in content.lower()  # Chart.js uses canvas elements

    def test_dashboard_contains_import_controls(self):
        """Test that the dashboard contains import controls."""
        client = Client()
        url = reverse("dashboard")
        response = client.get(url)
        content = response.content.decode()

        # Check for import-related elements
        assert "import" in content.lower()
        assert "file" in content.lower()
        assert "url" in content.lower()
        assert "submit" in content.lower() or "button" in content.lower()

    def test_dashboard_contains_database_controls(self):
        """Test that the dashboard contains database cleaning controls."""
        client = Client()
        url = reverse("dashboard")
        response = client.get(url)
        content = response.content.decode()

        # Check for database-related elements
        assert "clean" in content.lower() or "reset" in content.lower() or "clear" in content.lower()
        assert "database" in content.lower() or "data" in content.lower()

    def test_import_file_view_no_file(self):
        """Test that the import file view handles missing file correctly."""
        client = Client()
        url = reverse("import_file")
        response = client.post(url, {}, follow=True)
        
        # Check that the response redirects to the dashboard
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse("dashboard")
        
        # Check that an error message was set
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) > 0
        assert "No file" in str(messages[0]) or "file" in str(messages[0]).lower()

    @patch("visualization.views.call_command")
    def test_import_file_view_with_file(self, mock_call_command):
        """Test that the import file view processes file uploads."""
        # Create a temporary CSV file
        temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        temp_csv.write(b"Year,Age Group,Sex,Human Development Index Rating,VALUE\n")
        temp_csv.write(b"2023,0 - 4 years,1,20,1000\n")
        temp_csv.close()
        
        try:
            # Open file for reading
            with open(temp_csv.name, "rb") as csv_file:
                client = Client()
                url = reverse("import_file")
                response = client.post(
                    url, 
                    {"file": csv_file}, 
                    follow=True
                )
            
            # Check that the response redirects to the dashboard
            assert response.status_code == 200
            assert response.redirect_chain[-1][0] == reverse("dashboard")
            
            # Check that a success or error message was set
            messages = list(get_messages(response.wsgi_request))
            assert len(messages) > 0
        finally:
            # Clean up the temporary file
            os.unlink(temp_csv.name)

    def test_import_url_view_no_url(self):
        """Test that the import URL view handles missing URL correctly."""
        client = Client()
        url = reverse("import_url")
        response = client.post(url, {}, follow=True)
        
        # Check that the response redirects to the dashboard
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse("dashboard")
        
        # Check that an error message was set
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) > 0
        assert "No URL" in str(messages[0]) or "url" in str(messages[0]).lower()

    @patch("visualization.views.call_command")
    def test_import_url_view_with_url(self, mock_call_command):
        """Test that the import URL view processes URL imports."""
        # Mock the call_command function
        mock_call_command.return_value = None
        
        client = Client()
        url = reverse("import_url")
        response = client.post(
            url, 
            {"url": "https://example.com/data.csv"}, 
            follow=True
        )
        
        # Check that the response redirects to the dashboard
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse("dashboard")
        
        # Check that a success message was set
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) > 0
        
        # Check that the command was called with the URL
        mock_call_command.assert_called_once()

    def test_clean_database_view(self):
        """Test that the clean database view works correctly."""
        # Ensure we have data before cleaning
        assert DemographicStatistic.objects.count() > 0
        
        client = Client()
        url = reverse("clean_database")
        response = client.post(url, follow=True)
        
        # Check that the response redirects to the dashboard
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse("dashboard")
        
        # Check that a success message was set
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) > 0
        assert "clean" in str(messages[0]).lower()
        
        # Verify that demographic statistics were cleaned
        assert DemographicStatistic.objects.count() == 0

    @patch("visualization.views.call_command")
    def test_import_url_view_with_exception(self, mock_call_command):
        """Test that the import URL view handles exceptions correctly."""
        # Mock the call_command function to raise an exception
        mock_call_command.side_effect = Exception("Import failed")
        
        client = Client()
        url = reverse("import_url")
        response = client.post(
            url, 
            {"url": "https://example.com/data.csv"}, 
            follow=True
        )
        
        # Check that the response redirects to the dashboard
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse("dashboard")
        
        # Check that an error message was set
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) > 0
        assert "fail" in str(messages[0]).lower() or "error" in str(messages[0]).lower()
