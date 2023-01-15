import factory
import factory.fuzzy

from core.models import User
from goals.models import Category, Board, Goal, Comment, BoardParticipant


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    email = factory.Faker('email')
    password = '@passgreat'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.fuzzy.FuzzyText(length=25)


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    board = factory.SubFactory(BoardFactory)
    title = factory.fuzzy.FuzzyText(length=10)
    user = factory.SubFactory(UserFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.fuzzy.FuzzyText(length=10)
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.fuzzy.FuzzyText(length=10)
    goal = factory.SubFactory(UserFactory)
    user = factory.SubFactory(GoalFactory)
