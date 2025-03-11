"""
Command to display statistics from the imported data.

This command shows a summary of the data that has been imported, providing
counts by categories and some sample data.
"""

from django.core.management.base import BaseCommand
from django.db.models import Count

from demographics.models import AgeGroup, Sex, HDIndex, DemographicStatistic


class Command(BaseCommand):
    """
    Django management command to display statistics from the imported data.
    """

    help = "Display statistics from the imported demographic data"

    def add_arguments(self, parser):
        """Add command line arguments."""
        parser.add_argument("--year", type=int, help="Filter statistics by year")
        parser.add_argument(
            "--limit",
            type=int,
            default=10,
            help="Number of records to display (default: 10)",
        )

    def handle(self, *args, **options):
        """Handle the command execution."""
        year = options.get("year")
        limit = options.get("limit")

        # Display counts by category
        self.stdout.write(self.style.NOTICE("DATA SUMMARY"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"Age Groups: {AgeGroup.objects.count()}")
        self.stdout.write(f"Sex Categories: {Sex.objects.count()}")
        self.stdout.write(f"HD Index Categories: {HDIndex.objects.count()}")

        # Total statistics count
        stats_query = DemographicStatistic.objects
        if year:
            stats_query = stats_query.filter(year=year)
            self.stdout.write(
                f"Total Statistics (for year {year}): {stats_query.count()}"
            )
        else:
            self.stdout.write(f"Total Statistics: {stats_query.count()}")

        # Display years in the database
        years = (
            DemographicStatistic.objects.values("year")
            .annotate(count=Count("id"))
            .order_by("year")
        )
        self.stdout.write("\nYears in database:")
        for year_data in years:
            self.stdout.write(f"  {year_data['year']}: {year_data['count']} records")

        # Display sample data
        self.stdout.write(f"\nSample Data (limited to {limit} records):")
        self.stdout.write("-" * 50)
        self.stdout.write(
            f"{'Year':<6} {'Age Group':<15} {'Sex':<8} {'HDI Category':<30} {'Value':<10}"
        )
        self.stdout.write("-" * 50)

        for stat in stats_query.select_related("age_group", "sex", "hd_index").order_by(
            "year", "age_group__name"
        )[:limit]:
            self.stdout.write(
                f"{stat.year:<6} {stat.age_group.name:<15} {stat.sex.name:<8} "
                f"{stat.hd_index.name:<30} {stat.value:<10}"
            )

        # Display some aggregated statistics
        if year:
            self.stdout.write("\nAggregation Example:")

            # Pick a non-aggregated age group for demonstration
            age_group = AgeGroup.objects.filter(is_aggregate=False).first()
            if age_group:
                # Get the HDI category for demonstration
                hd_index = HDIndex.objects.filter(is_aggregate=False).first()
                if hd_index:
                    # Get breakdown by sex
                    breakdown = DemographicStatistic.get_breakdown_by_sex(
                        year=year, age_group=age_group, hd_index=hd_index
                    )

                    # Get total for both sexes
                    total = DemographicStatistic.get_aggregated_by_both_sexes(
                        year=year, age_group=age_group, hd_index=hd_index
                    )

                    self.stdout.write(
                        f"\nFor {year}, {age_group.name}, {hd_index.name}:"
                    )
                    for sex_name, value in breakdown.items():
                        self.stdout.write(f"  {sex_name}: {value}")
                    self.stdout.write(f"  Total (both sexes): {total}")

        self.stdout.write("\nTo import more data, use:")
        self.stdout.write(
            "  python manage.py import_demographics --file=path/to/data.csv"
        )
        self.stdout.write("  or")
        self.stdout.write(
            "  python manage.py import_demographics --url=https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/PEA27/CSV/1.0/en"
        )
