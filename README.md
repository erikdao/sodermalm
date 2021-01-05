# Sodermalm - Server app for Data Studio

## Development setup

This project uses `poetry` as the main python env management tool, please make sure it's properly installed before going on.

- To install the dependencies, issue

```
$ poetry install
```

- Then to run the app in development mode, use

```
$ cd src/sodermalm
$ poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
