# Logga

## Overview
Python logging made super easy!  Build and read the docs (as per below) for more info.

## Prerequisites
- [GNU make](https://www.gnu.org/software/make/manual/make.html)
- Python 3 Interpreter. [We recommend installing pyenv](https://github.com/pyenv/pyenv)
- [Docker](https://www.docker.com/)

## Getting Started
[Makester](https://loum.github.io/makester/) is used as the Integrated Developer Platform.

### (macOS Users only) Upgrading GNU Make
Follow [these notes](https://loum.github.io/makester/macos/#upgrading-gnu-make-macos) to get [GNU make](https://www.gnu.org/software/make/manual/make.html).

### Creating the Local Environment
Get the code and change into the top level `git` project directory:
```
git clone https://github.com/loum/logga.git && cd logga
```

> **_NOTE:_** Run all commands from the top-level directory of the `git` repository.

For first-time setup, get the [Makester project](https://github.com/loum/makester.git):
```
git submodule update --init
```

Initialise the environment:
```
make init
```

## Build the Documentation
Detailed project documentation is self contained under the ``doc/source`` directory. To build the documentation locally:

```
make docs
```

To serve the documentation locally:
```
python -m http.server --directory doc/build 19888
```

To view pages, open up a web browser and navigate to [http//:localhost:19888](http//:localhost:19888).
