from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters, generics
from rest_framework.pagination import LimitOffsetPagination

from .filters import GoalDateFilter
from .models import GoalCategory, Goal, GoalComment, Board
from .permissions import BoardPermissions, GoalCategoryPermissions, IsOwnerOrReadOnly, GoalPermissions, \
    CommentsPermissions
from .serializers import GoalCreateCategorySerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    GoalCommentCreateSerializer, GoalCommentSerializer, BoardSerializer, BoardListSerializer, BoardCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions, IsOwnerOrReadOnly]
    serializer_class = GoalCreateCategorySerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ['board']
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).exclude(status=Goal.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Goal.objects.select_related('user', 'category__board').filter(
            Q(goal__category__board__participants__user_id=self.request.user.id) & ~Q(status=Goal.Status.archived)
        )

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [CommentsPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    permission_classes = [CommentsPermissions]
    serializer_class = GoalCommentSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    # filterset_class = GoalDateFilter
    ordering_fields = ["goal"]
    ordering = ["-created"]

    # def get_queryset(self):
    #     return GoalComment.objects.filter(user=self.request.user)

    def get_queryset(self):
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id
        )


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [CommentsPermissions, IsOwnerOrReadOnly]

    def get_queryset(self):
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id
        )

    # def get_queryset(self):
    #     return GoalComment.objects.filter(user=self.request.user)


class BoardCreateView(generics.CreateAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # Фильтрация – идет через participants
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardListView(generics.ListAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardListSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    # filterset_class = GoalDateFilter
    ordering_fields = ["title"]
    ordering = ["-created"]

    def get_queryset(self):
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)
