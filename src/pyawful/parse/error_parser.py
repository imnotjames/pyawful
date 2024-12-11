import re
from typing import Callable, Sequence

from lxml.cssselect import CSSSelector
from lxml.html import HtmlElement

from ..errors import (
    AwfulError,
    InvalidLoginCredentials,
    RequiresAuthorization,
    WasLoggedOut,
)
from .common import parse_str

PATTERN_REQUIRES_AUTH = re.compile(
    "Sorry, you must be a registered forums member to view this page"
)
PATTERN_LOGGED_OUT = re.compile(
    "It's a great day for the forums, because you've just logged out!"
)
PATTERN_LOGIN_ERROR_ATTEMPTS = re.compile(r"You've tried to login (\d+) times so far")

CSS_PAGE_IS_ERROR = CSSSelector("body.standarderror")
CSS_STANDARD_ERROR_REASON = CSSSelector(".standarderror .standard .inner")
CSS_PAGE_LOGIN_ERROR = CSSSelector(
    'body.loginform .login_form b[style*="color:red"][style*="font-size:1.5em"]'
)
CSS_LOGIN_FORM = CSSSelector("form.login_form")


def parse_bad_password_error(document: HtmlElement) -> AwfulError | None:
    if len(CSS_PAGE_LOGIN_ERROR(document)) == 0:
        return None

    message = parse_str(CSS_PAGE_LOGIN_ERROR(document))
    form_text = parse_str(CSS_LOGIN_FORM(document))
    attempt_match = PATTERN_LOGIN_ERROR_ATTEMPTS.findall(form_text)

    if attempt_match:
        attempt_count = int(attempt_match[0])
    else:
        attempt_count = 0

    return InvalidLoginCredentials(message, attempt_count)


def parse_standard_error_page(document: HtmlElement) -> AwfulError | None:
    if len(CSS_PAGE_IS_ERROR(document)) == 0:
        return None

    message = parse_str(CSS_STANDARD_ERROR_REASON(document)).strip()

    if PATTERN_REQUIRES_AUTH.match(message):
        return RequiresAuthorization()

    if PATTERN_LOGGED_OUT.match(message):
        return WasLoggedOut()

    return AwfulError(message)


ERROR_PARSERS: Sequence[Callable[[HtmlElement], AwfulError | None]] = (
    parse_bad_password_error,
    parse_standard_error_page,
)


def parse_error(document: HtmlElement) -> AwfulError | None:
    for parse in ERROR_PARSERS:
        error = parse(document)
        if error:
            return error
