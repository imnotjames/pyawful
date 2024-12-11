from lxml.html import HtmlElement

from pyawful.parse.forum_parser import parse_forum_page


def test_parse_gets_page_location(example_forum_display: HtmlElement):
    response = parse_forum_page(example_forum_display)

    assert response.current_page == 1
    assert response.last_page == 651


def test_parse_gets_forum_name(example_forum_display: HtmlElement):
    response = parse_forum_page(example_forum_display)

    assert response.forum.id == 273
    assert response.forum.name == "General Bullshit"
