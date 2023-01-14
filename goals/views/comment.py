from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.models import Comment
from goals import serializers
from goals.permissions import CommentPermissions


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CommentCreateSerializer

    def perform_create(self, serializer: serializers.CommentCreateSerializer) -> None:
        serializer.save(goal_id=self.request.data['goal'])


class CommentListView(ListAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated, CommentPermissions]
    serializer_class = serializers.CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["goal"]
    ordering = ["-id"]

    def get_queryset(self) -> Comment:
        return Comment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class CommentView(RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermissions]

    def get_queryset(self) -> Comment:
        return Comment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )
