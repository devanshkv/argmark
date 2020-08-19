# argmark

[![GitHub issues](https://img.shields.io/github/issues/devanshkv/argmark?style=flat-square)](https://github.com/devanshkv/argmark/issues)
[![GitHub forks](https://img.shields.io/github/forks/devanshkv/argmark?style=flat-square)](https://github.com/devanshkv/argmark/forks)
[![GitHub stars](https://img.shields.io/github/stars/devanshkv/argmark?style=flat-square)](https://github.com/devanshkv/argmark/stars)
[![GitHub LICENSE](https://img.shields.io/github/license/devanshkv/argmark?style=flat-square)](https://github.com/devanshkv/argmark/LICENSE)
[![codecov](https://codecov.io/gh/devanshkv/argmark/branch/master/graph/badge.svg?style=flat-square)](https://codecov.io/gh/devanshkv/argmark)
  

Convert argparse based executable scripts to markdown documents. It is based upon [argdown](https://github.com/9999years/argdown) but has a simpler interfaceand a cleaner code.
### Installation
```bash
pip install argmark
```

### Usage
Using `argmark` is very simple. For a sample python file [sample_argparse.py](tests/sample_argparse.py):

```python
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
```

Run `argmark -f sample_argparse.py` and it would generate:
```markdown

    sample_argparse.py
    ==================
    
    # Description
    
    
    Just a test
    # Usage:
    
    
    ```bash
    usage: sample_argparse.py [-h] -f FILES [FILES ...]
    
    ```
        # Arguments
    
    |short|long|default|help|
    | :---: | :---: | :---: | :---: |
    |`-h`|`--help`||show this help message and exit|
    |`-f`|`--files`|`None`|Files to read.|

```

