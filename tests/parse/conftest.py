import os

import pytest
from lxml.html import HtmlElement, fromstring


def get_example(filename: str) -> HtmlElement:
    fixture_file = os.path.join(os.path.dirname(__file__), "fixtures", filename)

    with open(fixture_file) as f:
        return fromstring(f.read())


@pytest.fixture()
def example_no_error():
    return get_example("member.html")


@pytest.fixture()
def example_bad_page():
    return get_example("error_bad_page.html")


@pytest.fixture()
def example_bad_forum():
    return get_example("error_bad_forum.html")


@pytest.fixture()
def example_requires_auth():
    return get_example("error_requires_auth.html")


@pytest.fixture()
def example_bad_password():
    return get_example("error_bad_password.html")


@pytest.fixture()
def example_logout_page():
    return get_example("logout_page.html")


@pytest.fixture()
def example_login_page():
    return get_example("login_page.html")


@pytest.fixture()
def example_forum_display():
    return get_example("forumdisplay.html")


@pytest.fixture()
def example_member():
    return get_example("member.html")


@pytest.fixture()
def example_thread():
    return get_example("showthread.html")
