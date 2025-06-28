import argparse as _argparse
import logging
import os
import re
from typing import List, Union 
from inspect import cleandoc
import sys
from mdutils.mdutils import MdUtils


def inline_code(text: str) -> str:
    return f"`{text}`"

# Helper functions for md_help

def _create_md_file_object(parser: _argparse.ArgumentParser) -> MdUtils:
    if parser.prog is None:
        logging.info("parser.prog is None, saving as foo.md")
        md_file = MdUtils(file_name="foo", title="foo")
    else:
        file_name_base = os.path.splitext(parser.prog)[0]
        md_file = MdUtils(file_name=file_name_base, title=parser.prog)

    if parser.prog and not parser.prog.endswith(".py") and md_file.title.startswith("\n"):
        md_file.title = md_file.title.lstrip("\n")

    return md_file

def _add_parser_description(md_file: MdUtils, parser: _argparse.ArgumentParser) -> None:
    if parser.description:
        md_file.new_header(level=1, title="Description")
        md_file.new_paragraph(parser.description)

def _add_parser_epilog(md_file: MdUtils, parser: _argparse.ArgumentParser) -> None:
    if parser.epilog:
        md_file.new_header(level=1, title="Epilog")
        md_file.new_paragraph(parser.epilog)

def _add_usage_section(md_file: MdUtils, parser: _argparse.ArgumentParser) -> None:
    md_file.new_header(level=1, title="Usage:")
    usage_string = parser.format_usage() if parser.format_usage() is not None else ""
    md_file.insert_code(usage_string, language="bash")

def _format_action_for_table_row(action: _argparse.Action, parser: _argparse.ArgumentParser) -> List[str]:
    """
    Formats a single argparse.Action into a list of 4 strings for the arguments table.
    Handles both optional and positional arguments based on action.option_strings.
    """
    short_opt_str = ""
    long_opt_str = ""
    default_cell_str = ""
    
    if action.option_strings: # Optional argument
        short_opts_list = [inline_code(s) for s in action.option_strings if s.startswith('-') and not s.startswith('--')]
        long_opts_list = [inline_code(s) for s in action.option_strings if s.startswith('--')]
        short_opt_str = ", ".join(short_opts_list) if short_opts_list else ""
        long_opt_str = ", ".join(long_opts_list) if long_opts_list else ""
    else: # Positional argument
        short_opt_str = "" 
        long_opt_str = inline_code(action.dest) # Use 'dest' as the name for positional args

    # Default string formatting
    if isinstance(action, (_argparse._HelpAction, _argparse._VersionAction)) or \
       isinstance(action.default, bool) or \
       action.default == _argparse.SUPPRESS:
        default_cell_str = ""
    # Specific check for required positionals (no option_strings) with no meaningful default
    elif action.required and action.default is None and not action.option_strings and action.nargs is None : 
         default_cell_str = "" 
    elif action.default is None:
        default_cell_str = inline_code("None")
    else:
        val_str = str(action.default) if isinstance(action.default, str) else repr(action.default)
        default_cell_str = inline_code(val_str)
        
    # Help text string formatting
    if action.help is None:
        help_text_str = inline_code("None")
    elif action.help == _argparse.SUPPRESS:
        help_text_str = ""
    else:
        formatter = parser._get_formatter()
        help_text_str = formatter._expand_help(action).replace("\n", " ")
        
    return [short_opt_str, long_opt_str, default_cell_str, help_text_str]

def _build_arguments_table_data(parser: _argparse.ArgumentParser) -> List[str]:
    table_rows_data: List[List[str]] = [] # Stores lists of 4 strings (each list is a row)
    seen_action_ids = set()

    # First Pass (Optionals): Iterate through parser._option_string_actions.keys()
    # to match original iteration behavior for optionals.
    for option_string_key in parser._option_string_actions.keys():
        action = parser._option_string_actions[option_string_key]
        
        if id(action) in seen_action_ids:
            continue
        if isinstance(action, _argparse._SubParsersAction): # Skip subparser actions themselves
            continue
        
        # This pass is primarily for optionals.
        # _format_action_for_table_row handles based on action.option_strings
        table_rows_data.append(_format_action_for_table_row(action, parser))
        seen_action_ids.add(id(action))

    # Second Pass (Positionals): Iterate through parser._actions
    for action in parser._actions:
        if id(action) in seen_action_ids: # Already processed
            continue
        if isinstance(action, _argparse._SubParsersAction): 
            continue
        
        # If it has no option_strings, it's a positional argument
        if not action.option_strings:
            table_rows_data.append(_format_action_for_table_row(action, parser))
            # No need to add to seen_action_ids here as this is the final pass for this action
            
    # Flatten the table_rows_data with the header
    final_table_list: List[str] = ["short", "long", "default", "help"]
    for row in table_rows_data:
        final_table_list.extend(row)
            
    logging.debug(f"Built arguments table data for parser '{parser.prog}': {final_table_list}")
    return final_table_list

def _add_arguments_table(md_file: MdUtils, table_data: List[str], is_subcommand: bool = False) -> None:
    level = 2 if is_subcommand else 1 
    md_file.new_header(level=level, title="Arguments") 
    
    num_header_items = 4
    num_data_rows = (len(table_data) - num_header_items) // num_header_items
    
    if num_data_rows <= 0: 
        md_file.new_paragraph("No arguments defined for this command/subcommand.")
        return

    md_file.new_table(
        columns=num_header_items,
        rows=num_data_rows + 1, 
        text=table_data, 
        text_align="left",
    )

