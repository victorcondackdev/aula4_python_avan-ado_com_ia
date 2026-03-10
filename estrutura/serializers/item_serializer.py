from decimal import Decimal

from rest_framework import serializers

from api.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_price(self, value):
        if value <= Decimal("0"):
            raise serializers.ValidationError("price deve ser maior que zero.")
        return value

    def validate_quantity(self, value: int) -> int:
        if value < 0:
            raise serializers.ValidationError("quantity nao pode ser negativa.")
        return value

    def validate_name(self, value: str) -> str:
        cleaned_name = value.strip()
        if len(cleaned_name) < 3:
            raise serializers.ValidationError("name deve ter ao menos 3 caracteres.")
        return cleaned_name

    def validate(self, attrs: dict) -> dict:
        description = attrs.get("description")
        if isinstance(description, str):
            attrs["description"] = description.strip()
        return attrs

