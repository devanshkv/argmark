# argmark

[![GitHub issues](https://img.shields.io/github/issues/devanshkv/argmark?style=flat-square)](https://github.com/devanshkv/argmark/issues)
[![GitHub forks](https://img.shields.io/github/forks/devanshkv/argmark?style=flat-square)](https://github.com/devanshkv/argmark/forks)
[![GitHub stars](https://img.shields.io/github/stars/devanshkv/argmark?style=flat-square)](https://github.com/devanshkv/argmark/stars)
[![GitHub LICENSE](https://img.shields.io/github/license/devanshkv/argmark?style=flat-square)](https://github.com/devanshkv/argmark/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/argmark?style=flat-square)](https://pypi.org/project/argmark)
[![PyPI](https://img.shields.io/pypi/v/argmark?style=flat-square)](https://pypi.org/project/argmark)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fdevanshkv%2Fargmark.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fdevanshkv%2Fargmark?ref=badge_shield)

[![codecov](https://codecov.io/gh/devanshkv/argmark/branch/master/graph/badge.svg?style=flat-square)](https://codecov.io/gh/devanshkv/argmark)
  

Convert argparse based executable scripts to markdown documents. It is based on [argdown](https://github.com/9999years/argdown) but has a simpler interface and a cleaner code.
### Installation
For end-users, install `argmark` using pip:
```bash
pip install argmark
```
For development, please see the "Development" section below.

### Usage
Using `argmark` is very simple. Once installed, you can run it against a Python script that defines an `ArgumentParser`. For example, given a file `your_script.py`:

```python
import argparse

parser = argparse.ArgumentParser(
    prog="your_script.py",
    description="A sample script description.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-f", "--files", help="Files to read.", required=True, nargs="+",
)
parser.add_argument(
    "--limit", type=int, default=10, help="Maximum number of items to process."
)
# For argmark to find the parser, it needs to be accessible
# when the script is processed. Often, parse_args() is called.
# If not, ensure the parser object is discoverable by argmark's gen_help.
if __name__ == '__main__': # Or called directly if script is simple
    args = parser.parse_args()
```

Run `argmark -f your_script.py` (or the path to your script) and it would generate `your_script.md`:
```markdown

    your_script.py
    ==================
    
    # Description
    
    A sample script description.

    # Usage:
    
    ```bash
    usage: your_script.py [-h] -f FILES [FILES ...] [--limit LIMIT]
    ```

    # Arguments
    
    |short|long|default|help|
    | :---: | :---: | :---: | :---: |
    |`-h`|`--help`||show this help message and exit|
    |`-f`|`--files`|`None`|Files to read.|
    ||`--limit`|`10`|Maximum number of items to process.|

```

When developing `argmark` locally (after installing as shown in the "Development" section), you can invoke it from the project root using `uv`:
```bash
# Ensure your virtual environment is active
uv run argmark -- --files path/to/your_script.py
```
Note the `--` which separates arguments for `uv run` from arguments passed to the `argmark` script itself.



## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fdevanshkv%2Fargmark.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fdevanshkv%2Fargmark?ref=badge_large)