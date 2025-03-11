import pytest
from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Ensure the database is properly set up for testing.
    This will run migrations and make the database ready for testing.
    """
    with django_db_blocker.unblock():
        # Any initial data setup can go here
        pass


@pytest.fixture
def age_group_data():
    """
    Fixture providing sample age group data for testing.
    """
    return [
        {"name": "All ages", "is_aggregate": True},
        {"name": "0 - 4 years", "is_aggregate": False},
        {"name": "5 - 9 years", "is_aggregate": False},
        {"name": "10 - 14 years", "is_aggregate": False},
    ]


@pytest.fixture
def sex_data():
    """
    Fixture providing sample sex data for testing.
    """
    return [
        {"name": "Male", "is_aggregate": False},
        {"name": "Female", "is_aggregate": False},
        {"name": "Both sexes", "is_aggregate": True},
    ]


@pytest.fixture
def hd_index_data():
    """
    Fixture providing sample Human Development Index data for testing.
    """
    return [
        {"name": "Human Development Index (HDI) - All ratings", "is_aggregate": True},
        {"name": "High Human Development Index (HDI)", "is_aggregate": False},
        {"name": "Medium Human Development Index (HDI)", "is_aggregate": False},
        {"name": "Low Human Development Index (HDI)", "is_aggregate": False},
        {"name": "Very High Human Development Index (HDI)", "is_aggregate": False},
    ]
