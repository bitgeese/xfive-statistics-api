import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from django.core.management import call_command
from io import StringIO

from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic
from demographics.importers import DemographicsCSVImporter


# Mark all tests as requiring database access
pytestmark = pytest.mark.django_db


class TestDemographicsCSVImporter:
    """Tests for the DemographicsCSVImporter class."""

    @pytest.fixture
    def sample_csv_path(self):
        """Returns the path to the sample CSV file."""
        return Path(__file__).parent / "fixtures" / "sample_demographics.csv"

    @pytest.fixture
    def importer(self):
        """Returns an instance of DemographicsCSVImporter."""
        return DemographicsCSVImporter()

    def test_process_row(self, importer):
        """Test processing a single row from the CSV."""
        # Sample row from the CSV file
        row = {
            "Year": "2023",
            "Age Group": "0 - 4 years",
            "Sex": "1",  # Using code for "Male"
            "Human Development Index Rating": "20",  # Using code for "High Human Development Index (HDI)"
            "VALUE": "1000",
        }

        # Process the row
        processed = importer.process_row(row)

        # Check the processed data
        assert processed is not None
        assert processed["year"] == 2023
        assert processed["age_group"] == "0 - 4 years"
        assert processed["sex"] == "Male"
        assert processed["hd_index"] == "High Human Development Index (HDI)"
        assert processed["value"] == 1000

    def test_skip_aggregated_rows(self, importer):
        """Test that aggregated rows are skipped."""
        # Row with aggregated age group
        row1 = {
            "Year": "2023",
            "Age Group": "All ages",
            "Sex": "1",  # Male
            "Human Development Index Rating": "20",  # High HDI
            "VALUE": "1000",
        }

        # Row with aggregated sex
        row2 = {
            "Year": "2023",
            "Age Group": "0 - 4 years",
            "Sex": "-",  # Both sexes
            "Human Development Index Rating": "20",  # High HDI
            "VALUE": "1000",
        }

        # Row with aggregated HDI
        row3 = {
            "Year": "2023",
            "Age Group": "0 - 4 years",
            "Sex": "1",  # Male
            "Human Development Index Rating": "10",  # All ratings
            "VALUE": "1000",
        }

        # Test skip_aggregated_row for each case
        assert importer.skip_aggregated_row(row1) is True
        assert importer.skip_aggregated_row(row2) is True
        assert importer.skip_aggregated_row(row3) is True

        # Row with no aggregated values
        row4 = {
            "Year": "2023",
            "Age Group": "0 - 4 years",
            "Sex": "1",  # Male
            "Human Development Index Rating": "20",  # High HDI
            "VALUE": "1000",
        }

        assert importer.skip_aggregated_row(row4) is False

    def test_import_from_file(self, importer, sample_csv_path):
        """Test importing data from a CSV file."""
        # Import data from the sample CSV file
        result = importer.import_from_file(sample_csv_path)

        # Check results
        assert result["success"] is True
        assert result["total_rows"] > 0
        assert result["skipped_rows"] > 0
        assert result["imported_rows"] > 0

        # Check that the data was imported into the database
        assert AgeGroup.objects.count() > 0
        assert Sex.objects.count() > 0
        assert HDIndex.objects.count() > 0
        assert DemographicStatistic.objects.count() > 0

    @patch("httpx.get")
    def test_import_from_url(self, mock_get, importer, sample_csv_path):
        """Test importing data from a URL."""
        # Mock the response from httpx.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        with open(sample_csv_path, "r") as f:
            mock_response.text = f.read()
        mock_get.return_value = mock_response

        # Import data from a mock URL
        result = importer.import_from_url("https://example.com/data.csv")

        # Check results
        assert result["success"] is True
        assert result["total_rows"] > 0
        assert result["skipped_rows"] > 0
        assert result["imported_rows"] > 0

        # Check that the data was imported into the database
        assert AgeGroup.objects.count() > 0
        assert Sex.objects.count() > 0
        assert HDIndex.objects.count() > 0
        assert DemographicStatistic.objects.count() > 0

    @patch("httpx.get")
    def test_import_from_url_failure(self, mock_get, importer):
        """Test handling of failed URL imports."""
        # Mock a failed response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Import data from a mock URL that returns a 404
        result = importer.import_from_url("https://example.com/nonexistent.csv")

        # Check results
        assert result["success"] is False
        assert "error" in result

    def test_handle_invalid_data(self, importer):
        """Test handling of invalid data."""
        # Row with non-numeric value
        row1 = {
            "Year": "2023",
            "Age Group": "0 - 4 years",
            "Sex": "1",
            "Human Development Index Rating": "20",
            "VALUE": "not-a-number",
        }

        # Process the row
        processed1 = importer.process_row(row1)
        assert processed1 is None

        # Row with missing required fields
        row2 = {
            "Year": "2023",
            "Age Group": "0 - 4 years",
            # Missing "Sex"
            "Human Development Index Rating": "20",
            "VALUE": "1000",
        }

        # Process the row
        processed2 = importer.process_row(row2)
        assert processed2 is None


class TestImportCommand:
    """Tests for the import_demographics management command."""

    @pytest.fixture
    def sample_csv_path(self):
        """Returns the path to the sample CSV file."""
        return Path(__file__).parent / "fixtures" / "sample_demographics.csv"

    def test_command_file_import(self, sample_csv_path):
        """Test the command with a file import."""
        out = StringIO()
        call_command("import_demographics", f"--file={sample_csv_path}", stdout=out)

        # Check output
        output = out.getvalue()
        assert "successfully" in output.lower()
        assert "imported" in output.lower()

        # Check database entries
        assert AgeGroup.objects.count() > 0
        assert Sex.objects.count() > 0
        assert HDIndex.objects.count() > 0
        assert DemographicStatistic.objects.count() > 0

    @patch(
        "demographics.management.commands.import_demographics.DemographicsCSVImporter.import_from_url"
    )
    def test_command_url_import(self, mock_import_from_url):
        """Test the command with a URL import."""
        # Mock the import_from_url method
        mock_import_from_url.return_value = {
            "success": True,
            "total_rows": 20,
            "skipped_rows": 10,
            "imported_rows": 10,
            "error_rows": [],
        }

        out = StringIO()
        call_command(
            "import_demographics", "--url=https://example.com/data.csv", stdout=out
        )

        # Check that the import_from_url method was called
        mock_import_from_url.assert_called_once_with("https://example.com/data.csv")

        # Check output
        output = out.getvalue()
        assert "successfully" in output.lower()
        assert "imported" in output.lower()
