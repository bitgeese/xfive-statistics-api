"""
Tests for the frontend visualization views.

This module contains tests for the frontend visualization views
that display charts and interactive elements for the demographic data.
"""

import pytest
from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
class TestFrontendViews:
    """Test class for frontend visualization views."""

    def test_dashboard_view(self):
        """Test that the dashboard view returns a 200 status code."""
        client = Client()
        url = reverse("dashboard")
        response = client.get(url)
        assert response.status_code == 200

        # Check that the response contains the required HTML elements and scripts
        content = response.content.decode()
        assert "<title>Demographics Dashboard</title>" in content
        assert 'id="app"' in content  # Alpine.js app container
        assert "Alpine.js" in content or "alpine.js" in content
        assert "axios" in content
        assert "Chart.js" in content or "chart.js" in content
        assert "tailwind" in content

    def test_dashboard_contains_filter_controls(self):
        """Test that the dashboard contains filter controls."""
        client = Client()
        url = reverse("dashboard")
        response = client.get(url)
        content = response.content.decode()

        # Check for filter elements
        assert 'id="year-filter"' in content
        assert 'id="age-group-filter"' in content
        assert 'id="sex-filter"' in content
        assert 'id="hdi-filter"' in content

    def test_dashboard_contains_chart_containers(self):
        """Test that the dashboard contains chart containers."""
        client = Client()
        url = reverse("dashboard")
        response = client.get(url)
        content = response.content.decode()

        # Check for chart containers
        assert 'id="demographics-chart"' in content
        assert 'id="age-distribution-chart"' in content

    def test_dashboard_contains_import_controls(self):
        """Test that the dashboard contains import controls for file and URL."""
        client = Client()
        url = reverse("dashboard")
        response = client.get(url)
        content = response.content.decode()

        # Check for import controls
        assert 'id="import-file-form"' in content
        assert 'id="import-url-form"' in content
        assert 'id="file-import"' in content
        assert 'id="url-import"' in content
        assert "Import Data" in content

    def test_dashboard_contains_database_controls(self):
        """Test that the dashboard contains database cleaning controls."""
        client = Client()
        url = reverse("dashboard")
        response = client.get(url)
        content = response.content.decode()

        # Check for database controls
        assert 'id="clean-database-form"' in content
        assert "Clean Database" in content

    def test_import_file_view(self):
        """Test that the import file view works correctly."""
        client = Client()
        url = reverse("import_file")

        # This test just checks the view exists and returns a redirect
        # Actual file upload testing would require more complex mocking
        response = client.get(url)
        assert response.status_code == 405  # Should be POST only

    def test_import_url_view(self):
        """Test that the import URL view works correctly."""
        client = Client()
        url = reverse("import_url")

        # Test with a bad URL
        response = client.post(url, {"url": "not-a-url"})
        assert response.status_code == 302  # Should redirect

    def test_clean_database_view(self):
        """Test that the clean database view works correctly."""
        client = Client()
        url = reverse("clean_database")

        response = client.post(url)
        assert response.status_code == 302  # Should redirect
