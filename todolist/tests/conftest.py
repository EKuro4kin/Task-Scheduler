import pytest
from rest_framework.test import APIClient

from core.models import User
from tests import factories


@pytest.fixture
def new_user(db):
    user = User.objects.create_user(
        username="Vasya_1995",
        email="email@mail.ru",
        password="Password_123"
    )
    return user


@pytest.fixture
def auth_client(new_user):
    client = APIClient()
    client.login(username="Vasya_1995", password="Password_1234")
    return client


@pytest.fixture
def board():
    board = factories.BoardFactory.create()
    return board


@pytest.fixture
def participant(new_user, board):
    factories.ParticipantFactory.create(user=new_user, board=board)


@pytest.fixture
def category(board, new_user, participant):
    category = factories.CategoryFactory.create(board=board, user=new_user)
    return category


@pytest.fixture
def goal(category, new_user):
    goal = factories.GoalFactory.create(category=category, user=new_user)
    return goal


@pytest.fixture
def comment(goal, new_user):
    comment = factories.CommentFactory.create(user=new_user, goal=goal)
    return comment
