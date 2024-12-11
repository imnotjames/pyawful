from datetime import datetime

import pytest
from lxml.html import HtmlElement

from pyawful.parse.profile_parser import parse_profile_page


def test_parse_gets_user_name(example_member: HtmlElement):
    response = parse_profile_page(example_member)

    assert response.user.username == "Jeffrey of YOSPOS"


def test_parse_gets_post_count_and_rate(example_member: HtmlElement):
    response = parse_profile_page(example_member)

    assert response.post_count == 28605
    assert response.post_rate == pytest.approx(4.13)


def test_parse_gets_contact_info(example_member: HtmlElement):
    response = parse_profile_page(example_member)

    assert response.icq_name == "42069"
    assert response.aim_username is None
    assert response.yahoo_name is None
    assert response.homepage_url is None


def test_parse_gets_last_posted_at(example_member: HtmlElement):
    expected = datetime(year=2024, month=12, day=5, hour=21, minute=37)
    response = parse_profile_page(example_member)

    assert response.last_posted_at == expected


def test_parse_gets_registration(example_member: HtmlElement):
    expected = datetime(year=2005, month=12, day=21, hour=0, minute=0)
    response = parse_profile_page(example_member)

    assert response.registered_at == expected
