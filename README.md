# Greemigration
## surviving the waiting line of Green Card applications

This is a project about making predictions on the timeline of Green Card applications (permanent residency) using survival analysis.

### Installation

The installation guide can be found [here](./INSTALL.md).

#### Model file

The model file is available upon request only.

### Running

I have included a few different version of the web app, with `webapp5` being the latest. To run the app locally:

```
python webapp5.py
```

I have assumed the python environment has been correctly setup.

To run it with `gunicorn`:

```
gunicorn webapp5:app
```

