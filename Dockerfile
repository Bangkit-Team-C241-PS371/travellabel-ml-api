FROM --platform=linux/amd64 python:3.11.9-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app

 # run the uvicorn from within the app as we need to inject the PORT env var from there
ENTRYPOINT ["python3", "main.py"]
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
