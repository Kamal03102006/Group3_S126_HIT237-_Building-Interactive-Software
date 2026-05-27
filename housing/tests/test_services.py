from django.contrib.auth.models import User, Group
from django.test import TestCase

from housing.exceptions import (
    InvalidRepairStatus,
    PermissionDeniedForRepair,
    TenantProfileMissing,
)
from housing.models import Community, Dwelling, Tenant, RepairRequest, MaintenanceUpdate
from housing.services.dashboard_service import get_dashboard_summary_for_user
from housing.services.maintenance_service import add_maintenance_update
from housing.services.repair_request_service import (
    create_repair_request_for_user,
    get_visible_repair_requests,
    update_repair_status,
)


class SimpleRepairFormStub:
    """
    Small form stub so service can be tested without depending on template/view code.
    """

    def __init__(self, title="Broken Air Conditioner"):
        self.instance = RepairRequest(
            title=title,
            description="Air conditioner is not cooling.",
            category="aircon",
            priority="urgent",
        )

    def save(self, commit=True):
        if commit:
            self.instance.save()
        return self.instance


class RepairRequestServiceTests(TestCase):
    def setUp(self):
        self.community = Community.objects.create(
            name="Wadeye",
            region="NT"
        )
        self.dwelling = Dwelling.objects.create(
            community=self.community,
            house_code="WD001",
            address="12 Community Road",
            bedrooms=3,
            condition_status="fair"
        )

        self.tenant_user = User.objects.create_user(
            username="tenantdemo",
            password="demo12345"
        )
        self.other_user = User.objects.create_user(
            username="otherdemo",
            password="demo12345"
        )
        self.staff_user = User.objects.create_user(
            username="staffdemo",
            password="demo12345"
        )

        staff_group = Group.objects.create(name="Maintenance Staff")
        self.staff_user.groups.add(staff_group)

        self.tenant = Tenant.objects.create(
            user=self.tenant_user,
            dwelling=self.dwelling,
            full_name="Demo Tenant",
            email="tenant@example.com"
        )

        self.repair = RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            title="Leaking Kitchen Tap",
            description="Kitchen tap leaking.",
            category="plumbing",
            priority="medium",
            status="reported"
        )

    def test_tenant_only_sees_own_repairs(self):
        queryset = get_visible_repair_requests(self.tenant_user)

        self.assertIn(self.repair, queryset)
        self.assertEqual(queryset.count(), 1)

    def test_unlinked_user_sees_no_repairs(self):
        queryset = get_visible_repair_requests(self.other_user)

        self.assertEqual(queryset.count(), 0)

    def test_staff_can_see_all_repairs(self):
        queryset = get_visible_repair_requests(self.staff_user)

        self.assertIn(self.repair, queryset)

    def test_create_repair_request_assigns_tenant_dwelling_and_reported_status(self):
        form = SimpleRepairFormStub()

        repair = create_repair_request_for_user(self.tenant_user, form)

        self.assertEqual(repair.tenant, self.tenant)
        self.assertEqual(repair.dwelling, self.dwelling)
        self.assertEqual(repair.status, "reported")

    def test_create_repair_without_tenant_profile_raises_exception(self):
        form = SimpleRepairFormStub()

        with self.assertRaises(TenantProfileMissing):
            create_repair_request_for_user(self.other_user, form)

    def test_staff_can_update_repair_status(self):
        updated_repair = update_repair_status(
            self.staff_user,
            self.repair,
            "in_progress",
            "Technician assigned."
        )

        self.assertEqual(updated_repair.status, "in_progress")
        self.assertTrue(
            MaintenanceUpdate.objects.filter(
                repair_request=self.repair,
                status_snapshot="in_progress"
            ).exists()
        )

    def test_tenant_cannot_update_repair_status(self):
        with self.assertRaises(PermissionDeniedForRepair):
            update_repair_status(
                self.tenant_user,
                self.repair,
                "in_progress"
            )

    def test_invalid_status_raises_exception(self):
        with self.assertRaises(InvalidRepairStatus):
            update_repair_status(
                self.staff_user,
                self.repair,
                "not_a_real_status"
            )

    def test_add_maintenance_update_changes_status_and_creates_update_record(self):
        update = add_maintenance_update(
            user=self.staff_user,
            repair_request=self.repair,
            note="Work has started.",
            status_snapshot="in_progress"
        )

        self.repair.refresh_from_db()

        self.assertEqual(self.repair.status, "in_progress")
        self.assertEqual(update.status_snapshot, "in_progress")
        self.assertEqual(update.note, "Work has started.")

    def test_dashboard_summary_counts_visible_repairs(self):
        summary = get_dashboard_summary_for_user(self.staff_user)

        self.assertEqual(summary["total_repairs"], 1)
        self.assertEqual(summary["open_repairs"], 1)