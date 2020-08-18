from argmark.argmark import *


def test_inline_code():
    assert inline_code("f") == "`f`"


def test_get_indent():
    assert get_indent("  foo") == 2
    assert get_indent("\tfoo") == 8
