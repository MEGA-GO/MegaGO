import imp
import os

from pathlib import Path

app = imp.load_source(
    'app',
    os.path.join(Path(__file__).parent, 'app.py')
)

# Required for passenger to work and connect with this through the WSGI interface.
from app import app as application
