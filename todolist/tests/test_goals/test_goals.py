import json

import pytest
from django.urls import reverse

from goals import serializers
from tests import factories

#tests category

@pytest.mark.django_db
def test_create(auth_client, new_user, board, participant):
    response = auth_client.post(reverse("create_category"),
                                data=json.dumps({"title": "test_category", "board": board.pk}),
                                content_type="application/json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_list(auth_client, new_user, board, participant):
    categories = factories.CategoryFactory.create_batch(5, board=board, user=new_user)

    response = auth_client.get(reverse("category_list"))
    expected_response = serializers.GoalCategorySerializer(instance=categories, many=True).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve(auth_client, new_user, category, board):
    response = auth_client.get(reverse("category_pk", args=[category.pk]))

    expected_response = {"id": 7,
                         "user": {"id": new_user.pk,
                                  "username": new_user.username,
                                  "first_name": "",
                                  "last_name": "",
                                  "email": new_user.email},
                         "created": response.data.get("created"),
                         "updated": response.data.get("updated"),
                         "title": category.title,
                         "is_deleted": False,
                         "board": board.pk
                         }

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_delete(auth_client, new_user, category):
    response = auth_client.delete(reverse("category_pk", args=[category.pk]))
    assert response.status_code == 204


@pytest.mark.django_db
def test_update(auth_client, new_user, category, board):
    response = auth_client.put(reverse("category_pk", args=[category.pk]),
                               data={"board": board.pk, "title": "test_category"})

    assert response.status_code == 200
    assert response.data.get("title") == "test name category"

#tests comments

@pytest.mark.django_db
def test_create(auth_client, new_user, goal):
    response = auth_client.post(reverse("goal_comment_create"),
                                data={"text": "test comment", "goal": goal.pk})

    expected_response = {"id": response.data.get("id"),
                         "created": response.data.get("created"),
                         "updated": response.data.get("updated"),
                         "text": "test comment",
                         "goal": goal.pk}

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_list(auth_client, new_user, goal):
    comments = factories.CommentFactory.create_batch(5, goal=goal, user=new_user)
    response = auth_client.get(reverse("goal_comment_list"))
    expected_response = serializers.GoalCommentSerializer(instance=comments, many=True).data
    expected_response = sorted(expected_response, key=lambda x: x['id'], reverse=True)

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve(auth_client, new_user, comment, goal):
    response = auth_client.get(reverse("goal_comment_pk", args=[comment.pk]))

    expected_response = {"id": response.data.get("id"),
                         "user": {"id": new_user.pk,
                                  "username": "Vasya_1995",
                                  "first_name": "",
                                  "last_name": "",
                                  "email": "email@mail.ru"},
                         "created": response.data.get("created"),
                         "updated": response.data.get("updated"),
                         "text": comment.text,
                         "goal": goal.pk}

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_update(auth_client, new_user, comment):
    response = auth_client.put(reverse("goal_comment_pk", args=[comment.pk]),
                               data={"text": 'test text update'})

    assert response.status_code == 200
    assert response.data.get("text") == "test text update"


@pytest.mark.django_db
def test_delete(auth_client, new_user, comment):
    response = auth_client.delete(reverse("goal_comment_pk", args=[comment.pk]))

    assert response.status_code == 204

#tests goals

@pytest.mark.django_db
def test_create(auth_client, new_user, category):
    response = auth_client.post(reverse("goal_create"),
                                data={"title": "test goal", "category": category.pk})

    expected_response = {'id': response.data.get("id"),
                         'created': response.data.get("created"),
                         'updated': response.data.get("updated"),
                         'title': 'test goal',
                         'description': None,
                         'status': 1,
                         'priority': 2,
                         'due_date': None,
                         'category': category.pk}

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_list(auth_client, new_user, category):
    goals = factories.GoalFactory.create_batch(5, category=category, user=new_user)
    response = auth_client.get(reverse("goal_list"))

    expected_response = serializers.GoalSerializer(instance=goals, many=True).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve(auth_client, goal, new_user, category):
    resource = auth_client.get(reverse("goal_pk", args=[goal.pk]))

    expected_response = {"id": goal.pk,
                         "user": {"id": new_user.pk,
                                  "username": "Vasya_1995",
                                  "first_name": "",
                                  "last_name": "",
                                  "email": "email@mail.ru"},
                         "created": resource.data.get("created"),
                         "updated": resource.data.get("updated"),
                         "title": goal.title,
                         "description": None,
                         "status": 1,
                         "priority": 2,
                         "due_date": None,
                         "category": category.pk}

    assert resource.status_code == 200
    assert resource.data == expected_response


@pytest.mark.django_db
def test_update(auth_client, new_user, goal, category):
    response = auth_client.put(reverse("goal_pk", args=[goal.pk]),
                               data={"title": "test updated goal", "category": category.pk})

    assert response.status_code == 200
    assert response.data.get("title") == "test updated goal"


@pytest.mark.django_db
def test_delete(auth_client, goal):
    response = auth_client.delete(reverse("goal_pk", args=[goal.pk]))
    assert response.status_code == 204

#tests board

@pytest.mark.django_db
def test_create(auth_client):
    response = auth_client.post(reverse("board_create"),
                                data={"title": "test_board"})
    expected_response = {"id": response.data["id"],
                         "created": response.data.get("created"),
                         "updated": response.data.get("updated"),
                         "title": "test_board",
                         "is_deleted": False, }

    assert response.status_code == 201
    assert response.data == expected_response
