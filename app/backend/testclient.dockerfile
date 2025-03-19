FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip install --force-reinstall httpcore==0.15 importlib-metadata==4.13.0

COPY ./client /app
ENV PYTHONPATH=/app
