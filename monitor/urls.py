from django.urls import path

from .views import CurrentUsageView, UsageView

urlpatterns = [
    path('usage/', UsageView.as_view(), name='usage'),
    path('usage/current/', CurrentUsageView.as_view(), name='current_usage'),
]
