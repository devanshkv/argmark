import argparse as _argparse
import logging
import os
import re
from typing import List

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


def get_indent(line: str) -> int:
    """

    Get the indent of the file.

    Args:

        line (str) : A string whose indent needs to be found

    Returns:

        int: Indent

    """
    indent = 0
    for c in line:
        if c == " ":
            indent += 1
        elif c == "\t":
            indent += 8
        else:
            # break on first word / non-white char
            break
    return indent


def gen_help(lines: List) -> None:
    """
    Generate the help given the source code as list of lines

    Args:

        lines (List): List of the lines in the source code

    Returns:

        None

    """
    indent = 0
    parser_expr = re.compile(r"(\w+)\.parse_args\(")
    for i, line in enumerate(lines):
        if ".parse_args(" in line:
            parser = re.search(parser_expr, line)
            if parser is not None:
                lastline = i
                parser = parser.group(1)
                indent = get_indent(line)
                break
    lines = lines[:lastline]
    lines.append("\n")
    lines.append(" " * indent + "import argmark")
    lines.append(" " * indent + f"argmark.md_help({parser})")
    logging.debug("\n".join(lines))
    exec("\n".join(lines), {"__name__": "__main__"})


def get_options(parser : _argparse.ArgumentParser, actions_list: List[_argparse.Action]):
    """
    Get the options from the actions list

    Args:

        actions_list: actions list

    Returns:

        List: list of options

    """
    used_actions = []
    for action in actions_list:
        option = ["", "", action.help]
        this_id = id(action)
        if this_id in used_actions:
            continue
        used_actions.append(this_id)

        if not action.option_strings:
            option[0] = inline_code(action.dest)
        else:
            for opt in action.option_strings:
                option[0] += inline_code(opt) + ", "
            option[0] = option[0][:-2]    

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
            option[1] = inline_code(default)
        yield option, action.required


def md_help(parser: _argparse.ArgumentParser) -> None:
    """
    Generate a mardown file from the given argument parser.
    Args:
        parser: parser object

    Returns:

    """
    def add_table_section(name: str, options: List[str]):
        mdFile.new_header(level=1, title=name)
        logging.debug(f"Creating Table with text={options}")
        logging.debug(f"Pre map {options}")
        options = [
            inline_code(di) if di is None else di.replace("\n", " ") for di in options
        ]
        logging.debug(f"Post map {options}")
        mdFile.new_table(
            columns=3,
            rows=len(options) // 3,
            text=options,
            text_align="left",
        )

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

    positional_options = ["Option", "Default", "Description"]
    optional_options = ["Option", "Default", "Description"]
    required_options = ["Option", "Default", "Description"]
    for option, required in get_options(parser, parser._positionals._group_actions):
        positional_options.extend(option)
    for option, required in get_options(parser, parser._optionals._group_actions):
        if required:
            required_options.extend(option)
        else:
            optional_options.extend(option)
    
    if len(positional_options) > 3:
        add_table_section("Positional Arguments", positional_options)
    if len(required_options) > 3:
        add_table_section("Required Arguments", required_options)
    if len(optional_options) > 3:
        add_table_section("Optional Arguments", optional_options)

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
