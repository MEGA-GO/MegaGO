#!/bin/bash

# Switch to this virtual environment
source ./env/bin/activate

export FLASK_APP=app.py
export FLASK_ENV=development

flask run
