from rest_framework import serializers

from api.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value: str) -> str:
        cleaned_name = value.strip()
        if len(cleaned_name) < 3:
            raise serializers.ValidationError("name deve ter ao menos 3 caracteres.")

        queryset = Category.objects.filter(name__iexact=cleaned_name)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("category com esse name ja existe.")

        return cleaned_name

    def validate(self, attrs: dict) -> dict:
        description = attrs.get("description")
        if isinstance(description, str):
            attrs["description"] = description.strip()
        return attrs
