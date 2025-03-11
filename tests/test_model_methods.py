import pytest
from django.db.models import Sum

# Mark the test as using the Django database
pytestmark = pytest.mark.django_db


class TestDemographicStatisticMethods:
    """Tests for the methods on the DemographicStatistic model"""

    @pytest.fixture
    def setup_data(self, age_group_data, sex_data, hd_index_data):
        """Set up test data."""
        from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic
        
        # Create age groups
        age_groups = {}
        for data in age_group_data:
            age_groups[data["name"]] = AgeGroup.objects.create(
                name=data["name"],
                is_aggregate=data["is_aggregate"]
            )
        
        # Create sex categories
        sexes = {}
        for data in sex_data:
            sexes[data["name"]] = Sex.objects.create(
                name=data["name"],
                is_aggregate=data["is_aggregate"]
            )
        
        # Create HD index categories
        hd_indices = {}
        for data in hd_index_data:
            hd_indices[data["name"]] = HDIndex.objects.create(
                name=data["name"],
                is_aggregate=data["is_aggregate"]
            )
        
        # Create some statistics
        # Male, 0-4 years, High HDI: 1000
        DemographicStatistic.objects.create(
            year=2023,
            age_group=age_groups["0 - 4 years"],
            sex=sexes["Male"],
            hd_index=hd_indices["High Human Development Index (HDI)"],
            value=1000
        )
        
        # Female, 0-4 years, High HDI: 900
        DemographicStatistic.objects.create(
            year=2023,
            age_group=age_groups["0 - 4 years"],
            sex=sexes["Female"],
            hd_index=hd_indices["High Human Development Index (HDI)"],
            value=900
        )
        
        # Male, 5-9 years, High HDI: 800
        DemographicStatistic.objects.create(
            year=2023,
            age_group=age_groups["5 - 9 years"],
            sex=sexes["Male"],
            hd_index=hd_indices["High Human Development Index (HDI)"],
            value=800
        )
        
        # Female, 5-9 years, High HDI: 700
        DemographicStatistic.objects.create(
            year=2023,
            age_group=age_groups["5 - 9 years"],
            sex=sexes["Female"],
            hd_index=hd_indices["High Human Development Index (HDI)"],
            value=700
        )
        
        return {
            "age_groups": age_groups,
            "sexes": sexes,
            "hd_indices": hd_indices
        }

    def test_get_aggregated_by_both_sexes(self, setup_data):
        """Test getting statistics aggregated by both sexes."""
        from demographics.models import DemographicStatistic
        
        age_group = setup_data["age_groups"]["0 - 4 years"]
        hd_index = setup_data["hd_indices"]["High Human Development Index (HDI)"]
        
        # Get statistics for both sexes
        total = DemographicStatistic.get_aggregated_by_both_sexes(
            year=2023,
            age_group=age_group,
            hd_index=hd_index
        )
        
        # Should be 1000 (Male) + 900 (Female) = 1900
        assert total == 1900

    def test_get_aggregated_by_all_ages(self, setup_data):
        """Test getting statistics aggregated by all ages."""
        from demographics.models import DemographicStatistic
        
        sex = setup_data["sexes"]["Male"]
        hd_index = setup_data["hd_indices"]["High Human Development Index (HDI)"]
        
        # Get statistics for all ages
        total = DemographicStatistic.get_aggregated_by_all_ages(
            year=2023,
            sex=sex,
            hd_index=hd_index
        )
        
        # Should be 1000 (0-4 years) + 800 (5-9 years) = 1800
        assert total == 1800

    def test_get_aggregated_by_all_hdi(self, setup_data):
        """Test getting statistics aggregated by all HDI categories."""
        from demographics.models import DemographicStatistic, HDIndex
        
        # Create statistics for a different HDI category
        age_group = setup_data["age_groups"]["0 - 4 years"]
        sex = setup_data["sexes"]["Male"]
        low_hdi = setup_data["hd_indices"]["Low Human Development Index (HDI)"]
        
        DemographicStatistic.objects.create(
            year=2023,
            age_group=age_group,
            sex=sex,
            hd_index=low_hdi,
            value=500
        )
        
        # Get statistics for all HDI categories
        total = DemographicStatistic.get_aggregated_by_all_hdi(
            year=2023,
            age_group=age_group,
            sex=sex
        )
        
        # Should be 1000 (High HDI) + 500 (Low HDI) = 1500
        assert total == 1500

    def test_get_breakdown_by_sex(self, setup_data):
        """Test getting a breakdown of statistics by sex."""
        from demographics.models import DemographicStatistic
        
        age_group = setup_data["age_groups"]["0 - 4 years"]
        hd_index = setup_data["hd_indices"]["High Human Development Index (HDI)"]
        
        # Get breakdown by sex
        breakdown = DemographicStatistic.get_breakdown_by_sex(
            year=2023,
            age_group=age_group,
            hd_index=hd_index
        )
        
        # Should have entries for Male (1000) and Female (900)
        assert len(breakdown) == 2
        assert breakdown["Male"] == 1000
        assert breakdown["Female"] == 900 