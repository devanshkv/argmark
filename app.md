
app
===

# Description


Main app with subparsers.
# Usage:


```bash
usage: app [-h] [--verbose] {command1,command2} ...

```
# Arguments

|short|long|default|help|
| :--- | :--- | :--- | :--- |
|`-h`|`--help`||show this help message and exit|
||`--verbose`||Enable verbose output.|

# Subcommands

## Subcommand: `command1`

# Description


Detailed desc for command1
# Usage:


```bash
usage: app command1 [-h] [--opt1 OPT1] pos1

```
## Arguments

|short|long|default|help|
| :--- | :--- | :--- | :--- |
|`-h`|`--help`||show this help message and exit|
||`--opt1`|`10`|Option for command1.|
||`pos1`||Positional arg for command1.|


---
## Subcommand: `command2`

# Epilog


Epilog for command2
# Usage:


```bash
usage: app command2 [-h] [--flag]

```
## Arguments

|short|long|default|help|
| :--- | :--- | :--- | :--- |
|`-h`|`--help`||show this help message and exit|
||`--flag`||A boolean flag for command2.|


---