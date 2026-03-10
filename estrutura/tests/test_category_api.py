from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Category


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Perifericos",
            description="Itens de entrada",
            is_active=True,
        )

    def test_list_categories_returns_200(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_returns_201(self):
        url = reverse("category-list")
        payload = {
            "name": "Monitores",
            "description": "Telas e acessorios",
            "is_active": True,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_create_category_with_short_name_returns_400(self):
        url = reverse("category-list")
        payload = {
            "name": "AB",
            "description": "Nome curto",
            "is_active": True,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_category_with_duplicate_name_returns_400(self):
        url = reverse("category-list")
        payload = {
            "name": "perifericos",
            "description": "Duplicado case-insensitive",
            "is_active": True,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_category_returns_200(self):
        url = reverse("category-detail", kwargs={"pk": self.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_returns_200(self):
        url = reverse("category-detail", kwargs={"pk": self.category.id})
        payload = {
            "name": "Perifericos Premium",
            "description": "Linha premium",
            "is_active": True,
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category_returns_204(self):
        url = reverse("category-detail", kwargs={"pk": self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_routes_are_versioned_with_api_v1(self):
        self.assertEqual(reverse("category-list"), "/api/v1/categories/")
        self.assertEqual(
            reverse("category-detail", kwargs={"pk": self.category.id}),
            f"/api/v1/categories/{self.category.id}/",
        )

    def test_legacy_list_route_categories_also_works(self):
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_legacy_detail_route_categories_also_works(self):
        response = self.client.get(f"/categories/{self.category.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
