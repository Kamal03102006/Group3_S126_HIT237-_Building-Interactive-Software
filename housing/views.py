from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .exceptions import HousingDomainError
from .forms import (
    TenantRepairRequestForm,
    StaffRepairRequestUpdateForm,
    MaintenanceUpdateForm,
    RegisterForm,
)
from .models import RepairRequest, MaintenanceUpdate
from .services.dashboard_service import get_dashboard_summary_for_user
from .services.repair_request_service import (
    create_repair_request_for_user,
    get_filtered_repair_requests,
    get_repair_for_user,
)


class UserLoginView(LoginView):
    template_name = "housing/registration/login.html"


class UserLogoutView(LogoutView):
    pass


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "housing/registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Account created successfully. You can now log in."
        )
        return super().form_valid(form)


class MaintenanceStaffRequiredMixin(UserPassesTestMixin):
    """
    Allows access to Maintenance Staff, Housing Manager,
    or Django staff users.

    Role design:
    - Tenant: can create and view own repair requests
    - Maintenance Staff: can view and update repair requests
    - Housing Manager: can manage repair workflow and summaries
    - Admin/Staff: can manage everything through Django admin
    """

    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated
            and (
                user.is_staff
                or user.groups.filter(
                    name__in=["Maintenance Staff", "Housing Manager"]
                ).exists()
            )
        )


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Allows access only to Django admin/staff users.
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff


class RepairRequestListView(LoginRequiredMixin, ListView):
    model = RepairRequest
    template_name = "housing/repairrequest_list.html"
    context_object_name = "repair_requests"

    def get_queryset(self):
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")

        return get_filtered_repair_requests(
            user=self.request.user,
            status=status,
            priority=priority,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["status_choices"] = RepairRequest.STATUS_CHOICES
        context["priority_choices"] = RepairRequest.PRIORITY_CHOICES
        context["selected_status"] = self.request.GET.get("status", "")
        context["selected_priority"] = self.request.GET.get("priority", "")

        context["dashboard_summary"] = (
            get_dashboard_summary_for_user(
                self.request.user
            )
        )

        return context


class RepairRequestDetailView(LoginRequiredMixin, DetailView):
    model = RepairRequest
    template_name = "housing/repairrequest_detail.html"
    context_object_name = "repair_request"

    def get_object(self, queryset=None):
        return get_repair_for_user(
            self.request.user,
            self.kwargs["pk"]
        )


class RepairRequestCreateView(LoginRequiredMixin, CreateView):
    model = RepairRequest
    form_class = TenantRepairRequestForm
    template_name = "housing/repairrequest_form.html"

    def form_valid(self, form):
        try:
            self.object = create_repair_request_for_user(
                self.request.user,
                form
            )

            messages.success(
                self.request,
                "Repair request submitted successfully."
            )

            return redirect(
                self.object.get_absolute_url()
            )

        except HousingDomainError as error:
            messages.error(
                self.request,
                str(error)
            )

            return redirect("repairrequest-list")


class RepairRequestUpdateView(
    LoginRequiredMixin,
    MaintenanceStaffRequiredMixin,
    UpdateView
):
    model = RepairRequest
    form_class = StaffRepairRequestUpdateForm
    template_name = "housing/repairrequest_form.html"

    def get_object(self, queryset=None):
        return get_repair_for_user(
            self.request.user,
            self.kwargs["pk"]
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Repair request updated successfully."
        )

        return super().form_valid(form)


class MaintenanceUpdateCreateView(
    LoginRequiredMixin,
    MaintenanceStaffRequiredMixin,
    CreateView
):
    model = MaintenanceUpdate
    form_class = MaintenanceUpdateForm
    template_name = "housing/maintenanceupdate_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.repair_request = get_repair_for_user(
            request.user,
            self.kwargs["pk"]
        )

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):
        form.instance.repair_request = self.repair_request

        form.instance.updated_by = (
            self.request.user.get_full_name()
            or self.request.user.username
        )

        messages.success(
            self.request,
            "Maintenance update added successfully."
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "repairrequest-detail",
            kwargs={
                "pk": self.repair_request.pk
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["repair_request"] = self.repair_request

        return context