"""
Serializers for the demographics app.

This module contains serializers for the demographics app models,
including DemographicStatistic and related models.
"""

from rest_framework import serializers

from demographics.models import (
    AgeGroup,
    Sex,
    HDIndex,
    DemographicStatistic,
)


class AgeGroupSerializer(serializers.ModelSerializer):
    """Serializer for the AgeGroup model."""

    class Meta:
        model = AgeGroup
        fields = ["name", "is_aggregate"]


class SexSerializer(serializers.ModelSerializer):
    """Serializer for the Sex model."""

    class Meta:
        model = Sex
        fields = ["name", "is_aggregate"]


class HDIndexSerializer(serializers.ModelSerializer):
    """Serializer for the HDIndex model."""

    class Meta:
        model = HDIndex
        fields = ["name", "is_aggregate"]


class DemographicStatisticSerializer(serializers.ModelSerializer):
    """
    Serializer for the DemographicStatistic model.

    Includes nested representations of the related models and
    calculates the total for both sexes when applicable.
    """

    # Use string representation instead of primary keys
    age_group = serializers.CharField(source="age_group.name")
    sex = serializers.CharField(source="sex.name")
    hd_index = serializers.CharField(source="hd_index.name")

    # Field to hold the aggregated value for both sexes
    total_both_sexes = serializers.SerializerMethodField()

    class Meta:
        model = DemographicStatistic
        fields = ["year", "age_group", "sex", "hd_index", "value", "total_both_sexes"]

    def get_total_both_sexes(self, obj):
        """
        Calculate the total value for both sexes for this statistic.

        This method is used to populate the total_both_sexes field.
        It uses the model's class method to get the aggregated value.
        """
        # Only calculate if we have enough context (we need the age group and HDI)
        if hasattr(obj, "age_group") and hasattr(obj, "hd_index"):
            return DemographicStatistic.get_aggregated_by_both_sexes(
                year=obj.year, age_group=obj.age_group, hd_index=obj.hd_index
            )
        return None
