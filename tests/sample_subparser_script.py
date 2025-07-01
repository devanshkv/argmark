import argparse

parser = argparse.ArgumentParser(prog="app", description="Main app with subparsers.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")

subparsers = parser.add_subparsers(
    title="subcommands", dest="command", help="Available subcommands", required=True
)

# Subparser for 'command1'
parser_cmd1 = subparsers.add_parser(
    "command1",
    help="Short help for command1.",
    description="Detailed desc for command1",
)
parser_cmd1.add_argument("--opt1", type=int, default=10, help="Option for command1.")
parser_cmd1.add_argument("pos1", help="Positional arg for command1.")

# Subparser for 'command2'
parser_cmd2 = subparsers.add_parser(
    "command2", help="Short help for command2.", epilog="Epilog for command2"
)  # No explicit description
parser_cmd2.add_argument(
    "--flag", action="store_true", help="A boolean flag for command2."
)

# Call parse_args directly for gen_help to correctly identify the parser variable.
# The if __name__ == '__main__' block caused indentation issues with how gen_help constructs its exec string.
args = parser.parse_args(
    []
)  # Pass empty list to avoid issues with actual CLI args during testing/analysis
# print(args) # Not needed for argmark
