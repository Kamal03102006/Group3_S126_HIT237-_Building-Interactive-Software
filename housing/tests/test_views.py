from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from housing.models import Community, Dwelling, Tenant, RepairRequest


class RepairRequestViewTests(TestCase):
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
            title="Broken Front Door Lock",
            description="Front door lock damaged.",
            category="doors",
            priority="urgent",
            status="reported"
        )

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(reverse("repairrequest-list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_tenant_can_access_repair_list(self):
        self.client.login(username="tenantdemo", password="demo12345")

        response = self.client.get(reverse("repairrequest-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Broken Front Door Lock")

    def test_staff_can_access_repair_list(self):
        self.client.login(username="staffdemo", password="demo12345")

        response = self.client.get(reverse("repairrequest-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Broken Front Door Lock")

    def test_staff_can_access_update_page(self):
        self.client.login(username="staffdemo", password="demo12345")

        response = self.client.get(
            reverse("repairrequest-update", kwargs={"pk": self.repair.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_tenant_cannot_access_update_page(self):
        self.client.login(username="tenantdemo", password="demo12345")

        response = self.client.get(
            reverse("repairrequest-update", kwargs={"pk": self.repair.pk})
        )

        self.assertEqual(response.status_code, 403)

    def test_staff_cannot_use_tenant_submit_request_page(self):
        self.client.login(username="staffdemo", password="demo12345")

        response = self.client.get(reverse("repairrequest-create"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("repairrequest-list"))