from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import RepairRequestForm, MaintenanceUpdateForm
from .models import RepairRequest, MaintenanceUpdate


class RepairRequestListView(ListView):
    model = RepairRequest
    template_name = "housing/repairrequest_list.html"
    context_object_name = "repair_requests"

    def get_queryset(self):
        queryset = (
            RepairRequest.objects
            .select_related("dwelling", "tenant", "dwelling__community")
            .order_by("-reported_at")
        )

        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = RepairRequest.STATUS_CHOICES
        context["priority_choices"] = RepairRequest.PRIORITY_CHOICES
        context["selected_status"] = self.request.GET.get("status", "")
        context["selected_priority"] = self.request.GET.get("priority", "")
        return context


class RepairRequestDetailView(DetailView):
    model = RepairRequest
    template_name = "housing/repairrequest_detail.html"
    context_object_name = "repair_request"

    def get_queryset(self):
        return (
            RepairRequest.objects
            .select_related("dwelling", "tenant", "dwelling__community")
            .prefetch_related("updates")
        )


class RepairRequestCreateView(CreateView):
    model = RepairRequest
    form_class = RepairRequestForm
    template_name = "housing/repairrequest_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Repair request submitted successfully.")
        return super().form_valid(form)


class RepairRequestUpdateView(UpdateView):
    model = RepairRequest
    form_class = RepairRequestForm
    template_name = "housing/repairrequest_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Repair request updated successfully.")
        return super().form_valid(form)


class MaintenanceUpdateCreateView(CreateView):
    model = MaintenanceUpdate
    form_class = MaintenanceUpdateForm
    template_name = "housing/maintenanceupdate_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.repair_request = RepairRequest.objects.get(pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.repair_request = self.repair_request
        messages.success(self.request, "Maintenance update added successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("repairrequest-detail", kwargs={"pk": self.repair_request.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["repair_request"] = self.repair_request
        return context