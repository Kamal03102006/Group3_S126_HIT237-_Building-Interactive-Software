from django.urls import path
from .views import (
    RepairRequestListView,
    RepairRequestDetailView,
    RepairRequestCreateView,
    RepairRequestUpdateView,
    MaintenanceUpdateCreateView,
)

urlpatterns = [
    path("", RepairRequestListView.as_view(), name="repairrequest-list"),
    path("repairs/<int:pk>/", RepairRequestDetailView.as_view(), name="repairrequest-detail"),
    path("repairs/new/", RepairRequestCreateView.as_view(), name="repairrequest-create"),
    path("repairs/<int:pk>/edit/", RepairRequestUpdateView.as_view(), name="repairrequest-update"),
    path("repairs/<int:pk>/updates/new/", MaintenanceUpdateCreateView.as_view(), name="maintenanceupdate-create"),
]