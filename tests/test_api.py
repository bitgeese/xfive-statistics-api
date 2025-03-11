"""
Tests for the Demographics API endpoints.

This module contains tests for the Demographics API endpoints, including
filtering by various parameters and aggregation of statistics.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic


@pytest.mark.django_db
class TestDemographicsAPI:
    """Test class for Demographics API endpoints."""

    @pytest.fixture
    def api_client(self):
        """Return an API client for testing."""
        return APIClient()

    @pytest.fixture
    def setup_data(self):
        """
        Set up test data for demographic statistics.

        Creates sample data with different years, age groups, sexes, and HDI categories.
        """
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

        # Create demographic statistics for 2022
        # High HDI
        DemographicStatistic.objects.create(
            year=2022, age_group=age_group_1, sex=male, hd_index=high_hdi, value=100
        )
        DemographicStatistic.objects.create(
            year=2022, age_group=age_group_1, sex=female, hd_index=high_hdi, value=90
        )
        DemographicStatistic.objects.create(
            year=2022, age_group=age_group_2, sex=male, hd_index=high_hdi, value=80
        )
        DemographicStatistic.objects.create(
            year=2022, age_group=age_group_2, sex=female, hd_index=high_hdi, value=70
        )

        # Medium HDI
        DemographicStatistic.objects.create(
            year=2022, age_group=age_group_1, sex=male, hd_index=medium_hdi, value=50
        )
        DemographicStatistic.objects.create(
            year=2022, age_group=age_group_1, sex=female, hd_index=medium_hdi, value=40
        )
        DemographicStatistic.objects.create(
            year=2022, age_group=age_group_2, sex=male, hd_index=medium_hdi, value=30
        )
        DemographicStatistic.objects.create(
            year=2022, age_group=age_group_2, sex=female, hd_index=medium_hdi, value=20
        )

        # Create demographic statistics for 2023
        # High HDI
        DemographicStatistic.objects.create(
            year=2023, age_group=age_group_1, sex=male, hd_index=high_hdi, value=110
        )
        DemographicStatistic.objects.create(
            year=2023, age_group=age_group_1, sex=female, hd_index=high_hdi, value=100
        )
        DemographicStatistic.objects.create(
            year=2023, age_group=age_group_2, sex=male, hd_index=high_hdi, value=90
        )
        DemographicStatistic.objects.create(
            year=2023, age_group=age_group_2, sex=female, hd_index=high_hdi, value=80
        )

        # Medium HDI
        DemographicStatistic.objects.create(
            year=2023, age_group=age_group_1, sex=male, hd_index=medium_hdi, value=60
        )
        DemographicStatistic.objects.create(
            year=2023, age_group=age_group_1, sex=female, hd_index=medium_hdi, value=50
        )
        DemographicStatistic.objects.create(
            year=2023, age_group=age_group_2, sex=male, hd_index=medium_hdi, value=40
        )
        DemographicStatistic.objects.create(
            year=2023, age_group=age_group_2, sex=female, hd_index=medium_hdi, value=30
        )

        return {
            "age_groups": {"age_group_1": age_group_1, "age_group_2": age_group_2},
            "sexes": {"male": male, "female": female},
            "hd_indices": {"high_hdi": high_hdi, "medium_hdi": medium_hdi},
        }

    def test_demographics_list_endpoint(self, api_client, setup_data):
        """Test the demographics list endpoint returns all statistics."""
        url = reverse("demographics-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 16  # Total number of statistics in setup_data
        assert len(response.data["results"]) <= 50  # Pagination limit (from settings)

    def test_filter_by_year(self, api_client, setup_data):
        """Test filtering demographic statistics by year."""
        url = reverse("demographics-list")
        response = api_client.get(url, {"year": 2023})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 8  # Number of statistics for 2023
        for item in response.data["results"]:
            assert item["year"] == 2023

    def test_filter_by_age_group(self, api_client, setup_data):
        """Test filtering demographic statistics by age group."""
        age_group = setup_data["age_groups"]["age_group_1"]
        url = reverse("demographics-list")
        response = api_client.get(url, {"age_group": age_group.name})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 8  # Number of statistics for age_group_1
        for item in response.data["results"]:
            assert item["age_group"] == age_group.name

    def test_filter_by_sex(self, api_client, setup_data):
        """Test filtering demographic statistics by sex."""
        sex = setup_data["sexes"]["male"]
        url = reverse("demographics-list")
        response = api_client.get(url, {"sex": sex.name})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 8  # Number of statistics for males
        for item in response.data["results"]:
            assert item["sex"] == sex.name

    def test_filter_by_hd_index(self, api_client, setup_data):
        """Test filtering demographic statistics by HDI category."""
        hd_index = setup_data["hd_indices"]["high_hdi"]
        url = reverse("demographics-list")
        response = api_client.get(url, {"hd_index": hd_index.name})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 8  # Number of statistics for high HDI
        for item in response.data["results"]:
            assert item["hd_index"] == hd_index.name

    def test_combined_filters(self, api_client, setup_data):
        """Test filtering demographic statistics by multiple parameters."""
        age_group = setup_data["age_groups"]["age_group_1"]
        hd_index = setup_data["hd_indices"]["high_hdi"]
        url = reverse("demographics-list")
        response = api_client.get(
            url, {"year": 2023, "age_group": age_group.name, "hd_index": hd_index.name}
        )

        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["count"] == 2
        )  # Male and female for 2023, age_group_1, high_hdi
        for item in response.data["results"]:
            assert item["year"] == 2023
            assert item["age_group"] == age_group.name
            assert item["hd_index"] == hd_index.name

    def test_both_sexes_aggregation(self, api_client, setup_data):
        """
        Test that the API returns aggregated statistics for both sexes.

        This is a key requirement: when filtering by age group and HDI,
        the API should return individual statistics by sex and also
        include the aggregated total for both sexes.
        """
        age_group = setup_data["age_groups"]["age_group_1"]
        hd_index = setup_data["hd_indices"]["high_hdi"]
        url = reverse("demographics-list")
        response = api_client.get(
            url, {"year": 2023, "age_group": age_group.name, "hd_index": hd_index.name}
        )

        assert response.status_code == status.HTTP_200_OK

        # The response should include male and female statistics
        male_value = None
        female_value = None
        for item in response.data["results"]:
            if item["sex"] == "Male":
                male_value = item["value"]
            elif item["sex"] == "Female":
                female_value = item["value"]

        assert male_value is not None
        assert female_value is not None

        # The response should include the total for both sexes
        assert "total_both_sexes" in response.data["results"][0]
        assert (
            response.data["results"][0]["total_both_sexes"] == male_value + female_value
        )

    def test_empty_result_with_filter(self, api_client, setup_data):
        """Test that filtering with non-existent values returns an empty list."""
        url = reverse("demographics-list")
        response = api_client.get(url, {"year": 2024})  # Year not in test data

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0

    def test_invalid_filter_parameter_returns_error(self, api_client, setup_data):
        """Test that invalid filter parameters return appropriate error messages."""
        url = reverse("demographics-list")
        response = api_client.get(url, {"age_group": "Non-existent Age Group"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert "age_group" in response.data["error"]
        assert "Non-existent Age Group" in response.data["error"]
