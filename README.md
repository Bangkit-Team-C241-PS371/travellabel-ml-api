# TravelLabel Machine Learning API
This endpoint provides a function for location recommendation according to user input on search bar. The user can send a location name to the API, and the API will return a tourist attractions recommendation. The API uses a pre-trained review and rating model to recommend a suitable destination.

To serve the backend for recommended locations, TravelLabel uses FastAPI that supported the deployment of TensorFlow model.

# Tech Stack
- TensorFlow
- Numpy
- Pandas
- Google Cloud Platform
    - Google Cloud SQL (PostgreSQL 15)
    - Google Cloud Storage
- FastAPI

# How to use
1. Clone this repository
```
git clone https://github.com/Bangkit-Team-C241-PS371/travellabel-ml-api.git
```
2. Install requirements
```
pip install -r requirements.txt
```