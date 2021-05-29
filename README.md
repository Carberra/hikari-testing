# Discord bots in Python (2022)

Welcome to the official GitHub repository for the [Discord bots in Python (2022)](https://www.youtube.com/playlist?list=PLYeOw6sTSy6YgGJUrfH4xTwoXMUE1NpBt) series by [Carberra Tutorials](https://youtube.carberra.xyz)!

This repository is designed purely as a supplementary aid to the series, and should **NOT** be downloaded without having watched it first.

You can [browse the tags](https://github.com/Carberra/hikari-tutorial/releases) to view the code as it was after a specific episode.

## Prerequisites

### Things you'll need

- [Python 3.8.0 or greater](https://python.org/downloads)
- [A Discord bot](https://discord.com/developers/applications)

### Dependency table

|                        | Required | Used in series |
| ---------------------- | -------- | -------------- |
| **hikari[speedups]\*** | -        | -              |
| **hikari-lightbulb**   | -        | -              |
| **uvloop**             | -        | -              |
| **apscheduler**        | -        | -              |
| **aiosqlite**          | -        | -              |
| **psutil\*\***         | -        | -              |
| **pygount\*\***        | -        | -              |

*You need to meet [these conditions](https://github.com/hikari-py/hikari#hikarispeedups) to use speedups.
**These are only used in case studies.

### Installing required libraries

To install the necessary libraries, run one of the the following commands:

```bash
# Windows
py -3.9 -m pip install "hikari[speedups]" hikari-lightbulb uvloop apscheduler aiosqlite psutil pygount

# Linux/macOS
python3.9 -m pip install "hikari[speedups]" hikari-lightbulb uvloop apscheduler aiosqlite psutil pygount

# In a virtual environment
pip install "hikari[speedups]" hikari-lightbulb uvloop apscheduler aiosqlite psutil pygount
```

## License

This repository is made available via the [BSD 3-Clause License](https://github.com/Carberra/hikari-tutorial/blob/main/LICENSE).

## Help and further information

If you need help using this repository, [watch the series](https://www.youtube.com/playlist?list=PLYeOw6sTSy6YgGJUrfH4xTwoXMUE1NpBt). If you still need help beyond that, [join the Carberra Tutorials Discord server](https://discord.carberra.xyz).
