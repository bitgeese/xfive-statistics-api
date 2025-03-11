"""
CSV importer for demographic statistics.

This module provides functionality to import demographic data from CSV files,
either locally or from a URL. It uses Python's built-in csv module for
CSV processing and httpx for URL-based requests.
"""

from __future__ import annotations

import csv
import logging
import os
import tempfile
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

import httpx
from django.db import transaction

from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic


# Set up logging
logger = logging.getLogger(__name__)


class DemographicsCSVImporter:
    """
    Importer for demographic statistics from CSV files.

    This class handles importing demographic data from CSV files, either from
    a local file or from a URL. It validates the data, skips aggregated rows,
    and saves the data to the database.
    """

    # The aggregated values that should be skipped
    AGGREGATED_VALUES = {
        "Age Group": ["All ages"],
        "Sex": ["-", "Both sexes"],  # In the data, "-" is used for "Both sexes"
        "Human Development Index Rating": [
            "10",
            "Human Development Index (HDI) - All ratings",
        ],
    }

    # Map sex codes to sex names
    SEX_MAPPING = {"1": "Male", "2": "Female", "-": "Both sexes"}

    # Map HDI codes to HDI names
    HDI_MAPPING = {
        "10": "Human Development Index (HDI) - All ratings",
        "20": "High Human Development Index (HDI)",
        "30": "Low Human Development Index (HDI)",
        "40": "Medium Human Development Index (HDI)",
        "50": "Very High Human Development Index (HDI)",
    }

    def skip_aggregated_row(self, row: Dict[str, str]) -> bool:
        """
        Check if a row contains aggregated values that should be skipped.

        Args:
            row: The row data as a dictionary.

        Returns:
            True if the row should be skipped, False otherwise.
        """
        for column, values in self.AGGREGATED_VALUES.items():
            if row.get(column) in values:
                return True
        return False

    def process_row(self, row: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Process a single row from the CSV file.

        This method extracts the relevant data from the row, validates it,
        and returns a dictionary with processed values if valid.

        Args:
            row: The row data as a dictionary.

        Returns:
            A dictionary with processed values if valid, None otherwise.
        """
        try:
            # Check for required fields
            required_fields = [
                "Year",
                "Age Group",
                "Sex",
                "Human Development Index Rating",
                "VALUE",
            ]
            for field in required_fields:
                if field not in row or not row[field]:
                    logger.warning(f"Missing required field: {field}")
                    return None

            # Extract and convert values
            year = int(row["Year"])
            age_group = row["Age Group"]

            # Handle sex mapping
            sex_code = row["Sex"]
            sex = self.SEX_MAPPING.get(sex_code, sex_code)

            # Extract HDI
            hdi_code = row["Human Development Index Rating"]
            hd_index = self.HDI_MAPPING.get(hdi_code, hdi_code)

            # Convert VALUE to integer
            try:
                value = int(row["VALUE"])
            except ValueError:
                logger.warning(f"Invalid VALUE: {row['VALUE']}")
                return None

            return {
                "year": year,
                "age_group": age_group,
                "sex": sex,
                "hd_index": hd_index,
                "value": value,
            }
        except Exception as e:
            logger.exception(f"Error processing row: {e}")
            return None

    @transaction.atomic
    def import_data(self, data: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Import data from a list of CSV rows.

        This method processes each row, skips aggregated rows, and saves
        the data to the database.

        Args:
            data: A list of dictionaries, each representing a row from the CSV.

        Returns:
            A dictionary with import statistics.
        """
        total_rows = len(data)
        skipped_rows = 0
        imported_rows = 0
        error_rows = []

        # Process each row
        for i, row in enumerate(data):
            row_num = i + 1  # 1-indexed for error reporting

            # Skip aggregated rows
            if self.skip_aggregated_row(row):
                skipped_rows += 1
                continue

            # Process the row
            processed = self.process_row(row)
            if processed is None:
                error_rows.append(row_num)
                continue

            try:
                # Get or create age group
                age_group, _ = AgeGroup.objects.get_or_create(
                    name=processed["age_group"],
                    defaults={"is_aggregate": processed["age_group"] == "All ages"},
                )

                # Get or create sex
                sex, _ = Sex.objects.get_or_create(
                    name=processed["sex"],
                    defaults={"is_aggregate": processed["sex"] == "Both sexes"},
                )

                # Get or create HDI
                hd_index, _ = HDIndex.objects.get_or_create(
                    name=processed["hd_index"],
                    defaults={
                        "is_aggregate": processed["hd_index"]
                        == "Human Development Index (HDI) - All ratings"
                    },
                )

                # Create demographic statistic
                DemographicStatistic.objects.update_or_create(
                    year=processed["year"],
                    age_group=age_group,
                    sex=sex,
                    hd_index=hd_index,
                    defaults={"value": processed["value"]},
                )

                imported_rows += 1

            except Exception as e:
                logger.exception(f"Error saving row {row_num}: {e}")
                error_rows.append(row_num)

        return {
            "success": True,
            "total_rows": total_rows,
            "skipped_rows": skipped_rows,
            "imported_rows": imported_rows,
            "error_rows": error_rows,
        }

    def import_from_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Import data from a local CSV file.

        Args:
            file_path: The path to the CSV file.

        Returns:
            A dictionary with import statistics.
        """
        try:
            # Convert to Path object if it's a string
            if isinstance(file_path, str):
                file_path = Path(file_path)

            # Check if the file exists
            if not file_path.exists():
                return {"success": False, "error": f"File not found: {file_path}"}

            # Read the file directly with Python's CSV reader
            with open(file_path, "r") as f:
                reader = csv.DictReader(f)
                data = list(reader)

            # Import the data
            return self.import_data(data)
        except Exception as e:
            logger.exception(f"Error importing from file: {e}")
            return {"success": False, "error": str(e)}

    def import_from_url(self, url: str) -> Dict[str, Any]:
        """
        Import data from a URL pointing to a CSV file.

        Args:
            url: The URL of the CSV file.

        Returns:
            A dictionary with import statistics.
        """
        try:
            # Get the CSV content from the URL
            response = httpx.get(url)

            # Check if the request was successful
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Failed to fetch CSV from URL: HTTP {response.status_code}",
                }

            # Write response content to a temporary file
            with tempfile.NamedTemporaryFile(
                mode="w+", delete=False, suffix=".csv"
            ) as temp_file:
                temp_file.write(response.text)
                temp_path = temp_file.name

            # Import from the temporary file
            result = self.import_from_file(temp_path)

            # Clean up
            os.unlink(temp_path)

            return result
        except Exception as e:
            logger.exception(f"Error importing from URL: {e}")
            return {"success": False, "error": str(e)}
