import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import User
from goals.models import Board, Category
from goals.serializers import CategorySerializer


@pytest.mark.django_db
def test_create(auth_user: APIClient, add_user: User, board: Board) -> None:
    response = auth_user.post(
        reverse('create_category'),
        data={
           'title': 'test cat',
           'user': add_user.pk,
           'board': board.pk,
        },
    )
    expected_response = {
        'id': response.data.get('id'),
        'title': 'test cat',
        'board': board.pk,
        'created': response.data.get('created'),
        'updated': response.data.get('updated'),
        'is_deleted': False,
    }

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve(auth_user: APIClient, add_user: User, category: Category, board: Board) -> None:
    response = auth_user.get(reverse('retrieve_category', args=[category.pk]))

    expected_response = CategorySerializer(instance=category).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_delete(auth_user: APIClient, board: Board, category: Category) -> None:
    response = auth_user.delete(reverse('retrieve_category', args=[category.pk]))

    assert response.status_code == 204


@pytest.mark.django_db
def test_update(auth_user: APIClient, board: Board, add_user: User, category: Category) -> None:
    response = auth_user.put(
        reverse('retrieve_category', args=[category.pk]),
        data=json.dumps({
            'title': 'put category',
            'board': board.pk
        }),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.data.get('title') == 'put category'
