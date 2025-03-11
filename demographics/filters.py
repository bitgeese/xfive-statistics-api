"""
Filter backends for the demographics app.

This module contains filter backends for the demographics app models,
specifically for filtering DemographicStatistic instances.
"""

import django_filters
from django_filters import rest_framework as filters
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from demographics.models import DemographicStatistic, AgeGroup, Sex, HDIndex


class DemographicStatisticFilter(filters.FilterSet):
    """
    FilterSet for DemographicStatistic model.

    Allows filtering by year, age_group, sex, and hd_index.
    String-based filtering is used for related fields to make the API
    more user-friendly.
    """

    year = django_filters.NumberFilter(field_name="year")
    age_group = django_filters.CharFilter(
        field_name="age_group__name", method="filter_age_group"
    )
    sex = django_filters.CharFilter(field_name="sex__name", method="filter_sex")
    hd_index = django_filters.CharFilter(
        field_name="hd_index__name", method="filter_hd_index"
    )

    class Meta:
        model = DemographicStatistic
        fields = ["year", "age_group", "sex", "hd_index"]

    def filter_age_group(self, queryset, name, value):
        """
        Filter by age group and validate that the age group exists.

        Args:
            queryset: The queryset to filter
            name: The field name to filter on (age_group__name)
            value: The value to filter by

        Returns:
            Filtered queryset

        Raises:
            ValidationError: If the age group doesn't exist
        """
        if value and not AgeGroup.objects.filter(name=value).exists():
            raise DRFValidationError(
                {
                    "error": f"Invalid age_group parameter: '{value}' does not exist. Please provide a valid age group."
                }
            )
        return queryset.filter(**{name: value})

    def filter_sex(self, queryset, name, value):
        """
        Filter by sex and validate that the sex exists.

        Args:
            queryset: The queryset to filter
            name: The field name to filter on (sex__name)
            value: The value to filter by

        Returns:
            Filtered queryset

        Raises:
            ValidationError: If the sex doesn't exist
        """
        if value and not Sex.objects.filter(name=value).exists():
            raise DRFValidationError(
                {
                    "error": f"Invalid sex parameter: '{value}' does not exist. Please provide a valid sex (Male or Female)."
                }
            )
        return queryset.filter(**{name: value})

    def filter_hd_index(self, queryset, name, value):
        """
        Filter by HDI category and validate that the HDI category exists.

        Args:
            queryset: The queryset to filter
            name: The field name to filter on (hd_index__name)
            value: The value to filter by

        Returns:
            Filtered queryset

        Raises:
            ValidationError: If the HDI category doesn't exist
        """
        if value and not HDIndex.objects.filter(name=value).exists():
            raise DRFValidationError(
                {
                    "error": f"Invalid hd_index parameter: '{value}' does not exist. Please provide a valid HDI category."
                }
            )
        return queryset.filter(**{name: value})
