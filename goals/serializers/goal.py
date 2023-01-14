from rest_framework import serializers

from core.serializers import RetrieveUserSerializer
from goals.models import Goal, BoardParticipant


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
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


class GoalSerializer(serializers.ModelSerializer):
    user = RetrieveUserSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"
