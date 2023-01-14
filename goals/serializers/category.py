from rest_framework import serializers

from core.serializers import RetrieveUserSerializer
from goals.models import Category, BoardParticipant


class CategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    # def validate(self, attrs):
    #     roll = BoardParticipant.objects.filter(
    #         user=attrs.get('user'),
    #         board=attrs.get('board'),
    #         role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
    #     ).exists()
    #     if roll:
    #         return attrs
    #     raise serializers.ValidationError('You do not have permission to perform this action')


class CategorySerializer(serializers.ModelSerializer):
    user = RetrieveUserSerializer(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value: Category) -> Category:
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')

        return value
