from django.contrib.auth.models import User
from django.test import TestCase

from housing.models import Community, Dwelling, Tenant, RepairRequest


class RepairRequestModelTests(TestCase):
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
        self.user = User.objects.create_user(
            username="tenantdemo",
            password="demo12345"
        )
        self.tenant = Tenant.objects.create(
            user=self.user,
            dwelling=self.dwelling,
            full_name="Demo Tenant",
            email="tenant@example.com"
        )

    def test_reported_repair_is_open(self):
        repair = RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            title="Broken Air Conditioner",
            description="Air conditioner not working.",
            category="aircon",
            priority="urgent",
            status="reported"
        )

        self.assertTrue(repair.is_open())

    def test_completed_repair_is_not_open(self):
        repair = RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            title="Fixed Tap",
            description="Tap has been fixed.",
            category="plumbing",
            priority="medium",
            status="completed"
        )

        self.assertFalse(repair.is_open())

    def test_custom_queryset_open_returns_only_active_repairs(self):
        open_repair = RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            title="Door Lock Broken",
            description="Door lock needs repair.",
            category="doors",
            priority="high",
            status="reported"
        )

        RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            title="Completed Electrical Repair",
            description="Electrical issue fixed.",
            category="electrical",
            priority="low",
            status="completed"
        )

        self.assertIn(open_repair, RepairRequest.objects.open())
        self.assertEqual(RepairRequest.objects.open().count(), 1)

    def test_custom_queryset_urgent_returns_urgent_repairs(self):
        urgent_repair = RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            title="Urgent Ceiling Leak",
            description="Water dripping from ceiling.",
            category="roofing",
            priority="urgent",
            status="reported"
        )

        RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            title="Low Priority Window",
            description="Window handle loose.",
            category="other",
            priority="low",
            status="reported"
        )

        self.assertIn(urgent_repair, RepairRequest.objects.urgent())
        self.assertEqual(RepairRequest.objects.urgent().count(), 1)