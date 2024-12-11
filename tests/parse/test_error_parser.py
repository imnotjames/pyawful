from lxml.html import HtmlElement

from pyawful.errors import (
    AwfulError,
    InvalidLoginCredentials,
    RequiresAuthorization,
    WasLoggedOut,
)
from pyawful.parse.error_parser import parse_error


def test_parse_gets_bad_page_error(example_bad_page: HtmlElement):
    response = parse_error(example_bad_page)

    assert type(response) is AwfulError
    assert (
        str(response) == "The page number you requested does not exist in this thread."
    )


def test_parse_gets_bad_forum_error(example_bad_forum: HtmlElement):
    response = parse_error(example_bad_forum)

    assert type(response) is AwfulError
    assert str(response) == "Specified forum was not found in the live forums."


def test_parse_gets_requires_auth_error(example_requires_auth: HtmlElement):
    response = parse_error(example_requires_auth)

    assert isinstance(response, RequiresAuthorization)


def test_parse_gets_bad_password_error(example_bad_password: HtmlElement):
    response = parse_error(example_bad_password)

    assert isinstance(response, InvalidLoginCredentials)
    assert str(response) == "BAD PASSWORD!"
    assert response.attempt_count == 1


def test_parse_gets_logout_error(example_logout_page: HtmlElement):
    response = parse_error(example_logout_page)
    assert isinstance(response, WasLoggedOut)


def test_parse_gets_no_error_on_normal_page(example_no_error: HtmlElement):
    response = parse_error(example_no_error)

    assert response is None


def test_parse_gets_no_error_on_login_page(example_login_page: HtmlElement):
    response = parse_error(example_login_page)

    assert response is None
