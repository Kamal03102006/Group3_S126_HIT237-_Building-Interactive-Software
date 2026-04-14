from django import forms
from .models import RepairRequest, MaintenanceUpdate


class RepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = [
            "dwelling",
            "tenant",
            "title",
            "description",
            "category",
            "priority",
            "status",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        dwelling = cleaned_data.get("dwelling")
        tenant = cleaned_data.get("tenant")

        if tenant and dwelling and tenant.dwelling != dwelling:
            raise forms.ValidationError(
                "Selected tenant does not belong to the selected dwelling."
            )

        return cleaned_data


class MaintenanceUpdateForm(forms.ModelForm):
    class Meta:
        model = MaintenanceUpdate
        fields = ["note", "status_snapshot", "updated_by"]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 4}),
        }