from django.contrib.auth.models import User, Group
from django.test import TestCase

from housing.models import Community, Dwelling, Tenant, RepairRequest
from housing.services.permission_service import (
    user_is_staff_or_manager,
    user_is_tenant,
    user_can_update_repair,
    user_can_view_repair,
)


class PermissionServiceTests(TestCase):
    def setUp(self):
        self.community = Community.objects.create(
            name="Maningrida",
            region="NT"
        )
        self.dwelling = Dwelling.objects.create(
            community=self.community,
            house_code="MN001",
            address="5 Arnhem Street",
            bedrooms=4,
            condition_status="poor"
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
        self.manager_user = User.objects.create_user(
            username="managerdemo",
            password="demo12345"
        )

        staff_group = Group.objects.create(name="Maintenance Staff")
        manager_group = Group.objects.create(name="Housing Manager")

        self.staff_user.groups.add(staff_group)
        self.manager_user.groups.add(manager_group)

        self.tenant = Tenant.objects.create(
            user=self.tenant_user,
            dwelling=self.dwelling,
            full_name="Demo Tenant",
            email="tenant@example.com"
        )

        self.repair = RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            title="Bathroom Drain Blocked",
            description="Bathroom drain overflowing.",
            category="plumbing",
            priority="medium",
            status="reported"
        )

    def test_user_is_tenant_when_linked_to_tenant_profile(self):
        self.assertTrue(user_is_tenant(self.tenant_user))

    def test_unlinked_user_is_not_tenant(self):
        self.assertFalse(user_is_tenant(self.other_user))

    def test_staff_group_user_is_staff_or_manager(self):
        self.assertTrue(user_is_staff_or_manager(self.staff_user))

    def test_manager_group_user_is_staff_or_manager(self):
        self.assertTrue(user_is_staff_or_manager(self.manager_user))

    def test_tenant_cannot_update_repair(self):
        self.assertFalse(user_can_update_repair(self.tenant_user))

    def test_staff_can_update_repair(self):
        self.assertTrue(user_can_update_repair(self.staff_user))

    def test_tenant_can_view_own_repair(self):
        self.assertTrue(user_can_view_repair(self.tenant_user, self.repair))

    def test_unlinked_user_cannot_view_repair(self):
        self.assertFalse(user_can_view_repair(self.other_user, self.repair))

    def test_staff_can_view_any_repair(self):
        self.assertTrue(user_can_view_repair(self.staff_user, self.repair))