from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView,
    RegisterView,
    RepairRequestListView,
    RepairRequestDetailView,
    RepairRequestCreateView,
    RepairRequestUpdateView,
    MaintenanceUpdateCreateView,
)

urlpatterns = [
    path("accounts/login/", UserLoginView.as_view(), name="login"),
    path("accounts/logout/", UserLogoutView.as_view(), name="logout"),
    path("accounts/register/", RegisterView.as_view(), name="register"),

    path("", RepairRequestListView.as_view(), name="repairrequest-list"),
    path("repairs/<int:pk>/", RepairRequestDetailView.as_view(), name="repairrequest-detail"),
    path("repairs/new/", RepairRequestCreateView.as_view(), name="repairrequest-create"),
    path("repairs/<int:pk>/edit/", RepairRequestUpdateView.as_view(), name="repairrequest-update"),
    path("repairs/<int:pk>/updates/new/", MaintenanceUpdateCreateView.as_view(), name="maintenanceupdate-create"),
]