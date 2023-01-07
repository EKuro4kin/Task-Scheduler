import factory

from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('Vasya_1995')
    email = factory.Faker('email@mail.ru')
    password = 'Password_123'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker('name')


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Faker('name')


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Faker('name')

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text = 'comments'

