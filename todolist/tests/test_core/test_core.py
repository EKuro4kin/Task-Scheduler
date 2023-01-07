import json

import pytest
from django.urls import reverse

from core import serializers


@pytest.mark.django_db
def test_create(client):
    response = client.post(reverse('signup'),
                           data={'username': 'Vasya_1995',
                                 'first_name': 'Vasya',
                                 'last_name': 'Vasyaa',
                                 'email': 'email@mail.ru',
                                 'password': 'Password_123',
                                 'password_repeat': 'Password_123'})

    expected_response = {'id': response.data.get('id'),
                         'last_login': response.data.get('last_login'),
                         'is_superuser': response.data.get('is_superuser'),
                         'username': 'Vasya_1995',
                         'first_name': 'Vasya',
                         'last_name': 'Vasyaa',
                         'email': 'email@mail.ru',
                         'is_staff': response.data.get('is_staff'),
                         'is_active': response.data.get('is_active'),
                         'date_joined': response.data.get('date_joined'),
                         'groups': response.data.get('groups'),
                         'user_permissions': response.data.get('user_permissions')
                         }

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_login(client, new_user):
    response = client.post(reverse('login_user'),
                           data=json.dumps({'username': 'Vasya_1995',
                                            'password': 'Password_123'}),
                           content_type='application/json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_retrieve(auth_client, new_user):
    response = auth_client.get(reverse('profile'))
    expected_response = serializers.ProfileSerializer(instance=new_user).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_update(auth_client, new_user):
    response = auth_client.put(reverse('profile'),
                               data={'username': 'Vasya_1995',
                                     'first_name': 'Vasya',
                                     'last_name': 'Vasyaa',
                                     'email': 'email@mail.ru'})

    assert response.status_code == 200
    assert response.data == {'id': new_user.id,
                             'username': 'Vasya_1995',
                             'first_name': 'Vasya',
                             'last_name': 'Vasyaa',
                             'email': 'email@mail.ru'}


@pytest.mark.django_db
def test_update_password(auth_client, new_user):
    response_change_pass = auth_client.put(reverse('update_password'),
                                           data={'new_password': 'Password_1234',
                                                 'old_password': 'Password_123'})

    response_new_password = auth_client.post(reverse('login_user'),
                                             data=json.dumps({'username': 'Vasya_1995',
                                                              'password': 'Password_1234'}),
                                             content_type='application/json')

    assert response_change_pass.status_code == 200
    assert response_new_password.status_code == 200