def gen_help(lines: List) -> None:
    lines_string = "import argparse\nimport argmark\n"
    parser_expr = re.compile(r"(\w+)\.parse_args\(")
    firstline_idx, lastline_idx = -1, -1
    parser_var_name = None

    for i, line in enumerate(lines):
        if firstline_idx == -1 and "ArgumentParser(" in line:
            firstline_idx = i
        if firstline_idx != -1 and ".parse_args(" in line:
            var_match = re.search(r"(\b[a-zA-Z_][a-zA-Z0-9_]*\b)\s*\.\s*parse_args\(", line)
            if var_match:
                potential_parser_var = var_match.group(1)
                parser_def_segment = "\n".join(lines[firstline_idx:i+1])
                if f"{potential_parser_var} = " in parser_def_segment or f"{potential_parser_var}=" in parser_def_segment:
                    parser_var_name = potential_parser_var
                    lastline_idx = i 
                    break 
    
    if firstline_idx == -1 or lastline_idx == -1 or parser_var_name is None:
        logging.error("Could not robustly find ArgumentParser or the var calling .parse_args().")
        return
    
    script_segment_for_parser_def = cleandoc("\n".join(lines[firstline_idx:lastline_idx]))
    final_exec_string = f"{script_segment_for_parser_def}\nargmark.md_help({parser_var_name})"
    
    exec_globals = {
        "argparse": _argparse, "argmark": sys.modules[__name__], "__name__": "__main__" }
    logging.debug(f"Executing for gen_help:\n{final_exec_string}")
    try:
        exec(final_exec_string, exec_globals)
    except Exception as e:
        logging.error(f"Error executing for gen_help: {e}\nCode:\n{final_exec_string}", exc_info=True)

def md_help(parser: _argparse.ArgumentParser) -> None:
    md_file = _create_md_file_object(parser)

    if parser.prog and md_file.title == parser.prog: 
        md_file.new_header(level=1, title=parser.prog)
    
    _add_parser_description(md_file, parser)
    _add_parser_epilog(md_file, parser)
    _add_usage_section(md_file, parser)
    
    main_table_data = _build_arguments_table_data(parser) 
    
    if len(main_table_data) > 4: 
        _add_arguments_table(md_file, main_table_data, is_subcommand=False)
    else:
        md_file.new_header(level=1, title="Arguments") 
        md_file.new_paragraph("No command-line arguments defined (excluding default help).")
        logging.info(f"No arguments to document in the table for parser '{parser.prog}'.")

    subparsers_action = None
    for action in parser._actions:
        if isinstance(action, _argparse._SubParsersAction):
            subparsers_action = action
            break
    
    if subparsers_action and hasattr(subparsers_action, 'choices') and subparsers_action.choices:
        md_file.new_header(level=1, title="Subcommands") 
        for name, sub_parser_instance in subparsers_action.choices.items():
            md_file.new_header(level=2, title=f"Subcommand: {inline_code(name)}")
            
            if sub_parser_instance.description:
                _add_parser_description(md_file, sub_parser_instance) 
            if sub_parser_instance.epilog:
                _add_parser_epilog(md_file, sub_parser_instance) 
            
            _add_usage_section(md_file, sub_parser_instance) 

            sub_table_data = _build_arguments_table_data(sub_parser_instance)
            if len(sub_table_data) > 4:
                _add_arguments_table(md_file, sub_table_data, is_subcommand=True) 
            else:
                md_file.new_header(level=2, title="Arguments") 
                md_file.new_paragraph(f"No arguments defined for subcommand {inline_code(name)}.")
            md_file.new_paragraph("---") 

    md_file.create_md_file()

    md_path = md_file.file_name if md_file.file_name.endswith(".md") else md_file.file_name + ".md"
    with open(md_path, "a", encoding="utf-8") as f:
        if not open(md_path, "rb").read().endswith(b"\n"):
            f.write("\n")

def main():
    script_argv = [arg for arg in sys.argv[1:] if arg != '--']
    parser = _argparse.ArgumentParser(
        prog="argmark",
        description="Convert argparse based bin scripts to markdown documents",
        formatter_class=_argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-f", "--files", help="files to convert", required=True, nargs="+")
    parser.add_argument(
        "-v", "--verbose", help="Be verbose", action="store_true")

    args, unknown_args = parser.parse_known_args(script_argv)
    logging_format = "%(asctime)s - %(funcName)s -%(name)s - %(levelname)s - %(message)s"
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=logging_format)
    else:
        logging.basicConfig(level=logging.INFO, format=logging_format)

    if unknown_args:
        logging.warning(f"Unknown arguments encountered and ignored: {unknown_args}")

    for file_path in args.files:
        try:
            with open(file_path, "r") as f:
                gen_help(f.readlines())
        except FileNotFoundError as e:
            logging.error(f"Error: File not found: {file_path}. {e}")
        except IOError as e:
            logging.error(f"Error: Could not read file {file_path}. {e}")
        # Removed the general Exception catch to be more specific as per instructions
        # If other errors need to be caught, they can be added here.

if __name__ == "__main__":
    main()
