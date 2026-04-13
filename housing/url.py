from django.urls import path
from .views import RepairRequestListView, RepairRequestDetailView

urlpatterns = [
    path("", RepairRequestListView.as_view(), name="repairrequest-list"),
    path("repairs/<int:pk>/", RepairRequestDetailView.as_view(), name="repairrequest-detail"),
]