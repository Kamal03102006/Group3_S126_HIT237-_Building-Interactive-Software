from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import RepairRequest, MaintenanceUpdate


class TenantRepairRequestForm(forms.ModelForm):
    """
    Form used by tenants when creating repair requests.
    The tenant, dwelling and status are assigned automatically
    by the service layer using the logged-in user.
    """

    class Meta:
        model = RepairRequest
        fields = [
            "title",
            "description",
            "category",
            "priority",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class StaffRepairRequestUpdateForm(forms.ModelForm):
    """
    Form used by maintenance staff or housing managers
    when updating repair request details and status.
    """

    class Meta:
        model = RepairRequest
        fields = [
            "title",
            "description",
            "category",
            "priority",
            "status",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class MaintenanceUpdateForm(forms.ModelForm):
    """
    Form used to add maintenance updates.
    updated_by is assigned automatically from the logged-in user.
    """

    class Meta:
        model = MaintenanceUpdate
        fields = [
            "note",
            "status_snapshot",
        ]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 4}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]