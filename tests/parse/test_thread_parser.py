from datetime import datetime

from lxml.html import HtmlElement

from pyawful.parse.thread_parser import parse_thread_page


def test_parse_gets_page_location(example_thread: HtmlElement):
    response = parse_thread_page(example_thread)

    assert response.current_page == 3
    assert response.last_page == 4


def test_parse_gets_locked_status(example_thread: HtmlElement):
    response = parse_thread_page(example_thread)

    assert not response.is_locked


def test_parse_gets_forum_reference(example_thread: HtmlElement):
    response = parse_thread_page(example_thread)

    assert response.forum.id == 273
    assert response.forum.name == "General Bullshit"


def test_parse_gets_thread_reference(example_thread: HtmlElement):
    response = parse_thread_page(example_thread)

    assert response.thread.id == 4076894
    assert response.thread.title == "ITT we're boomers online"


def test_parse_gets_posts(example_thread: HtmlElement):
    response = parse_thread_page(example_thread)

    assert len(response.posts) == 40

    actual_post = response.posts[0]

    assert actual_post.id == 543571595
    assert not actual_post.is_ignored


def test_parse_gets_post_dates(example_thread: HtmlElement):
    expected_created_at = datetime(year=2024, month=12, day=6, hour=13, minute=25)
    expected_modified_at = datetime(year=2024, month=12, day=6, hour=15, minute=53)

    response = parse_thread_page(example_thread)

    actual_post = response.posts[37]

    assert actual_post.last_modified_at != actual_post.created_at
    assert actual_post.created_at == expected_created_at
    assert actual_post.last_modified_at == expected_modified_at


def test_parse_gets_post_author(example_thread: HtmlElement):
    response = parse_thread_page(example_thread)

    actual_post = response.posts[0]

    assert actual_post.author.id == 215054
    assert actual_post.author.username == "AEMINAL"
