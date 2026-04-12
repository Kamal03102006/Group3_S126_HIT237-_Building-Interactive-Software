from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Community, Dwelling, Tenant, RepairRequest


class DwellingListView(ListView):
    model = Dwelling
    template_name = "housing/house_list.html"
    context_object_name = "houses"

    def get_queryset(self):
        return Dwelling.objects.select_related("community").order_by("house_code")


class RepairRequestListView(ListView):
    model = RepairRequest
    template_name = "housing/request_list.html"
    context_object_name = "requests"

    def get_queryset(self):
        return (
            RepairRequest.objects
            .select_related("dwelling", "tenant")
            .order_by("-reported_at")
        )


class RepairRequestDetailView(DetailView):
    model = RepairRequest
    template_name = "housing/repairrequest_detail.html"
    context_object_name = "repair_request"

    def get_queryset(self):
        return (
            RepairRequest.objects
            .select_related("dwelling", "tenant")
            .prefetch_related("updates")
        )


class RepairRequestCreateView(CreateView):
    model = RepairRequest
    template_name = "housing/repairrequest_form.html"
    fields = ["dwelling", "tenant", "title", "description", "category", "priority"]
    success_url = reverse_lazy("repairrequest-list")


class RepairRequestUpdateView(UpdateView):
    model = RepairRequest
    template_name = "housing/repairrequest_form.html"
    fields = ["title", "description", "category", "priority", "status"]
    success_url = reverse_lazy("repairrequest-list")


class RepairRequestDeleteView(DeleteView):
    model = RepairRequest
    template_name = "housing/repairrequest_confirm_delete.html"
    success_url = reverse_lazy("repairrequest-list")