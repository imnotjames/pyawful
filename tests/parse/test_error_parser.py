import os

import pytest
from lxml.html import fromstring

from pyawful.errors import (
    AwfulError,
    InvalidLoginCredentials,
    RequiresAuthorization,
    WasLoggedOut,
)
from pyawful.parse.error_parser import parse_error


def get_example(filename: str) -> str:
    fixture_file = os.path.join(os.path.dirname(__file__), "fixtures", filename)

    with open(fixture_file) as f:
        return f.read()


@pytest.fixture()
def example_no_error_html():
    return get_example("member.html")


@pytest.fixture()
def example_bad_page_html():
    return get_example("error_bad_page.html")


@pytest.fixture()
def example_bad_forum_html():
    return get_example("error_bad_forum.html")


@pytest.fixture()
def example_requires_auth_html():
    return get_example("error_requires_auth.html")


@pytest.fixture()
def example_bad_password_html():
    return get_example("error_bad_password.html")


@pytest.fixture()
def example_logout_page_html():
    return get_example("logout_page.html")


@pytest.fixture()
def example_login_page_html():
    return get_example("login_page.html")


def test_parse_gets_bad_page_error(example_bad_page_html: str):
    response = parse_error(fromstring(example_bad_page_html))

    assert type(response) is AwfulError
    assert (
        str(response) == "The page number you requested does not exist in this thread."
    )


def test_parse_gets_bad_forum_error(example_bad_forum_html: str):
    response = parse_error(fromstring(example_bad_forum_html))

    assert type(response) is AwfulError
    assert str(response) == "Specified forum was not found in the live forums."


def test_parse_gets_requires_auth_error(example_requires_auth_html: str):
    response = parse_error(fromstring(example_requires_auth_html))

    assert isinstance(response, RequiresAuthorization)


def test_parse_gets_bad_password_error(example_bad_password_html: str):
    response = parse_error(fromstring(example_bad_password_html))

    assert isinstance(response, InvalidLoginCredentials)
    assert str(response) == "BAD PASSWORD!"
    assert response.attempt_count == 1


def test_parse_gets_logout_error(example_logout_page_html: str):
    response = parse_error(fromstring(example_logout_page_html))
    assert isinstance(response, WasLoggedOut)


def test_parse_gets_no_error_on_normal_page(example_no_error_html: str):
    response = parse_error(fromstring(example_no_error_html))

    assert response is None


def test_parse_gets_no_error_on_login_page(example_login_page_html: str):
    response = parse_error(fromstring(example_login_page_html))

    assert response is None
