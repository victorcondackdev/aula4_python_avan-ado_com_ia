from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Item


class ItemAPITestCase(APITestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="Teclado",
            description="Mecanico",
            price="199.90",
            quantity=10,
            is_active=True,
        )

    def test_list_items_returns_200(self):
        url = reverse("item-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_item_returns_201(self):
        url = reverse("item-list")
        payload = {
            "name": "Mouse",
            "description": "Sem fio",
            "price": "99.90",
            "quantity": 3,
            "is_active": True,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)

    def test_create_item_with_invalid_price_returns_400(self):
        url = reverse("item-list")
        payload = {
            "name": "Cabo",
            "description": "USB-C",
            "price": "0.00",
            "quantity": 5,
            "is_active": True,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_with_negative_quantity_returns_400(self):
        url = reverse("item-list")
        payload = {
            "name": "Hub USB",
            "description": "4 portas",
            "price": "79.90",
            "quantity": -1,
            "is_active": True,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_with_short_name_returns_400(self):
        url = reverse("item-list")
        payload = {
            "name": "AB",
            "description": "Nome curto",
            "price": "59.90",
            "quantity": 2,
            "is_active": True,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_item_returns_200(self):
        url = reverse("item-detail", kwargs={"pk": self.item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item_returns_200(self):
        url = reverse("item-detail", kwargs={"pk": self.item.id})
        payload = {
            "name": "Teclado Atualizado",
            "description": "ABNT2",
            "price": "249.90",
            "quantity": 8,
            "is_active": True,
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_item_returns_200(self):
        url = reverse("item-detail", kwargs={"pk": self.item.id})
        payload = {"quantity": 7}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item_returns_204(self):
        url = reverse("item-detail", kwargs={"pk": self.item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_routes_are_versioned_with_api_v1(self):
        self.assertEqual(reverse("item-list"), "/api/v1/items/")
        self.assertEqual(reverse("item-detail", kwargs={"pk": self.item.id}), f"/api/v1/items/{self.item.id}/")

    def test_legacy_list_route_items_also_works(self):
        response = self.client.get("/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_legacy_detail_route_items_also_works(self):
        response = self.client.get(f"/items/{self.item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

