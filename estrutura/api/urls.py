from django.urls import include, path
from rest_framework.routers import DefaultRouter

from viewsets import CategoryViewSet, ItemViewSet

router = DefaultRouter()
router.register("items", ItemViewSet, basename="item")
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = [
    # Alias legado sem versionamento para compatibilidade.
    path(
        "items/",
        ItemViewSet.as_view({"get": "list", "post": "create"}),
        name="item-list-legacy",
    ),
    path(
        "items/<int:pk>/",
        ItemViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="item-detail-legacy",
    ),
    path(
        "categories/",
        CategoryViewSet.as_view({"get": "list", "post": "create"}),
        name="category-list-legacy",
    ),
    path(
        "categories/<int:pk>/",
        CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="category-detail-legacy",
    ),
    path("api/v1/", include(router.urls)),
]

