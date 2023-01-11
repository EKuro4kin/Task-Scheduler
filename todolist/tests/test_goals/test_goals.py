import json

import pytest
from django.urls import reverse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from goals import serializers
from tests import factories

# tests category

@pytest.mark.django_db
def test_create_category(auth_client, new_user, board, participant):
    response = auth_client.post(reverse('create-category'),
                                data=json.dumps({'title': 'test_category', 'board': board.pk}),
                                content_type='application/json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_list_category(auth_client, new_user, board, participant):
    categories = factories.CategoryFactory.create_batch(5, board=board, user=new_user)

    response = auth_client.get(reverse('list-categories'))

    category_list = serializers.GoalCategorySerializer(instance=categories, many=True).data
    expected_response = sorted(category_list, key=lambda x: x['title'])

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve_category(auth_client, new_user, category, board):
    response = auth_client.get(reverse('retrieve-update-destroy-category', args=[category.pk]))

    expected_response = {'id': response.data.get('id'),
                         'user': {'id': new_user.pk,
                                  'username': new_user.username,
                                  'first_name': '',
                                  'last_name': '',
                                  'email': new_user.email},
                         'created': response.data.get('created'),
                         'updated': response.data.get('updated'),
                         'title': category.title,
                         'is_deleted': False,
                         'board': board.pk
                         }

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_delete_category(auth_client, new_user, category):
    response = auth_client.delete(reverse('retrieve-update-destroy-category', args=[category.pk]))
    assert response.status_code == 204


@pytest.mark.django_db
def test_update_category(auth_client, new_user, category, board):
    response = auth_client.put(reverse('retrieve-update-destroy-category', args=[category.pk]),
                               data={'board': board.pk, 'title': 'test_category'})

    assert response.status_code == 200
    assert response.data.get('title') == 'test_category'

#tests comments

@pytest.mark.django_db
def test_create_comments(auth_client, new_user, goal):
    response = auth_client.post(reverse('create-comment'),
                                data={'text': 'test comment', 'goal': goal.pk})

    expected_response = {'id': response.data.get('id'),
                         'created': response.data.get('created'),
                         'updated': response.data.get('updated'),
                         'text': 'test comment',
                         'goal': goal.pk
                         }

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_list_comments(auth_client, new_user, goal):
    comments = factories.CommentFactory.create_batch(5, goal=goal, user=new_user)
    response = auth_client.get(reverse('list-comment'))
    expected_response = serializers.GoalCommentSerializer(instance=comments, many=True).data
    expected_response = sorted(expected_response, key=lambda x: x['id'], reverse=True)

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve_comments(auth_client, new_user, comment, goal, category):
    response = auth_client.get(reverse('retrieve-update-destroy-comment', args=[comment.pk]))

    expected_response = {'id': response.data.get('id'),
                         'user': {'id': new_user.pk,
                                  'username': 'Vasya_1995',
                                  'first_name': '',
                                  'last_name': '',
                                  'email': 'email@mail.ru'},
                         'created': response.data.get('created'),
                         'updated': response.data.get('updated'),
                         'text': 'comments',
                         'goal': goal.pk}

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_update_comments(auth_client, new_user, comment):
    response = auth_client.put(reverse('retrieve-update-destroy-comment', args=[comment.pk]),
                               data={'text': 'test text update', 'goal': 1})

    assert response.status_code == 200
    assert response.data.get('text') == 'test text update'


@pytest.mark.django_db
def test_delete_comments(auth_client, new_user, comment):
    response = auth_client.delete(reverse('retrieve-update-destroy-comment', args=[comment.pk]))

    assert response.status_code == 204

# tests goals

@pytest.mark.django_db
def test_create_goals(auth_client, new_user, category):
    response = auth_client.post(reverse('create-goal'),
                                data={'title': 'test goal', 'category': category.pk, 'description': 'description'})

    expected_response = {'id': response.data.get('id'),
                         'created': response.data.get('created'),
                         'updated': response.data.get('updated'),
                         'title': 'test goal',
                         'description': 'description',
                         'status': 1,
                         'priority': 2,
                         'due_date': None,
                         'category': category.pk}

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_list_goals(auth_client, new_user, category):
    goals = factories.GoalFactory.create_batch(5, category=category, user=new_user)
    response = auth_client.get(reverse('list-goals'))

    goal_not_sorted = serializers.GoalSerializer(instance=goals, many=True).data
    goal_sorted = sorted(goal_not_sorted, key=lambda x: x['created'])
    expected_response = sorted(goal_sorted, key=lambda x: x['title'])

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve_goals(auth_client, goal, new_user, category):
    resource = auth_client.get(reverse('retrieve-update-destroy-goal', args=[goal.pk]))

    expected_response = {'id': goal.pk,
                         'user': {'id': new_user.pk,
                                  'username': 'Vasya_1995',
                                  'first_name': '',
                                  'last_name': '',
                                  'email': 'email@mail.ru'},
                         'created': resource.data.get('created'),
                         'updated': resource.data.get('updated'),
                         'title': goal.title,
                         'description': '',
                         'status': 1,
                         'priority': 2,
                         'due_date': None,
                         'category': category.pk}

    assert resource.status_code == 200
    assert resource.data == expected_response


@pytest.mark.django_db
def test_update_goals(auth_client, new_user, goal, category):
    response = auth_client.put(reverse('retrieve-update-destroy-goal', args=[goal.pk]),
                               data={'title': 'test updated goal', 'category': category.pk, 'description': 'description'})

    assert response.status_code == 200
    assert response.data.get('title') == 'test updated goal'


@pytest.mark.django_db
def test_delete_goals(auth_client, goal):
    response = auth_client.delete(reverse('retrieve-update-destroy-goal', args=[goal.pk]))
    assert response.status_code == 204

# tests board

@pytest.mark.django_db
def test_create_board(auth_client):
    response = auth_client.post(reverse('create-board'),
                                data={'title': 'test_board'})
    expected_response = {'id': response.data['id'],
                         'created': response.data.get('created'),
                         'updated': response.data.get('updated'),
                         'title': 'test_board',
                         'is_deleted': False, }

    assert response.status_code == 201
    assert response.data == expected_response
