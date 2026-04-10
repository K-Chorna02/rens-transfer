import sys, os

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app  # adjust this import to match your app

application = create_app()