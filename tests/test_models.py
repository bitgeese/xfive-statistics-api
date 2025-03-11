import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# Mark the test as using the Django database
pytestmark = pytest.mark.django_db


class TestAgeGroupModel:
    """Tests for the AgeGroup model."""

    def test_create_age_group(self, age_group_data):
        """Test creating an age group."""
        from demographics.models import AgeGroup

        age_group = AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )

        assert age_group.name == age_group_data[1]["name"]
        assert age_group.is_aggregate == age_group_data[1]["is_aggregate"]
        assert str(age_group) == age_group_data[1]["name"]

    def test_unique_name_constraint(self, age_group_data):
        """Test that age group names must be unique."""
        from demographics.models import AgeGroup

        AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )

        with pytest.raises(IntegrityError):
            AgeGroup.objects.create(
                name=age_group_data[1]["name"],
                is_aggregate=age_group_data[1]["is_aggregate"],
            )


class TestSexModel:
    """Tests for the Sex model."""

    def test_create_sex(self, sex_data):
        """Test creating a sex entry."""
        from demographics.models import Sex

        sex = Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )

        assert sex.name == sex_data[0]["name"]
        assert sex.is_aggregate == sex_data[0]["is_aggregate"]
        assert str(sex) == sex_data[0]["name"]

    def test_unique_name_constraint(self, sex_data):
        """Test that sex names must be unique."""
        from demographics.models import Sex

        Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )

        with pytest.raises(IntegrityError):
            Sex.objects.create(
                name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
            )


class TestHDIndexModel:
    """Tests for the HDIndex model."""

    def test_create_hd_index(self, hd_index_data):
        """Test creating an HDIndex entry."""
        from demographics.models import HDIndex

        hd_index = HDIndex.objects.create(
            name=hd_index_data[1]["name"], is_aggregate=hd_index_data[1]["is_aggregate"]
        )

        assert hd_index.name == hd_index_data[1]["name"]
        assert hd_index.is_aggregate == hd_index_data[1]["is_aggregate"]
        assert str(hd_index) == hd_index_data[1]["name"]

    def test_unique_name_constraint(self, hd_index_data):
        """Test that HDIndex names must be unique."""
        from demographics.models import HDIndex

        HDIndex.objects.create(
            name=hd_index_data[1]["name"], is_aggregate=hd_index_data[1]["is_aggregate"]
        )

        with pytest.raises(IntegrityError):
            HDIndex.objects.create(
                name=hd_index_data[1]["name"],
                is_aggregate=hd_index_data[1]["is_aggregate"],
            )


class TestDemographicStatisticModel:
    """Tests for the DemographicStatistic model."""

    def test_create_demographic_statistic(
        self, age_group_data, sex_data, hd_index_data
    ):
        """Test creating a demographic statistic."""
        from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic

        age_group = AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )
        sex = Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )
        hd_index = HDIndex.objects.create(
            name=hd_index_data[1]["name"], is_aggregate=hd_index_data[1]["is_aggregate"]
        )

        stat = DemographicStatistic.objects.create(
            year=2023, age_group=age_group, sex=sex, hd_index=hd_index, value=1000
        )

        assert stat.year == 2023
        assert stat.age_group == age_group
        assert stat.sex == sex
        assert stat.hd_index == hd_index
        assert stat.value == 1000
        assert (
            str(stat) == f"2023 - {age_group.name} - {sex.name} - {hd_index.name}: 1000"
        )

    def test_unique_combination_constraint(
        self, age_group_data, sex_data, hd_index_data
    ):
        """Test that the combination of year, age_group, sex, and hd_index must be unique."""
        from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic

        age_group = AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )
        sex = Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )
        hd_index = HDIndex.objects.create(
            name=hd_index_data[1]["name"], is_aggregate=hd_index_data[1]["is_aggregate"]
        )

        DemographicStatistic.objects.create(
            year=2023, age_group=age_group, sex=sex, hd_index=hd_index, value=1000
        )

        with pytest.raises(ValidationError):
            DemographicStatistic.objects.create(
                year=2023, age_group=age_group, sex=sex, hd_index=hd_index, value=2000
            )

    def test_positive_value_constraint(self, age_group_data, sex_data, hd_index_data):
        """Test that value must be positive."""
        from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic

        age_group = AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )
        sex = Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )
        hd_index = HDIndex.objects.create(
            name=hd_index_data[1]["name"], is_aggregate=hd_index_data[1]["is_aggregate"]
        )

        with pytest.raises(ValueError):
            DemographicStatistic.objects.create(
                year=2023, age_group=age_group, sex=sex, hd_index=hd_index, value=-1000
            )
