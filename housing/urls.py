from django.urls import path
from .views import (
    DwellingListView,
    RepairRequestListView,
    RepairRequestDetailView,
    RepairRequestCreateView,
    RepairRequestUpdateView,
    RepairRequestDeleteView,
)

urlpatterns = [
    path("", RepairRequestListView.as_view(), name="repairrequest-list"),
    path("houses/", DwellingListView.as_view(), name="dwelling-list"),
    path("repairs/<int:pk>/", RepairRequestDetailView.as_view(), name="repairrequest-detail"),
    path("repairs/create/", RepairRequestCreateView.as_view(), name="repairrequest-create"),
    path("repairs/<int:pk>/edit/", RepairRequestUpdateView.as_view(), name="repairrequest-update"),
    path("repairs/<int:pk>/delete/", RepairRequestDeleteView.as_view(), name="repairrequest-delete"),
]