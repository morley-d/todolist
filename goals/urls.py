from django.urls import path

from goals import views


urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name='create_category'),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name='list_category'),
    path("goal_category/<pk>", views.GoalCategoryView.as_view(), name='retrieve_category'),
    path("goal/create", views.GoalCreateView.as_view(), name='create_goal'),
    path("goal/list", views.GoalListView.as_view(), name='list_goal'),
    path("goal/<pk>", views.GoalView.as_view(), name='retrieve_goal'),
    path("goal_comment/create", views.CommentCreateView.as_view(), name='create_comment'),
    path("goal_comment/list", views.CommentListView.as_view(), name='list_comment'),
    path("goal_comment/<pk>", views.CommentView.as_view(), name='retrieve_comment'),
    path("board/create", views.BoardCreateView.as_view(), name='create_board'),
    path("board/list", views.BoardListView.as_view(), name='list_board'),
    path("board/<pk>", views.BoardView.as_view(), name='retrieve_board'),
]
