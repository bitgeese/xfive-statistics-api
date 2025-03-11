from django.contrib import admin
from django.db.models import Sum
from .models import AgeGroup, Sex, HDIndex, DemographicStatistic


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    """Admin configuration for AgeGroup model."""
    list_display = ('name', 'is_aggregate')
    list_filter = ('is_aggregate',)
    search_fields = ('name',)


@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    """Admin configuration for Sex model."""
    list_display = ('name', 'is_aggregate')
    list_filter = ('is_aggregate',)
    search_fields = ('name',)


@admin.register(HDIndex)
class HDIndexAdmin(admin.ModelAdmin):
    """Admin configuration for HDIndex model."""
    list_display = ('name', 'is_aggregate')
    list_filter = ('is_aggregate',)
    search_fields = ('name',)


@admin.register(DemographicStatistic)
class DemographicStatisticAdmin(admin.ModelAdmin):
    """Admin configuration for DemographicStatistic model."""
    list_display = ('year', 'age_group', 'sex', 'hd_index', 'value')
    list_filter = ('year', 'age_group', 'sex', 'hd_index')
    search_fields = ('year', 'age_group__name', 'sex__name', 'hd_index__name')
    readonly_fields = ('computed_total',)
    
    def computed_total(self, obj):
        """
        Display computed total for both sexes if viewing a single sex entry.
        """
        if obj.sex.is_aggregate:
            return "Already an aggregate value"
        
        total = DemographicStatistic.get_aggregated_by_both_sexes(
            year=obj.year,
            age_group=obj.age_group,
            hd_index=obj.hd_index
        )
        return f"{total} (computed total for both sexes)"
    
    computed_total.short_description = "Computed Total"
