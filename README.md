# Summary

This README.md file provides an overview of the application, stack, development preparation, and deployment steps for the TravelLabel ML API.

## Overview

The TravelLabel Machine Learning API (ML API) is a RESTful API that serves as the backend for the machine learning models of the application. Currently, it handles one model, which is recommending similar destinations accoridng to user input.

## Tech Stack

The project utilizes the following technologies and frameworks:

- Python
- Tensorflow
- FastAPI
- Pandas
- Numpy
- Google Cloud Platform
    - Google Cloud Storage

## Development Preparation

To set up the development environment, follow these steps:

1. Install Python version as specified in `.python-version`.
2. Create a virtual environment to isolate dependencies: `python -m venv env`.
3. Install the required Python packages using pip: `pip install -r requirements.txt`.
4. Setup local versions of the required environment variables, by using `.env.example` as a template.
4. Run the application in development mode (with auto reload) by using `fastapi dev .\src\main.py`

## Deployment Steps
![Cloud Architecture Diagram](https://i.ibb.co.com/QdtYqGp/be-travellabel.png)
Please note that the included CI/CD using GitHub actions is already configured to build and deploy to Cloud Run. The following actions secrets are required for this CI/CD:
- `GCP_SA_KEY`: Key (JSON format) for the Service Account that will execute the deployment tasks.
- `IMAGE_TAG`: Image tag to push the built docker image to.
> [!IMPORTANT]
> Docker image must be pushed onto GCP Artifact Registry, as this is required by Cloud Run.
- `GCP_SERVICE_NAME`: Intended service name of the Cloud Run service.

To deploy the TravelLabel ML API in other platforms, follow these steps:

1. Set up a hosting provider or cloud platform that accepts Docker-format images. In this case, we will be using Cloud Run.
2. Configure the environment variables for the production environment (using `.env.example` as a template).
3. Build the application using the included Dockerfile.
4. Deploy the application image. Application will be exposed on the port according to the `PORT` environment variable, defaulting to 3000.
