from __future__ import annotations
from typing import Dict, Optional, Any, Union

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, QuerySet


class BaseCategory(models.Model):
    """
    Base abstract model for demographic categories.

    This model provides common fields and methods for all demographic categories
    such as age groups, sex, and human development index ratings.
    """

    name = models.CharField(max_length=255, unique=True)
    is_aggregate = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class AgeGroup(BaseCategory):
    """
    Model representing different age group categories.

    Examples: "All ages", "0 - 4 years", "5 - 9 years"
    """

    class Meta:
        verbose_name = "Age Group"
        verbose_name_plural = "Age Groups"


class Sex(BaseCategory):
    """
    Model representing different sex categories.

    Examples: "Male", "Female", "Both sexes"
    """

    class Meta:
        verbose_name = "Sex"
        verbose_name_plural = "Sexes"


class HDIndex(BaseCategory):
    """
    Model representing different Human Development Index categories.

    Examples: "Human Development Index (HDI) - All ratings", "High Human Development Index (HDI)"
    """

    class Meta:
        verbose_name = "Human Development Index"
        verbose_name_plural = "Human Development Indices"


class DemographicStatistic(models.Model):
    """
    Model representing demographic statistics for a specific combination of
    year, age group, sex, and human development index.
    """

    year = models.PositiveIntegerField()
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)
    hd_index = models.ForeignKey(HDIndex, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "Demographic Statistic"
        verbose_name_plural = "Demographic Statistics"
        # Ensure no duplicate combinations of year, age_group, sex, and hd_index
        constraints = [
            models.UniqueConstraint(
                fields=["year", "age_group", "sex", "hd_index"],
                name="unique_demographic_statistic",
            )
        ]
        # Add index for common queries
        indexes = [
            models.Index(fields=["year"]),
            models.Index(fields=["year", "age_group"]),
            models.Index(fields=["year", "sex"]),
            models.Index(fields=["year", "hd_index"]),
        ]

    def __str__(self) -> str:
        return f"{self.year} - {self.age_group.name} - {self.sex.name} - {self.hd_index.name}: {self.value}"

    def clean(self) -> None:
        """
        Validate the model instance.

        Raises:
            ValueError: If value is negative.
        """
        super().clean()
        if self.value < 0:
            raise ValueError("Value cannot be negative")

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Save the model instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ValueError: If value is negative.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def get_aggregated_by_both_sexes(
        cls, year: int, age_group: AgeGroup, hd_index: HDIndex
    ) -> int:
        """
        Get the total value aggregated for both sexes for a given year, age group, and HDI category.

        Args:
            year: The year to filter by.
            age_group: The age group to filter by.
            hd_index: The HDI category to filter by.

        Returns:
            The aggregated value for both sexes.
        """
        result = cls.objects.filter(
            year=year,
            age_group=age_group,
            hd_index=hd_index,
            sex__is_aggregate=False,  # Exclude 'Both sexes' to avoid double counting
        ).aggregate(total=Sum("value"))

        return result["total"] or 0

    @classmethod
    def get_aggregated_by_all_ages(cls, year: int, sex: Sex, hd_index: HDIndex) -> int:
        """
        Get the total value aggregated for all age groups for a given year, sex, and HDI category.

        Args:
            year: The year to filter by.
            sex: The sex category to filter by.
            hd_index: The HDI category to filter by.

        Returns:
            The aggregated value for all age groups.
        """
        result = cls.objects.filter(
            year=year,
            sex=sex,
            hd_index=hd_index,
            age_group__is_aggregate=False,  # Exclude 'All ages' to avoid double counting
        ).aggregate(total=Sum("value"))

        return result["total"] or 0

    @classmethod
    def get_aggregated_by_all_hdi(cls, year: int, age_group: AgeGroup, sex: Sex) -> int:
        """
        Get the total value aggregated for all HDI categories for a given year, age group, and sex.

        Args:
            year: The year to filter by.
            age_group: The age group to filter by.
            sex: The sex category to filter by.

        Returns:
            The aggregated value for all HDI categories.
        """
        result = cls.objects.filter(
            year=year,
            age_group=age_group,
            sex=sex,
            hd_index__is_aggregate=False,  # Exclude 'All ratings' to avoid double counting
        ).aggregate(total=Sum("value"))

        return result["total"] or 0

    @classmethod
    def get_breakdown_by_sex(
        cls, year: int, age_group: AgeGroup, hd_index: HDIndex
    ) -> Dict[str, int]:
        """
        Get a breakdown of values by sex for a given year, age group, and HDI category.

        Args:
            year: The year to filter by.
            age_group: The age group to filter by.
            hd_index: The HDI category to filter by.

        Returns:
            A dictionary mapping sex names to their respective values.
        """
        stats = cls.objects.filter(
            year=year,
            age_group=age_group,
            hd_index=hd_index,
            sex__is_aggregate=False,  # Exclude 'Both sexes' to get individual breakdowns
        ).select_related("sex")

        return {stat.sex.name: stat.value for stat in stats}

    @classmethod
    def filter_statistics(
        cls,
        year: Optional[int] = None,
        age_group: Optional[Union[AgeGroup, str]] = None,
        sex: Optional[Union[Sex, str]] = None,
        hd_index: Optional[Union[HDIndex, str]] = None,
    ) -> QuerySet:
        """
        Filter statistics based on the provided parameters.

        Any parameter that is None will not be used for filtering.

        Args:
            year: The year to filter by.
            age_group: The age group to filter by (either an AgeGroup object or a string name).
            sex: The sex category to filter by (either a Sex object or a string name).
            hd_index: The HDI category to filter by (either an HDIndex object or a string name).

        Returns:
            A queryset of filtered DemographicStatistic objects.
        """
        filters = {}

        if year is not None:
            filters["year"] = year

        if age_group is not None:
            if isinstance(age_group, str):
                filters["age_group__name"] = age_group
            else:
                filters["age_group"] = age_group

        if sex is not None:
            if isinstance(sex, str):
                filters["sex__name"] = sex
            else:
                filters["sex"] = sex

        if hd_index is not None:
            if isinstance(hd_index, str):
                filters["hd_index__name"] = hd_index
            else:
                filters["hd_index"] = hd_index

        return cls.objects.filter(**filters)
