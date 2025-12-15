# AWS Elastic Beanstalk WSGI Configuration
# This file is required for AWS EB to run FastAPI app

import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# Expose the FastAPI application for AWS EB
application = app

if __name__ == "__main__":
    application.run()
