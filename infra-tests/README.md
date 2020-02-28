# Testinfra tests for RHOSP 13

## Requirements

You will need the `tox` command for running the tests.

## Running the tests

The simplest way to run the tests is:

```
tox
```

This will run all the tests using eight workers, and will save results in `report.html`. The `tox` command will take care of setting up a virtual environment, installing required packages, and then running the commands in that virtual environment.

If you prefer, you can set up a virtual environment manually and install the requirements by running:

```
pip install -r requirements.txt
```
