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
        """Test creating an HDI entry."""
        from demographics.models import HDIndex

        hd_index = HDIndex.objects.create(
            name=hd_index_data[0]["name"], is_aggregate=hd_index_data[0]["is_aggregate"]
        )

        assert hd_index.name == hd_index_data[0]["name"]
        assert hd_index.is_aggregate == hd_index_data[0]["is_aggregate"]
        assert str(hd_index) == hd_index_data[0]["name"]

    def test_unique_name_constraint(self, hd_index_data):
        """Test that HDI names must be unique."""
        from demographics.models import HDIndex

        HDIndex.objects.create(
            name=hd_index_data[0]["name"], is_aggregate=hd_index_data[0]["is_aggregate"]
        )

        with pytest.raises(IntegrityError):
            HDIndex.objects.create(
                name=hd_index_data[0]["name"],
                is_aggregate=hd_index_data[0]["is_aggregate"],
            )


class TestDemographicStatisticModel:
    """Tests for the DemographicStatistic model."""

    def test_create_demographic_statistic(
        self, age_group_data, sex_data, hd_index_data
    ):
        """Test creating a demographic statistic."""
        from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic

        # Create related objects
        age_group = AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )
        sex = Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )
        hd_index = HDIndex.objects.create(
            name=hd_index_data[0]["name"], is_aggregate=hd_index_data[0]["is_aggregate"]
        )

        # Create the statistic
        statistic = DemographicStatistic.objects.create(
            year=2023,
            age_group=age_group,
            sex=sex,
            hd_index=hd_index,
            value=1000,
        )

        # Check the values
        assert statistic.year == 2023
        assert statistic.age_group == age_group
        assert statistic.sex == sex
        assert statistic.hd_index == hd_index
        assert statistic.value == 1000
        assert "2023" in str(statistic)
        assert age_group.name in str(statistic)
        assert sex.name in str(statistic)
        assert hd_index.name in str(statistic)
        assert "1000" in str(statistic)

    def test_unique_combination_constraint(
        self, age_group_data, sex_data, hd_index_data
    ):
        """Test that the combination of year, age_group, sex, and hd_index must be unique."""
        from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic

        # Create related objects
        age_group = AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )
        sex = Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )
        hd_index = HDIndex.objects.create(
            name=hd_index_data[0]["name"], is_aggregate=hd_index_data[0]["is_aggregate"]
        )

        # Create the first statistic
        DemographicStatistic.objects.create(
            year=2023,
            age_group=age_group,
            sex=sex,
            hd_index=hd_index,
            value=1000,
        )

        # Attempting to create a duplicate should raise a ValidationError
        # Note: Django validates uniqueness constraints with full_clean before trying to insert
        with pytest.raises(ValidationError):
            duplicate = DemographicStatistic(
                year=2023,
                age_group=age_group,
                sex=sex,
                hd_index=hd_index,
                value=2000,  # Different value, but same combination of other fields
            )
            duplicate.full_clean()

    def test_positive_value_constraint(self, age_group_data, sex_data, hd_index_data):
        """Test that the value must be positive."""
        from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic

        # Create related objects
        age_group = AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )
        sex = Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )
        hd_index = HDIndex.objects.create(
            name=hd_index_data[0]["name"], is_aggregate=hd_index_data[0]["is_aggregate"]
        )

        # Attempting to create a statistic with a negative value should raise a ValidationError
        with pytest.raises(ValueError):
            DemographicStatistic.objects.create(
                year=2023,
                age_group=age_group,
                sex=sex,
                hd_index=hd_index,
                value=-1000,  # Negative value
            )

    def test_filter_statistics_method(self, age_group_data, sex_data, hd_index_data):
        """Test the filter_statistics method."""
        from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic

        # Create related objects
        age_group1 = AgeGroup.objects.create(
            name=age_group_data[0]["name"],
            is_aggregate=age_group_data[0]["is_aggregate"],
        )
        age_group2 = AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )

        male = Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )
        female = Sex.objects.create(
            name=sex_data[1]["name"], is_aggregate=sex_data[1]["is_aggregate"]
        )

        hd_index1 = HDIndex.objects.create(
            name=hd_index_data[0]["name"], is_aggregate=hd_index_data[0]["is_aggregate"]
        )
        hd_index2 = HDIndex.objects.create(
            name=hd_index_data[1]["name"], is_aggregate=hd_index_data[1]["is_aggregate"]
        )

        # Create statistics
        DemographicStatistic.objects.create(
            year=2022, age_group=age_group1, sex=male, hd_index=hd_index1, value=100
        )
        DemographicStatistic.objects.create(
            year=2022, age_group=age_group1, sex=female, hd_index=hd_index1, value=150
        )
        DemographicStatistic.objects.create(
            year=2023, age_group=age_group1, sex=male, hd_index=hd_index1, value=200
        )
        DemographicStatistic.objects.create(
            year=2023, age_group=age_group2, sex=male, hd_index=hd_index2, value=300
        )

        # Test filtering by year
        year_filtered = DemographicStatistic.filter_statistics(year=2023)
        assert year_filtered.count() == 2

        # Test filtering by age_group object
        age_filtered = DemographicStatistic.filter_statistics(age_group=age_group1)
        assert age_filtered.count() == 3

        # Test filtering by age_group name
        age_name_filtered = DemographicStatistic.filter_statistics(
            age_group=age_group1.name
        )
        assert age_name_filtered.count() == 3

        # Test filtering by sex object
        sex_filtered = DemographicStatistic.filter_statistics(sex=male)
        assert sex_filtered.count() == 3

        # Test filtering by sex name
        sex_name_filtered = DemographicStatistic.filter_statistics(sex=male.name)
        assert sex_name_filtered.count() == 3

        # Test filtering by hd_index object
        hdi_filtered = DemographicStatistic.filter_statistics(hd_index=hd_index1)
        assert hdi_filtered.count() == 3

        # Test filtering by hd_index name
        hdi_name_filtered = DemographicStatistic.filter_statistics(
            hd_index=hd_index1.name
        )
        assert hdi_name_filtered.count() == 3

        # Test combined filtering
        combined_filtered = DemographicStatistic.filter_statistics(
            year=2023, age_group=age_group1, sex=male
        )
        assert combined_filtered.count() == 1
        assert combined_filtered.first().value == 200

    def test_clean_method(self, age_group_data, sex_data, hd_index_data):
        """Test the clean method enforces validation rules."""
        from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic

        # Create related objects
        age_group = AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )
        sex = Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )
        hd_index = HDIndex.objects.create(
            name=hd_index_data[0]["name"], is_aggregate=hd_index_data[0]["is_aggregate"]
        )

        # Create a valid statistic
        statistic = DemographicStatistic(
            year=2023,
            age_group=age_group,
            sex=sex,
            hd_index=hd_index,
            value=1000,
        )

        # This should not raise any errors
        statistic.clean()

        # Now set a negative value
        statistic.value = -10

        # This should raise a ValueError
        with pytest.raises(ValueError):
            statistic.clean()

    def test_save_method_calls_clean(self, age_group_data, sex_data, hd_index_data):
        """Test that the save method calls clean to validate the object."""
        from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic

        # Create related objects
        age_group = AgeGroup.objects.create(
            name=age_group_data[1]["name"],
            is_aggregate=age_group_data[1]["is_aggregate"],
        )
        sex = Sex.objects.create(
            name=sex_data[0]["name"], is_aggregate=sex_data[0]["is_aggregate"]
        )
        hd_index = HDIndex.objects.create(
            name=hd_index_data[0]["name"], is_aggregate=hd_index_data[0]["is_aggregate"]
        )

        # Create a statistic with invalid data
        statistic = DemographicStatistic(
            year=2023,
            age_group=age_group,
            sex=sex,
            hd_index=hd_index,
            value=-1000,  # Negative value
        )

        # Attempting to save should raise an exception
        with pytest.raises(ValueError):
            statistic.save()
