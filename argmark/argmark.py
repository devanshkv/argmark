import argparse as _argparse
import logging
import os
import re
from typing import List
from inspect import cleandoc
from mdutils.mdutils import MdUtils


def inline_code(code: str) -> str:
    """
    Covert code to inline code

    Args:

        code (str) : code to be converted to inline code

    Returns:

        str: inline code

    """
    return f"`{code}`"



def gen_help(lines: List) -> None:
    """
    Generate lines of code containing the argument parser and pass it to md_help.

    Args:

        lines (List): List of the lines in the source code

    Returns:

        None

    """
    lines_string = ""
    lines_string += "import argparse"
    lines_string += "\n"
    lines_string += "import argmark"
    lines_string += "\n"

    parser_expr = re.compile(r"(\w+)\.parse_args\(")
    for i, line in enumerate(lines):
        if "ArgumentParser(" in line:
            firstline = i
        if ".parse_args(" in line:
            parser = re.search(parser_expr, line)
            if parser is not None:
                lastline = i
                parser = parser.group(1)
                break

    lines = lines[firstline:lastline]
    
    lines_string += cleandoc("\n".join(lines))
    lines_string += "\n"
    lines_string += f"argmark.md_help({parser})"
    logging.debug(lines_string)
    exec(lines_string, {"__name__": "__main__"})


def md_help(parser: _argparse.ArgumentParser) -> None:
    """
    Generate a mardown file from the given argument parser.
    Args:
        parser: parser object

    Returns:

    """
    if parser.prog is None:
        logging.info("Saving as foo.md")
        mdFile = MdUtils(file_name="foo")
    else:
        mdFile = MdUtils(file_name=os.path.splitext(parser.prog)[0], title=parser.prog)

    if parser.description:
        mdFile.new_header(level=1, title="Description")
        mdFile.new_paragraph(parser.description)

    if parser.epilog:
        mdFile.new_header(level=1, title="Epilog")
        mdFile.new_paragraph(parser.epilog)

    mdFile.new_header(level=1, title="Usage:")
    mdFile.insert_code(parser.format_usage(), language="bash")

    used_actions = {}
    options = ["short", "long", "default", "help"]
    i = 0
    for k in parser._option_string_actions:

        action = parser._option_string_actions[k]
        list_of_str = ["", "", "", action.help]
        this_id = id(action)
        if this_id in used_actions:
            continue
        used_actions[this_id] = True

        for opt in action.option_strings:
            # --, long option
            if len(opt) > 1 and opt[1] in parser.prefix_chars:
                list_of_str[1] = inline_code(opt)
            # short opt
            elif len(opt) > 0 and opt[0] in parser.prefix_chars:
                list_of_str[0] = inline_code(opt)

        if not (
            isinstance(action.default, bool)
            or isinstance(action, _argparse._VersionAction)
            or isinstance(action, _argparse._HelpAction)
        ):
            default = (
                action.default
                if isinstance(action.default, str)
                else repr(action.default)
            )
            list_of_str[2] = inline_code(default)

        options.extend(list_of_str)

        i += 1

    mdFile.new_header(level=1, title="Arguments")
    logging.debug(f"Creating Table with text={options}")
    logging.debug(f"Pre map {options}")
    options = [
        inline_code(di) if di is None else di.replace("\n", " ") for di in options
    ]
    logging.debug(f"Post map {options}")
    mdFile.new_table(
        columns=4,
        rows=len(options) // 4,
        text=options,
        text_align="left",
    )
    mdFile.create_md_file()


def main():
    parser = _argparse.ArgumentParser(
        prog="argmark",
        description="Convert argparse based bin scripts to markdown documents",
        formatter_class=_argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--files",
        help="files to convert",
        required=True,
        nargs="+",
    )
    parser.add_argument("-v", "--verbose", help="Be verbose", action="store_true")

    args, _ = parser.parse_known_args()

    logging_format = (
        "%(asctime)s - %(funcName)s -%(name)s - %(levelname)s - %(message)s"
    )

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=logging_format)
    else:
        logging.basicConfig(level=logging.INFO, format=logging_format)

    for file in args.files:
        with open(file, "r") as f:
            gen_help(f.readlines())


if __name__ == "__main__":
    main()
