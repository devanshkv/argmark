import argparse

parser = argparse.ArgumentParser(
    prog="sample_argparse.py",
    description="Just a test",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-f", "--files", help="Files to read.", required=True, nargs="+",
)
values = parser.parse_args()
