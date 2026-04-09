from django.views.generic import ListView, DetailView
from .models import RepairRequest


class RepairRequestListView(ListView):
    model = RepairRequest
    template_name = "housing/repairrequest_list.html"
    context_object_name = "repair_requests"

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
        )