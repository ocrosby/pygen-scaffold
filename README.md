# pygen-scaffold

A python program for scaffolding python projects.

![Test](https://github.com/ocrosby/pygen-scaffold/actions/workflows/ci.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/ocrosby/pygen-scaffold/badge.svg?branch=feature/init)](https://coveralls.io/github/ocrosby/pygen-scaffold?branch=feature/init)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)



## Setup

### Step 1. Create a virtual environment

You only need to do this once, if you've done it before for this project, you can skip this step.

```bash 
python3 -m venv venv
```

### Step 2. Activate the virtual environment

```bash
source venv/bin/activate
```

### Step 3. Upgrade PIP

```bash
pip install --upgrade pip
```

### Step 4. Install the dependencies

```bash
# Install the production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```


## Development Usage

### Clean transient files

```bash
inv clean
```

### Run the tests

```bash
inv test
```

### Generate Coverage Report

```bash
inv coverage
```

### Run the linter

```bash
inv lint
```

### Execute the build process

```bash
inv
```




## References
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)