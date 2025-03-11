"""
URL patterns for the visualization app.

This module contains URL patterns for the visualization app,
including dashboard and visualization views.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("import-file/", views.import_file, name="import_file"),
    path("import-url/", views.import_url, name="import_url"),
    path("clean-database/", views.clean_database, name="clean_database"),
]
