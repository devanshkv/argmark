import filecmp

from argmark.argmark import *

_install_dir = os.path.abspath(os.path.dirname(__file__))


def test_inline_code():
    assert inline_code("f") == "`f`"


def test_get_indent():
    assert get_indent("  foo") == 2
    assert get_indent("\tfoo") == 8


def test_gen_help():
    py_file = os.path.join(_install_dir, "sample_argparse.py")
    md_file = "sample_argparse.md"
    answer = os.path.join(_install_dir, "answer.md")
    with open(py_file, 'r') as f:
        gen_help(f.readlines())
    assert os.path.isfile(md_file)
    assert filecmp.cmp(md_file, answer)
    os.remove(md_file)
