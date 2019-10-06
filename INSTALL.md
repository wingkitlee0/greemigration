# Installation

## Structure

`Greemigration` contains two parts: the model and the web app. The model is put in a python package called `gcpredict`. The directory is structured like below:

```
greemigration/
    gcpredict/
    notebooks/
    webapp5/
    requirements.txt
    webapp5.py
    ...
```

The web apps are stored in `webappX/` where X is the version number. There should be a wrapper script `webappX.py` in the base directory (if not, just create one from other versions that you have).

## Installation Instructions

First, go to the root of the directory (i.e., `greemigration/`) and create a virtual environment for python packages:
```
virtualenv venv
```
where `venv` is the name of the environment. A new folder will be created.

Activate the environment:
```
source venv/bin/activate
```

Next, install the model package then all the packages from `requirements.txt`:
```
pip install gcpredict/
pip install -r requirements.txt
```
Make sure to include `/` for gcpredict as we are installing the version from the package directory directly.

## Running the web app locally

The web app can be run locally using `flask`. Simply use the following command:
```
python webapp5.py
```
where `webapp5.py` is located at `greemigration/`




