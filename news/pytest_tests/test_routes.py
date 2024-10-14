from http import HTTPStatus
import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

@pytest.mark.parametrize(
    'name',
    (
            'news:home',
            # 'news:detail',
            'users:login',
            'users:logout',
            'users:signup',
    )
)
def test_pages_availability_unauthorized(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
            (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
    ),
)
@pytest.mark.parametrize(
    'name, args',
    (
            ('news:delete', pytest.lazy_fixture('slug_for_args')),
            ('news:edit', pytest.lazy_fixture('slug_for_args')),
    )
)
def test_pages_availability_for_author(parametrized_client, name, args, expected_status, comment):

    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status

#ToDo написать тест на редиректы.