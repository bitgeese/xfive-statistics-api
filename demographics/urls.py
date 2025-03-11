"""
URL patterns for the demographics app.

This module contains URL patterns for the demographics app API endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from demographics.views import DemographicStatisticViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r"demographics", DemographicStatisticViewSet, basename="demographics")

# The API URLs are determined automatically by the router
urlpatterns = [
    path("", include(router.urls)),
]
