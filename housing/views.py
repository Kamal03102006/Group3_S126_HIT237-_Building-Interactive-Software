from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import RepairRequest
from .forms import RepairRequestForm


class RepairRequestListView(ListView):
    model = RepairRequest
    template_name = "housing/request_list.html"
    context_object_name = "repair_requests"

    def get_queryset(self):
        return (
            RepairRequest.objects
            .select_related("dwelling", "tenant")
            .order_by("-reported_at")
        )


class RepairRequestDetailView(DetailView):
    model = RepairRequest
    template_name = "housing/request_detail.html"
    context_object_name = "repair_request"

    def get_queryset(self):
        return RepairRequest.objects.select_related("dwelling", "tenant")


class RepairRequestCreateView(CreateView):
    model = RepairRequest
    form_class = RepairRequestForm
    template_name = "housing/request_form.html"
    success_url = reverse_lazy("request-list")


class RepairRequestUpdateView(UpdateView):
    model = RepairRequest
    form_class = RepairRequestForm
    template_name = "housing/request_form.html"
    success_url = reverse_lazy("request-list")


class RepairRequestDeleteView(DeleteView):
    model = RepairRequest
    template_name = "housing/request_confirm_delete.html"
    success_url = reverse_lazy("request-list")