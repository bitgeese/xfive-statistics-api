"""
Management command to import demographic data from CSV.

Usage:
    python manage.py import_demographics --file=/path/to/file.csv
    python manage.py import_demographics --url=https://example.com/data.csv
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from demographics.importers import DemographicsCSVImporter


class Command(BaseCommand):
    """
    Django management command for importing demographic data from CSV files.

    This command can import data from either a local file or a URL.
    """

    help = "Import demographic statistics from a CSV file or URL"

    def add_arguments(self, parser):
        """Add command line arguments."""
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--file", type=str, help="Path to the CSV file to import")
        group.add_argument("--url", type=str, help="URL of the CSV file to import")

    def handle(self, *args, **options):
        """Handle the command execution."""
        start_time = timezone.now()
        importer = DemographicsCSVImporter()

        if options["file"]:
            self.stdout.write(f"Importing data from file: {options['file']}")
            result = importer.import_from_file(options["file"])
        elif options["url"]:
            self.stdout.write(f"Importing data from URL: {options['url']}")
            result = importer.import_from_url(options["url"])
        else:
            raise CommandError("Either --file or --url must be provided")

        if result["success"]:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully imported demographic data:\n"
                    f"- Total rows: {result['total_rows']}\n"
                    f"- Skipped rows (aggregated): {result['skipped_rows']}\n"
                    f"- Imported rows: {result['imported_rows']}\n"
                    f"- Error rows: {len(result.get('error_rows', []))}"
                )
            )

            if result.get("error_rows"):
                self.stdout.write(
                    self.style.WARNING(
                        f"Errors occurred in the following rows: {', '.join(map(str, result['error_rows']))}"
                    )
                )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to import data: {result.get('error', 'Unknown error')}"
                )
            )

        end_time = timezone.now()
        duration = (end_time - start_time).total_seconds()
        self.stdout.write(f"Import completed in {duration:.2f} seconds")
