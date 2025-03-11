"""
Views for the demographics app.

This module contains API views for the demographics app models.
"""

from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from demographics.models import DemographicStatistic
from demographics.serializers import DemographicStatisticSerializer
from demographics.filters import DemographicStatisticFilter


class DemographicStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows demographic statistics to be viewed.

    Provides a list of all demographic statistics with filtering capabilities.

    Query Parameters:
    - year: Filter by year (e.g., 2023)
    - age_group: Filter by age group name (e.g., "0 - 4 years")
    - sex: Filter by sex name (e.g., "Male", "Female")
    - hd_index: Filter by HDI category name (e.g., "High Human Development Index (HDI)")

    The response includes the aggregated total for both sexes when filtering
    by age group and HDI category.
    """

    queryset = DemographicStatistic.objects.select_related(
        "age_group", "sex", "hd_index"
    ).all()
    serializer_class = DemographicStatisticSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = DemographicStatisticFilter
    ordering_fields = ["year", "value"]
    ordering = ["year"]
